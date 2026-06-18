#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

calendar_url="${LUMA_CALENDAR_URL:-https://luma.com/mln}"
commit=false
push=false

usage() {
  cat <<'USAGE'
Usage: bin/update_mln_from_luma.sh [--commit] [--push]

Fetches the MLn Luma calendar, appends any unseen events to _data/mln.yml,
and creates the matching _pages/mln_weekN.md stubs.

Options:
  --commit   Commit MLn sync changes if any were made.
  --push     Commit changes if needed, then push the current branch.

Environment:
  LUMA_CALENDAR_URL  Calendar URL to sync from. Default: https://luma.com/mln
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --commit)
      commit=true
      ;;
    --push)
      commit=true
      push=true
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
  shift
done

for cmd in curl python3 git; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "Missing required command: $cmd" >&2
    exit 1
  fi
done

tmp_dir="$(mktemp -d)"
trap 'rm -rf "$tmp_dir"' EXIT

calendar_html="$tmp_dir/calendar.html"
curl -fsSL "$calendar_url" -o "$calendar_html"

python3 - "$calendar_html" <<'PY'
import datetime as dt
import html
import json
import re
import sys
import textwrap
import urllib.request
from pathlib import Path

calendar_html_path = Path(sys.argv[1])
data_path = Path("_data/mln.yml")
page_dir = Path("_pages")
today = dt.date.today()


def next_data_from_html(raw_html, label):
    match = re.search(
        r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>',
        raw_html,
        re.S,
    )
    if not match:
        raise RuntimeError(f"Could not find __NEXT_DATA__ in {label}")
    return json.loads(html.unescape(match.group(1)))


def fetch_text(url):
    req = urllib.request.Request(url, headers={"User-Agent": "mln-luma-sync/1.0"})
    with urllib.request.urlopen(req, timeout=30) as response:
        return response.read().decode("utf-8")


def flatten_text(node, links):
    if not node:
        return ""

    node_type = node.get("type")
    if node_type == "text":
        text = node.get("text", "")
        for mark in node.get("marks", []):
            if mark.get("type") == "link":
                url = mark.get("attrs", {}).get("href", "")
                if text.strip() and url:
                    links.append({"title": text.strip(), "url": url})
        return text

    if node_type == "hard_break":
        return "\n"

    return "".join(flatten_text(child, links) for child in node.get("content", []))


def text_blocks(doc, links):
    blocks = []
    for node in (doc or {}).get("content", []):
        if node.get("type") == "blockquote":
            blocks.extend(text_blocks(node, links))
            continue
        if node.get("type") == "horizontal_rule":
            continue

        text = re.sub(r"[ \t]+", " ", flatten_text(node, links)).strip()
        if text:
            blocks.append(text)
    return blocks


def yaml_scalar(value):
    return json.dumps(str(value), ensure_ascii=False)


def wrapped_lines(text, width=76):
    return textwrap.wrap(str(text), width=width, break_long_words=False) or [""]


def week_title(raw_name, num):
    return re.sub(
        rf"^MLn Club \(ML Reading Group\) #{num}:\s*",
        "",
        raw_name,
        flags=re.I,
    ).strip()


def event_status(start_at):
    event_date = dt.datetime.fromisoformat(start_at.replace("Z", "+00:00")).date()
    return "past" if event_date < today else "upcoming"


def useful_reading_links(links):
    seen = set()
    useful = []
    skipped_hosts = ("forms.gle/", "czhs.github.io/mln", "cmuaisafety.com")

    for link in links:
        url = re.sub(r"\?utm_source=luma$", "", link["url"])
        title = link["title"].strip()
        if not url or not title or any(host in url for host in skipped_hosts):
            continue
        if url in seen:
            continue
        seen.add(url)
        useful.append({"title": title, "url": url})

    return useful


data_text = data_path.read_text()
existing_slugs = set(re.findall(r'^\s+slug:\s+"([^"]+)"', data_text, re.M))
week_nums = [int(num) for num in re.findall(r"^\s+- num:\s+(\d+)", data_text, re.M)]
next_num = max(week_nums) + 1

calendar = next_data_from_html(calendar_html_path.read_text(), calendar_html_path)
items = (
    calendar.get("props", {})
    .get("pageProps", {})
    .get("initialData", {})
    .get("data", {})
    .get("featured_items", [])
)
new_events = [
    item["event"]
    for item in items
    if item.get("event") and item["event"].get("url") not in existing_slugs
]
new_events.sort(key=lambda event: event.get("start_at", ""))

if not new_events:
    print("No new MLn Luma events found.")
    raise SystemExit(0)

with data_path.open("a") as data_file:
    for event in new_events:
        slug = event["url"]
        event_html = fetch_text(f"https://luma.com/{slug}")
        details = (
            next_data_from_html(event_html, slug)
            .get("props", {})
            .get("pageProps", {})
            .get("initialData", {})
            .get("data", {})
        )
        event_data = details["event"]
        links = []
        blocks = text_blocks(details.get("description_mirror"), links)

        num = next_num
        next_num += 1
        title = week_title(event_data["name"], num)
        questions = []
        for line in blocks[1:]:
            if not line.endswith("?"):
                break
            questions.append(line)
        summary = questions[0] if questions else (blocks[1] if len(blocks) > 1 else title)
        description_parts = [
            line
            for line in blocks
            if not line.startswith(f"Week {num}:")
            and not line.startswith("Reading Recommendations, Questions, or Comments?")
        ]
        description = " ".join(description_parts)
        reading = useful_reading_links(links)

        data_file.write(f"  - num: {num}\n")
        data_file.write(f"    slug: {yaml_scalar(slug)}\n")
        data_file.write(f"    evt: {yaml_scalar(event_data['api_id'])}\n")
        data_file.write(f"    status: {event_status(event_data['start_at'])}\n")
        data_file.write(f"    title: {yaml_scalar(title)}\n")
        data_file.write(f"    cover: {yaml_scalar(event_data['cover_url'])}\n")
        data_file.write(f"    summary: {yaml_scalar(summary)}\n")
        data_file.write("    description: >-\n")
        for line in wrapped_lines(description):
            data_file.write(f"      {line}\n")
        data_file.write("    reading:\n")
        if not reading:
            data_file.write(f"      - title: {yaml_scalar(title)}\n")
            data_file.write(f"        url: {yaml_scalar(f'https://luma.com/{slug}')}\n")
        else:
            for link in reading:
                data_file.write(f"      - title: {yaml_scalar(link['title'])}\n")
                data_file.write(f"        url: {yaml_scalar(link['url'])}\n")

        page_path = page_dir / f"mln_week{num}.md"
        page_path.write_text(
            f"---\n"
            f"layout: mln\n"
            f"permalink: /mln/week-{num}/\n"
            f"week: {num}\n"
            f"standalone_title: \"Week {num} · {title} — MLn Reading Club\"\n"
            f"---\n"
        )

        print(f"Added MLn week {num}: {title}")
PY

if git diff --quiet -- _data/mln.yml _pages/mln_week*.md; then
  changed=false
else
  changed=true
fi

if [[ "$commit" == true && "$changed" == true ]]; then
  git add _data/mln.yml _pages/mln_week*.md bin/update_mln_from_luma.sh
  git commit -m "Update MLn events from Luma"
fi

if [[ "$push" == true ]]; then
  git push
fi
