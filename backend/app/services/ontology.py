"""Deterministic retrieval over the OntologySnapshot — the 'single source of truth'.

The ontology is a large structured data model (thousands of properties/classes with
definitions and domain values). We do NOT dump all of it into the prompt, and we do NOT
use vector embeddings (whose similarity ranking would be non-deterministic). Instead we do
transparent, reproducible keyword retrieval: per WTP theme we score every ontology concept
by how many theme keywords it contains and keep the top matches.

Two products come out of this module:
  • `full_text(rows)`   → the complete, human-readable rendering of the ontology, used as the
                          verification corpus so any ontology quote can be checked.
  • `retrieve(rows, k)` → a compact per-theme block injected into the prompt so the standard
                          side is grounded in the actual data model, not the model's memory.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

# The FIXED set of themes analysed every run — this is what makes the number of findings
# stable and reproducible (no more "8 vs 10 onderdelen"). Keep in sync with the frontend
# WTP_THEMES list.
CANONICAL_THEMES: list[str] = [
    "Opbouwsystematiek",
    "Partnerpensioen",
    "Wezenpensioen",
    "Arbeidsongeschiktheid (premievrijstelling)",
    "Indexatie/Toeslagen",
    "Compensatie afschaffing doorsneesystematiek",
    "Beleggingsbeleid/Lifecycle",
    "Uitkeringsfase / Collectief Variabel Pensioen",
    "Risicodelingsreserve",
    "Invaren",
    "Bijsparen",
]

# Keywords used to retrieve relevant ontology concepts per theme (deterministic scoring).
THEME_KEYWORDS: dict[str, list[str]] = {
    "Opbouwsystematiek": ["premie", "opbouw", "premiepercentage", "pensioengrondslag",
                          "franchise", "beschikbare", "kapitaal", "grondslag"],
    "Partnerpensioen": ["partnerpensioen", "partner", "nabestaande", "overlijden", "lpp"],
    "Wezenpensioen": ["wees", "wezen", "kind"],
    "Arbeidsongeschiktheid (premievrijstelling)": ["arbeidsongeschikt", "premievrijstelling",
                          "premievrij", "invaliditeit", "voortzetting"],
    "Indexatie/Toeslagen": ["toeslag", "indexatie", "aanpassing", "rendement", "spreiding",
                          "projectierendement"],
    "Compensatie afschaffing doorsneesystematiek": ["compensatie", "doorsnee",
                          "doorsneesystematiek", "depot", "staffel"],
    "Beleggingsbeleid/Lifecycle": ["belegg", "lifecycle", "life cycle", "rebalanc",
                          "risicoprofiel", "units", "beleggingsbalans"],
    "Uitkeringsfase / Collectief Variabel Pensioen": ["uitkering", "collectief variabel",
                          "cvp", "variabele uitkering", "uitkeringsfase"],
    "Risicodelingsreserve": ["risicodelingsreserve", "reserve", "solidariteit", "rdr",
                          "stabiliteit"],
    "Invaren": ["invaren", "invaar", "waardeoverdracht", "standaardmethode", "transitie"],
    "Bijsparen": ["bijspar", "vrijwillig", "extra", "upa", "bijspaarruimte"],
}

_SHEETS = ("PROPERTY", "CLASS", "SUBCLASS")


@dataclass
class Concept:
    name: str
    definition: str
    domain_values: str
    category: str
    text: str  # normalised searchable blob


def _clean(v) -> str:
    if v is None:
        return ""
    s = str(v).strip()
    return "" if s.lower() in ("none", "n/d", "nan") else s


def load_concepts(path: Path) -> list[Concept]:
    """Read Name/Definition/DomainValue/Category from the ontology's main sheets."""
    import openpyxl

    wb = openpyxl.load_workbook(str(path), read_only=True, data_only=True)
    concepts: list[Concept] = []
    for sheet in _SHEETS:
        if sheet not in wb.sheetnames:
            continue
        ws = wb[sheet]
        rows = list(ws.iter_rows(values_only=True))
        if not rows:
            continue
        header = [str(c) if c is not None else "" for c in rows[0]]

        def col(name: str) -> int | None:
            return header.index(name) if name in header else None

        i_name, i_def = col("Name"), col("Definition")
        i_dom, i_cat = col("DomainValue"), col("Category")
        i_clar, i_goal = col("Clarification"), col("Goal")
        for r in rows[1:]:
            name = _clean(r[i_name]) if i_name is not None and i_name < len(r) else ""
            if not name:
                continue
            definition = _clean(r[i_def]) if i_def is not None and i_def < len(r) else ""
            clar = _clean(r[i_clar]) if i_clar is not None and i_clar < len(r) else ""
            goal = _clean(r[i_goal]) if i_goal is not None and i_goal < len(r) else ""
            dom = _clean(r[i_dom]) if i_dom is not None and i_dom < len(r) else ""
            cat = _clean(r[i_cat]) if i_cat is not None and i_cat < len(r) else ""
            definition = " ".join(x for x in (definition, clar, goal) if x)
            blob = " ".join((name, definition, dom, cat)).lower()
            concepts.append(Concept(name=name, definition=definition, domain_values=dom,
                                    category=cat, text=blob))
    wb.close()
    return concepts


def _render(c: Concept, max_def: int | None = None) -> str:
    definition = c.definition
    if max_def is not None and len(definition) > max_def:
        definition = definition[:max_def].rstrip() + "…"
    parts = [c.name.replace("_", " ")]
    if definition:
        parts.append(f": {definition}")
    if c.domain_values:
        parts.append(f" [waarden: {c.domain_values}]")
    if c.category:
        parts.append(f" (categorie: {c.category})")
    return "".join(parts)


def full_text(concepts: list[Concept], max_chars: int) -> str:
    """Complete rendering used as the verification corpus for ontology citations."""
    out: list[str] = []
    total = 0
    for c in concepts:
        line = "• " + _render(c)
        out.append(line)
        total += len(line)
        if total >= max_chars:
            out.append("[... ontology afgekapt voor lengte ...]")
            break
    return "\n".join(out)


def retrieve(concepts: list[Concept], per_theme: int = 8, max_def: int = 300) -> str:
    """Deterministic per-theme retrieval block for the prompt.

    For each canonical theme, score concepts by keyword hits and keep the top matches.
    Ties are broken by name so the output is byte-stable across runs. Definitions are capped
    for the prompt (the full text stays in the verification index, so quotes still verify).
    """
    blocks: list[str] = []
    for theme in CANONICAL_THEMES:
        kws = THEME_KEYWORDS.get(theme, [])
        scored: list[tuple[int, str, Concept]] = []
        for c in concepts:
            score = sum(c.text.count(kw) for kw in kws)
            if score > 0:
                scored.append((score, c.name, c))
        # Highest score first; deterministic tie-break on name.
        scored.sort(key=lambda t: (-t[0], t[1]))
        top = scored[:per_theme]
        if not top:
            continue
        lines = "\n".join("  • " + _render(c, max_def=max_def) for _, _, c in top)
        blocks.append(f"## Thema: {theme}\n{lines}")
    return "\n\n".join(blocks)


def keyword_pattern() -> re.Pattern:
    """(unused placeholder kept for future tooling)"""
    return re.compile("")
