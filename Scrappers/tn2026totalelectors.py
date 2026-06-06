"""
Scrape total electors for Tamil Nadu constituencies from tnelections2026.in.

Example:
    python3 tnelections_electors_scraper.py
    python3 tnelections_electors_scraper.py --name arcot

Output:
    tn_2026_total_electors.csv
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import quote

import requests


BASE_URL = "https://tnelections2026.in"
CONSTITUENCIES_JS_URL = f"{BASE_URL}/data/constituencies.js"
DEFAULT_OUTPUT = "tn_2026_total_electors.csv"


@dataclass
class ConstituencyElectors:
    constituency_no: int
    constituency_name: str
    slug: str
    district: str
    category: str | None
    total_electors: int
    male_electors: int | None
    female_electors: int | None
    third_gender_electors: int | None
    page_url: str


def slugify_constituency_name(name: str) -> str:
    normalized = unicodedata.normalize("NFKD", name.lower().strip())
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_text).strip("-")
    return slug


def fetch_text(url: str) -> str:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/137.0.0.0 Safari/537.36"
        ),
        "Accept": "text/javascript,application/javascript,text/plain,*/*",
        "Referer": f"{BASE_URL}/constituency?name=arcot",
    }
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    return response.text


def extract_js_array(source: str, variable_name: str) -> list[dict[str, Any]]:
    match = re.search(rf"\bvar\s+{re.escape(variable_name)}\s*=\s*\[", source)
    if not match:
        raise ValueError(f"Could not find JavaScript array: {variable_name}")

    start = match.end() - 1
    depth = 0
    in_string = False
    escape = False

    for index in range(start, len(source)):
        char = source[index]

        if in_string:
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == '"':
                in_string = False
            continue

        if char == '"':
            in_string = True
        elif char == "[":
            depth += 1
        elif char == "]":
            depth -= 1
            if depth == 0:
                array_text = source[start : index + 1]
                return json.loads(array_text)

    raise ValueError(f"Array {variable_name} was not closed")


def load_constituencies() -> list[dict[str, Any]]:
    source = fetch_text(CONSTITUENCIES_JS_URL)
    constituencies = extract_js_array(source, "TN_CONSTITUENCIES_234")
    if len(constituencies) != 234:
        print(f"Warning: expected 234 constituencies, found {len(constituencies)}", file=sys.stderr)
    return constituencies


def to_record(row: dict[str, Any]) -> ConstituencyElectors:
    name = str(row["name"])
    slug = slugify_constituency_name(name)
    third_gender = row.get("thirdGender")
    if third_gender is None and all(key in row for key in ("electors", "male", "female")):
        third_gender = int(row["electors"]) - int(row["male"]) - int(row["female"])

    return ConstituencyElectors(
        constituency_no=int(row["id"]),
        constituency_name=name,
        slug=slug,
        district=str(row.get("district", "")),
        category=row.get("category"),
        total_electors=int(row["electors"]),
        male_electors=int(row["male"]) if row.get("male") is not None else None,
        female_electors=int(row["female"]) if row.get("female") is not None else None,
        third_gender_electors=int(third_gender) if third_gender is not None else None,
        page_url=f"{BASE_URL}/constituency?name={quote(slug)}",
    )


def write_csv(path: Path, records: list[ConstituencyElectors]) -> None:
    fields = [
        "constituency_no",
        "constituency_name",
        "slug",
        "district",
        "category",
        "total_electors",
        "male_electors",
        "female_electors",
        "third_gender_electors",
        "page_url",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for record in records:
            writer.writerow(record.__dict__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scrape constituency-wise total electors from tnelections2026.in."
    )
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--name",
        help="Optional constituency slug/name filter, for example: arcot",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    wanted_slug = slugify_constituency_name(args.name) if args.name else None

    rows = load_constituencies()
    records = [to_record(row) for row in rows]
    if wanted_slug:
        records = [
            record
            for record in records
            if record.slug == wanted_slug
            or slugify_constituency_name(record.constituency_name) == wanted_slug
        ]

    if not records:
        print(f"No constituency matched: {args.name}", file=sys.stderr)
        return 1

    output = Path(args.output)
    write_csv(output, records)

    for record in records:
        print(
            f"{record.constituency_no:03d} "
            f"{record.constituency_name}: "
            f"{record.total_electors:,} electors"
        )

    print(f"\nSaved: {output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
