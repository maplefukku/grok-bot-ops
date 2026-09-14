from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping
from urllib.parse import urlparse

DEFAULT_REGISTRY = Path(__file__).resolve().parent / "data" / "registry.json"
_SLUG_RE = re.compile(r"[^a-z0-9]+")
_KEBAB_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_ITEM_NAME_RE = _KEBAB_RE
_RESERVED_ITEM_NAMES = frozenset({"registry"})


@dataclass(frozen=True)
class RegistryItemRef:
    name: str
    title: str
    description: str
    categories: tuple[str, ...]
    source_url: str | None
    why: str | None
    use_cases: tuple[str, ...]
    raw: Mapping[str, Any]

    def as_public(self) -> dict[str, Any]:
        fleet = (
            self.raw.get("meta", {}).get("fleet", {})
            if isinstance(self.raw.get("meta"), dict)
            else {}
        )
        out: dict[str, Any] = {
            "name": self.name,
            "title": self.title,
            "description": self.description,
            "categories": list(self.categories),
            "sourceUrl": self.source_url,
            "why": self.why,
            "useCases": list(self.use_cases),
        }
        if isinstance(fleet, dict) and fleet.get("source"):
            out["source"] = fleet["source"]
        return out


class RegistryError(ValueError):
    pass


def validate_item_name(name: str) -> str:
    if not isinstance(name, str) or not name.strip():
        raise RegistryError("item.name is required")
    cleaned = name.strip()
    if cleaned != name:
        raise RegistryError("item.name must not have surrounding whitespace")
    if any(sep in cleaned for sep in ("/", "\\", "..")):
        raise RegistryError(f"item.name must not contain path separators: {name!r}")
    if cleaned in _RESERVED_ITEM_NAMES:
        raise RegistryError(f"item.name is reserved: {name!r}")
    if not _ITEM_NAME_RE.match(cleaned):
        raise RegistryError(f"item.name must be kebab-case: {name!r}")
    return cleaned


def to_kebab_tag(value: str) -> str:
    tag = _SLUG_RE.sub("-", value.strip().lower()).strip("-")
    if not tag:
        raise RegistryError("use-case tag must be non-empty")
    if not _KEBAB_RE.match(tag):
        raise RegistryError(f"use-case must be kebab-case: {value!r}")
    return tag


def slug_from_url(url: str) -> str:
    parsed = urlparse(url.strip())
    host = (parsed.hostname or "ref").lower().replace(".", "-")
    path = _SLUG_RE.sub("-", (parsed.path or "").lower()).strip("-")
    base = "-".join(part for part in (host, path) if part)
    if parsed.query:
        digest = hashlib.sha256(parsed.query.encode("utf-8")).hexdigest()[:8]
        base = f"{base}-{digest}" if base else digest
    if parsed.fragment:
        digest = hashlib.sha256(parsed.fragment.encode("utf-8")).hexdigest()[:6]
        base = f"{base}-f{digest}"
    slug = base[:80] or "ref"
    return validate_item_name(slug)


class RegistryCatalog:
    def __init__(self, path: Path | None = None) -> None:
        self._path = path or DEFAULT_REGISTRY
        self._data: dict[str, Any] | None = None

    @property
    def path(self) -> Path:
        return self._path

    def data_dir(self) -> Path:
        return self._path.parent.resolve()

    def item_file_path(self, name: str) -> Path:
        safe = validate_item_name(name)
        resolved = (self.data_dir() / f"{safe}.json").resolve()
        if not resolved.is_relative_to(self.data_dir()):
            raise RegistryError(f"item path escapes data dir: {name!r}")
        return resolved

    def load(self, *, force: bool = False) -> dict[str, Any]:
        if self._data is not None and not force:
            return self._data
        try:
            text = self._path.read_text(encoding="utf-8")
        except FileNotFoundError as exc:
            raise RegistryError(f"missing registry: {self._path}") from exc
        data = json.loads(text)
        if not isinstance(data, dict):
            raise RegistryError("registry root must be an object")
        items = data.get("items")
        if not isinstance(items, list):
            raise RegistryError("registry.items must be an array")
        self._data = data
        return data

    def save(self) -> None:
        data = self.load()
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        for raw in data.get("items", []):
            if isinstance(raw, dict) and raw.get("name"):
                safe = validate_item_name(str(raw["name"]))
                item_path = self.item_file_path(safe)
                item_path.write_text(
                    json.dumps(raw, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                )
        self._data = data

    def read_item_json_from_disk(self, name: str) -> dict[str, Any] | None:
        """Canonical item for MCP wire (`…/data/{name}.json`)."""
        try:
            item_path = self.item_file_path(name)
        except RegistryError:
            return None
        if not item_path.is_file():
            return None
        data = json.loads(item_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise RegistryError(f"invalid item json: {item_path}")
        return data

    def get_raw(self, name: str) -> dict[str, Any] | None:
        disk = self.read_item_json_from_disk(name)
        if disk is not None:
            return disk
        safe = validate_item_name(name)
        for raw in self.load().get("items", []):
            if isinstance(raw, dict) and raw.get("name") == safe:
                return dict(raw)
        return None

    def items(self) -> list[RegistryItemRef]:
        data = self.load()
        out: list[RegistryItemRef] = []
        for raw in data["items"]:
            if not isinstance(raw, dict):
                continue
            out.append(_item_ref(raw))
        return out

    def get(self, name: str) -> RegistryItemRef | None:
        raw = self.get_raw(name)
        if raw is None:
            return None
        return _item_ref(raw)

    def view(self, name: str) -> dict[str, Any] | None:
        """Local WRAP of shadcn `view_items_in_registries` — reads disk item JSON when present."""
        raw = self.get_raw(name)
        if raw is None:
            return None
        payload = dict(raw)
        payload["registry"] = self.load().get("name", "@ui-refs")
        payload["registryItem"] = f"{payload['registry']}/{validate_item_name(name)}"
        payload["mcpWirePath"] = str(
            self.item_file_path(validate_item_name(name)).relative_to(self.data_dir())
        )
        return payload

    def examples(
        self,
        query: str,
        *,
        use_case: str | None = None,
        limit: int = 10,
    ) -> list[RegistryItemRef]:
        """Local subset WRAP of `get_item_examples_from_registries` (docs text; no files[].content)."""
        hits = self.search(query, use_case=use_case, limit=limit * 3)
        out: list[RegistryItemRef] = []
        q = query.strip().lower()
        for item in hits:
            docs = str(item.raw.get("docs") or "").lower()
            desc = item.description.lower()
            if not q or q in docs or q in desc or any(t in docs for t in q.split()):
                out.append(item)
            if len(out) >= limit:
                break
        return out

    def list_names(self) -> list[str]:
        return [item.name for item in self.items()]

    def search(
        self,
        query: str,
        *,
        use_case: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> list[RegistryItemRef]:
        q = query.strip().lower()
        uc = use_case.strip().lower() if use_case else None
        scored: list[tuple[int, RegistryItemRef]] = []
        for item in self.items():
            if uc and uc not in {c.lower() for c in item.use_cases}:
                if uc not in {c.lower() for c in item.categories}:
                    continue
            hay = " ".join(
                [
                    item.name,
                    item.title,
                    item.description,
                    item.source_url or "",
                    " ".join(item.categories),
                    " ".join(item.use_cases),
                    item.why or "",
                ]
            ).lower()
            if not q:
                score = 0
            elif q in hay:
                score = 100 - hay.index(q)
            else:
                tokens = [t for t in q.split() if t]
                if not tokens:
                    score = 0
                elif all(t in hay for t in tokens):
                    score = 50
                else:
                    continue
            scored.append((score, item))
        scored.sort(key=lambda pair: (-pair[0], pair[1].name))
        window = scored[offset : offset + limit]
        return [item for _, item in window]

    def upsert_item(self, item: Mapping[str, Any]) -> None:
        data = self.load()
        items: list[Any] = data.setdefault("items", [])
        name = validate_item_name(str(item.get("name") or ""))
        payload = dict(item)
        payload["name"] = name
        replaced = False
        for idx, existing in enumerate(items):
            if isinstance(existing, dict) and existing.get("name") == name:
                items[idx] = payload
                replaced = True
                break
        if not replaced:
            items.append(payload)
        self._data = data


def _item_ref(raw: Mapping[str, Any]) -> RegistryItemRef:
    name = str(raw.get("name") or "")
    title = str(raw.get("title") or name)
    description = str(raw.get("description") or "")
    categories_raw = raw.get("categories") or []
    categories = tuple(str(c) for c in categories_raw if c)
    meta = raw.get("meta") if isinstance(raw.get("meta"), dict) else {}
    fleet = meta.get("fleet") if isinstance(meta.get("fleet"), dict) else {}
    source_url = fleet.get("sourceUrl")
    if source_url is not None:
        source_url = str(source_url)
    why = fleet.get("ingestedWhy")
    if why is not None:
        why = str(why)
    use_raw = fleet.get("useCases") or categories
    use_cases = tuple(str(u) for u in use_raw if u)
    return RegistryItemRef(
        name=name,
        title=title,
        description=description,
        categories=categories,
        source_url=source_url,
        why=why,
        use_cases=use_cases,
        raw=dict(raw),
    )


def _validate_fleet_memory(item: dict[str, Any], idx: int) -> list[str]:
    errors: list[str] = []
    meta = item.get("meta")
    if not isinstance(meta, dict):
        errors.append(f"items[{idx}].meta required")
        return errors
    fleet = meta.get("fleet")
    if not isinstance(fleet, dict):
        errors.append(f"items[{idx}].meta.fleet required")
        return errors
    source = fleet.get("sourceUrl")
    why = fleet.get("ingestedWhy")
    if not isinstance(source, str) or not source.strip():
        errors.append(f"items[{idx}].meta.fleet.sourceUrl required")
    elif not source.strip().startswith(("http://", "https://")):
        errors.append(f"items[{idx}].meta.fleet.sourceUrl must be http(s)")
    if not isinstance(why, str) or not why.strip():
        errors.append(f"items[{idx}].meta.fleet.ingestedWhy required")
    return errors


def validate_registry_shape(data: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    if "$schema" not in data:
        errors.append("missing $schema")
    if not isinstance(data.get("items"), list):
        errors.append("items must be array")
        return errors
    seen_names: set[str] = set()
    for idx, item in enumerate(data["items"]):
        if not isinstance(item, dict):
            errors.append(f"items[{idx}] must be object")
            continue
        name = item.get("name")
        if not name:
            errors.append(f"items[{idx}].name required")
        else:
            try:
                safe = validate_item_name(str(name))
            except RegistryError as exc:
                errors.append(f"items[{idx}].name invalid: {exc}")
                safe = str(name)
            if safe in seen_names:
                errors.append(f"items[{idx}].duplicate name: {safe}")
            seen_names.add(safe)
        if not item.get("type"):
            errors.append(f"items[{idx}].type required")
        desc = item.get("description")
        if not isinstance(desc, str) or not desc.strip():
            errors.append(f"items[{idx}].description required for index")
        errors.extend(_validate_fleet_memory(item, idx))
        for tag in item.get("categories") or []:
            if isinstance(tag, str) and tag and not _KEBAB_RE.match(tag):
                errors.append(f"items[{idx}].categories not kebab: {tag}")
        fleet = (
            (item.get("meta") or {}).get("fleet")
            if isinstance(item.get("meta"), dict)
            else {}
        )
        if isinstance(fleet, dict):
            for tag in fleet.get("useCases") or []:
                if isinstance(tag, str) and tag and not _KEBAB_RE.match(tag):
                    errors.append(f"items[{idx}].meta.fleet.useCases not kebab: {tag}")
    return errors
