from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence
from urllib.parse import urlparse

from ui_library.registry_core import (
    RegistryCatalog,
    RegistryError,
    slug_from_url,
    to_kebab_tag,
)


@dataclass(frozen=True)
class IngestInput:
    """Public contract: X UI収集 lane hands URL+why only; index lives here."""

    url: str
    why: str
    use_cases: tuple[str, ...] = ()
    title: str | None = None


def _validate_url(url: str) -> None:
    parsed = urlparse(url.strip())
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise RegistryError("url must be http(s) with host")


def ingest_ref(
    catalog: RegistryCatalog,
    payload: IngestInput,
    *,
    name: str | None = None,
) -> str:
    _validate_url(payload.url)
    why = payload.why.strip()
    if not why:
        raise RegistryError("why is required")
    item_name = name or f"ref-{slug_from_url(payload.url)}"
    use_cases = tuple(
        to_kebab_tag(u) for u in payload.use_cases if u and u.strip()
    )
    title = (payload.title or item_name).strip()
    description = why.strip()
    item = {
        "name": item_name,
        "type": "registry:item",
        "title": title,
        "description": description,
        "categories": list(use_cases),
        "meta": {
            "fleet": {
                "sourceUrl": payload.url.strip(),
                "ingestedWhy": why,
                "useCases": list(use_cases),
                "context": "ui-library",
            }
        },
        "docs": f"Source: {payload.url.strip()}\n\nWhy: {why}",
    }
    catalog.upsert_item(item)
    catalog.save()
    return item_name
