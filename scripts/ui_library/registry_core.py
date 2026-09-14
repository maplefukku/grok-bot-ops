from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence
from urllib.parse import urlparse

DEFAULT_REGISTRY = Path(__file__).resolve().parent / "data" / "registry.json"
_SLUG_RE = re.compile(r"[^a-z0-9]+")
_KEBAB_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


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
        return {
            "name": self.name,
            "title": self.title,
            "description": self.description,
            "categories": list(self.categories),
            "sourceUrl": self.source_url,
            "why": self.why,
            "useCases": list(self.use_cases),
        }


class RegistryError(ValueError):
    pass


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
    return base[:80] or "ref"


class RegistryCatalog:
    def __init__(self, path: Path | None = None) -> None:
        self._path = path or DEFAULT_REGISTRY
        self._data: dict[str, Any] | None = None

    @property
    def path(self) -> Path:
        return self._path

    def load(self) -> dict[str, Any]:
        if self._data is not None:
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
                item_path = self._path.parent / f"{raw['name']}.json"
                item_path.write_text(
                    json.dumps(raw, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                )
        self._data = data

    def items(self) -> list[RegistryItemRef]:
        data = self.load()
        out: list[RegistryItemRef] = []
        for raw in data["items"]:
            if not isinstance(raw, dict):
                continue
            out.append(_item_ref(raw))
        return out

    def get(self, name: str) -> RegistryItemRef | None:
        for item in self.items():
            if item.name == name:
                return item
        return None

    def view(self, name: str) -> dict[str, Any] | None:
        """shadcn MCP `view_items_in_registries` WRAP — full registry-item JSON."""
        item = self.get(name)
        if item is None:
            return None
        payload = dict(item.raw)
        payload["registry"] = self.load().get("name", "@ui-refs")
        payload["registryItem"] = f"{payload['registry']}/{name}"
        return payload

    def examples(
        self,
        query: str,
        *,
        use_case: str | None = None,
        limit: int = 10,
    ) -> list[RegistryItemRef]:
        """shadcn MCP `get_item_examples_from_registries` WRAP — docs + description."""
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
        name = item.get("name")
        if not isinstance(name, str) or not name:
            raise RegistryError("item.name is required")
        replaced = False
        for idx, existing in enumerate(items):
            if isinstance(existing, dict) and existing.get("name") == name:
                items[idx] = dict(item)
                replaced = True
                break
        if not replaced:
            items.append(dict(item))
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


def validate_registry_shape(data: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    if "$schema" not in data:
        errors.append("missing $schema")
    if not isinstance(data.get("items"), list):
        errors.append("items must be array")
        return errors
    for idx, item in enumerate(data["items"]):
        if not isinstance(item, dict):
            errors.append(f"items[{idx}] must be object")
            continue
        if not item.get("name"):
            errors.append(f"items[{idx}].name required")
        if not item.get("type"):
            errors.append(f"items[{idx}].type required")
        desc = item.get("description")
        if not isinstance(desc, str) or not desc.strip():
            errors.append(f"items[{idx}].description required for index")
        for tag in item.get("categories") or []:
            if isinstance(tag, str) and tag and not _KEBAB_RE.match(tag):
                errors.append(f"items[{idx}].categories not kebab: {tag}")
        fleet = (item.get("meta") or {}).get("fleet") if isinstance(item.get("meta"), dict) else {}
        if isinstance(fleet, dict):
            for tag in fleet.get("useCases") or []:
                if isinstance(tag, str) and tag and not _KEBAB_RE.match(tag):
                    errors.append(f"items[{idx}].meta.fleet.useCases not kebab: {tag}")
    return errors
