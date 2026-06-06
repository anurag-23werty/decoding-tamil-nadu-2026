"""
Scrape total votes polled for each Tamil Nadu Assembly constituency from ECI.

The ECI result pages for May 2026 expose constituency pages like:
https://results.eci.gov.in/ResultAcGenMay2026/ConstituencywiseS2252.htm

This script prefers direct HTTP requests over Selenium because the data is
already present in the HTML. It also discovers constituency URLs from the
Tamil Nadu state page, then falls back to AC numbers 1..234 if discovery fails.
"""

from __future__ import annotations

import argparse
import csv
import random
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


DEFAULT_BASE = "https://results.eci.gov.in/ResultAcGenMay2026/"
STATE_CODE = "S22"
STATEWISE_PAGE = f"statewise{STATE_CODE}2.htm"
TOTAL_ACS = 234


@dataclass(frozen=True)
class ConstituencyUrl:
    ac_no: int
    url: str


@dataclass
class ConstituencyResult:
    constituency_no: int
    constituency_name: str | None
    evm_votes: int | None
    postal_votes: int | None
    total_votes_polled: int | None
    status: str | None
    last_updated: str | None
    source_url: str
    error: str | None = None


def clean_text(value: str) -> str:
    return " ".join(value.replace("\xa0", " ").split())


def to_int(value: str) -> int | None:
    digits = re.sub(r"[^\d]", "", value)
    return int(digits) if digits else None


def new_session() -> requests.Session:
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/137.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
        }
    )
    return session


def fetch(session: requests.Session, url: str, retries: int = 3, timeout: int = 30) -> str:
    last_error: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            response = session.get(url, timeout=timeout)
            response.raise_for_status()
            return response.text
        except requests.RequestException as exc:
            last_error = exc
            if attempt < retries:
                time.sleep(2 * attempt)
    raise RuntimeError(f"Could not fetch {url}: {last_error}")


class SeleniumFetcher:
    def __init__(self, headful: bool = False) -> None:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options

        options = Options()
        if not headful:
            options.add_argument("--headless=new")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--start-maximized")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/137.0.0.0 Safari/537.36"
        )
        self.driver = webdriver.Chrome(options=options)

    def fetch(self, url: str) -> str:
        self.driver.get(url)
        time.sleep(2)
        return self.driver.page_source

    def close(self) -> None:
        self.driver.quit()


def discover_constituency_urls(
    fetch_html: Callable[[str], str],
    base_url: str,
    no_discover: bool = False,
) -> list[ConstituencyUrl]:
    if no_discover:
        return fallback_constituency_urls(base_url)

    state_url = urljoin(base_url, STATEWISE_PAGE)
    html = fetch_html(state_url)
    soup = BeautifulSoup(html, "html.parser")
    found: dict[int, str] = {}

    for link in soup.find_all("a", href=True):
        href = link["href"]
        match = re.search(rf"Constituencywise{STATE_CODE}(\d+)\.htm", href)
        if not match:
            continue
        ac_no = int(match.group(1))
        found[ac_no] = urljoin(state_url, href)

    if not found:
        print("Could not discover constituency links; using AC numbers 1..234.", file=sys.stderr)
        return fallback_constituency_urls(base_url)

    return [ConstituencyUrl(ac_no, found[ac_no]) for ac_no in sorted(found)]


def fallback_constituency_urls(base_url: str) -> list[ConstituencyUrl]:
    return [
        ConstituencyUrl(
            ac_no=ac_no,
            url=urljoin(base_url, f"Constituencywise{STATE_CODE}{ac_no}.htm"),
        )
        for ac_no in range(1, TOTAL_ACS + 1)
    ]


def extract_heading(soup: BeautifulSoup) -> tuple[int | None, str | None]:
    heading = soup.find(["h1", "h2", "h3"], string=re.compile("Assembly Constituency"))
    if not heading:
        text = clean_text(soup.get_text(" "))
        match = re.search(r"Assembly Constituency\s+(\d+)\s*-\s*(.+?)\s*\(Tamil Nadu\)", text)
    else:
        match = re.search(
            r"Assembly Constituency\s+(\d+)\s*-\s*(.+?)\s*\(Tamil Nadu\)",
            clean_text(heading.get_text(" ")),
        )

    if not match:
        return None, None

    return int(match.group(1)), clean_text(match.group(2))


def extract_status_and_update(soup: BeautifulSoup) -> tuple[str | None, str | None]:
    text = clean_text(soup.get_text(" "))
    status_match = re.search(r"(Status of EVM Round:\s*\d+\s*/\s*\d+)", text)
    updated_match = re.search(r"(Last Updated at\s+.+?$)", text)
    return (
        clean_text(status_match.group(1)) if status_match else None,
        clean_text(updated_match.group(1)) if updated_match else None,
    )


def parse_total_row(soup: BeautifulSoup) -> tuple[int | None, int | None, int | None]:
    """
    Return (evm_votes, postal_votes, total_votes_polled).

    Candidate rows have seven columns, but the ECI Total row is commonly shorter,
    for example: Total, blank, EVM Votes, Postal Votes, Total Votes.
    """
    for row in soup.find_all("tr"):
        cells = [clean_text(cell.get_text(" ")) for cell in row.find_all(["td", "th"])]
        if not cells:
            continue

        if any(cell.lower() == "total" for cell in cells):
            numbers = [to_int(cell) for cell in cells]
            numbers = [number for number in numbers if number is not None]
            if len(numbers) >= 3:
                return numbers[-3], numbers[-2], numbers[-1]
            if numbers:
                return None, None, numbers[-1]

    # Fallback for flattened/minified markup.
    text = clean_text(soup.get_text(" "))
    match = re.search(r"\bTotal\b\s+(\d[\d,]*)\s+(\d[\d,]*)\s+(\d[\d,]*)", text)
    if match:
        return tuple(int(part.replace(",", "")) for part in match.groups())  # type: ignore[return-value]

    return None, None, None


def parse_constituency_page(html: str, source_url: str, expected_ac_no: int) -> ConstituencyResult:
    soup = BeautifulSoup(html, "html.parser")
    heading_ac_no, constituency_name = extract_heading(soup)
    status, last_updated = extract_status_and_update(soup)
    evm_votes, postal_votes, total_votes_polled = parse_total_row(soup)

    return ConstituencyResult(
        constituency_no=heading_ac_no or expected_ac_no,
        constituency_name=constituency_name,
        evm_votes=evm_votes,
        postal_votes=postal_votes,
        total_votes_polled=total_votes_polled,
        status=status,
        last_updated=last_updated,
        source_url=source_url,
    )


def scrape(
    fetch_html: Callable[[str], str],
    urls: Iterable[ConstituencyUrl],
    delay_min: float,
    delay_max: float,
) -> list[ConstituencyResult]:
    results: list[ConstituencyResult] = []
    urls = list(urls)

    for index, item in enumerate(urls, start=1):
        print(f"[{index}/{len(urls)}] AC {item.ac_no}: {item.url}")
        try:
            html = fetch_html(item.url)
            result = parse_constituency_page(html, item.url, item.ac_no)
            if result.total_votes_polled is None:
                result.error = "Total row not found"
            print(
                "  -> "
                f"{result.constituency_name or 'Unknown'} | "
                f"total={result.total_votes_polled}"
            )
        except Exception as exc:
            result = ConstituencyResult(
                constituency_no=item.ac_no,
                constituency_name=None,
                evm_votes=None,
                postal_votes=None,
                total_votes_polled=None,
                status=None,
                last_updated=None,
                source_url=item.url,
                error=str(exc),
            )
            print(f"  -> ERROR: {exc}", file=sys.stderr)

        results.append(result)
        if index < len(urls):
            time.sleep(random.uniform(delay_min, delay_max))

    return results


def write_csv(path: Path, rows: list[ConstituencyResult]) -> None:
    fieldnames = [
        "constituency_no",
        "constituency_name",
        "evm_votes",
        "postal_votes",
        "total_votes_polled",
        "status",
        "last_updated",
        "source_url",
        "error",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row.__dict__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scrape Tamil Nadu 2026 constituency total votes from ECI."
    )
    parser.add_argument("--base-url", default=DEFAULT_BASE)
    parser.add_argument("--output", default="tn_2026_votes.csv")
    parser.add_argument("--start", type=int, help="First constituency number to scrape.")
    parser.add_argument("--end", type=int, help="Last constituency number to scrape.")
    parser.add_argument("--limit", type=int, help="Scrape only the first N discovered pages.")
    parser.add_argument("--delay-min", type=float, default=1.0)
    parser.add_argument("--delay-max", type=float, default=3.0)
    parser.add_argument(
        "--engine",
        choices=["auto", "requests", "selenium"],
        default="auto",
        help="Use direct HTTP, Selenium, or try HTTP first and fall back to Selenium on blocks.",
    )
    parser.add_argument(
        "--headful",
        action="store_true",
        help="Show Chrome when using Selenium.",
    )
    parser.add_argument(
        "--no-discover",
        action="store_true",
        help="Skip state page discovery and try ConstituencywiseS22{ac_no}.htm for 1..234.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.delay_min < 0 or args.delay_max < args.delay_min:
        print("Invalid delay range.", file=sys.stderr)
        return 2

    selenium_fetcher: SeleniumFetcher | None = None
    session = new_session()

    def request_fetch(url: str) -> str:
        return fetch(session, url)

    fetch_html: Callable[[str], str] = request_fetch
    try:
        if args.engine == "selenium":
            selenium_fetcher = SeleniumFetcher(headful=args.headful)
            fetch_html = selenium_fetcher.fetch

        try:
            urls = discover_constituency_urls(fetch_html, args.base_url, args.no_discover)
        except RuntimeError as exc:
            if args.engine != "auto":
                raise
            print(f"Direct HTTP failed ({exc}); falling back to Selenium.", file=sys.stderr)
            selenium_fetcher = SeleniumFetcher(headful=args.headful)
            fetch_html = selenium_fetcher.fetch
            urls = discover_constituency_urls(fetch_html, args.base_url, args.no_discover)

        if args.start is not None:
            urls = [item for item in urls if item.ac_no >= args.start]
        if args.end is not None:
            urls = [item for item in urls if item.ac_no <= args.end]
        if args.limit is not None:
            urls = urls[: args.limit]

        results = scrape(fetch_html, urls, args.delay_min, args.delay_max)
        output = Path(args.output)
        write_csv(output, results)
    finally:
        if selenium_fetcher is not None:
            selenium_fetcher.close()

    successful = sum(1 for row in results if row.total_votes_polled is not None)
    failed = len(results) - successful
    print(f"\nSaved: {output.resolve()}")
    print(f"Rows: {len(results)} | Parsed totals: {successful} | Failed: {failed}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
