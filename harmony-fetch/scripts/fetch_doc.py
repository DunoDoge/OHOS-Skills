#!/usr/bin/env python3
"""
Fetch HarmonyOS developer documentation from Huawei developer portal.

Usage:
    python3 fetch_doc.py <objectId> [--html] [--lang cn|en|ru]
    python3 fetch_doc.py --catalog <catalogName> [--lang cn|en|ru] [--flat]

Examples:
    # Fetch a specific document (markdown output)
    python3 fetch_doc.py arkts-state-management-overview

    # Fetch raw HTML
    python3 fetch_doc.py arkts-state-management-overview --html

    # Browse catalog tree
    python3 fetch_doc.py --catalog harmonyos-guides

    # Browse catalog in flat mode (list all leaf documents)
    python3 fetch_doc.py --catalog harmonyos-guides --flat
"""

import json
import sys
import urllib.request
import urllib.error
from html.parser import HTMLParser
from io import StringIO
import re

API_BASE = "https://developer.huawei.com/consumer/{lang}/documentPortal"
CATALOG_API = API_BASE + "/getCatalogTree"
DOC_API = API_BASE + "/getDocumentById"


def fetch_catalog(catalog_name: str, lang: str = "cn") -> dict:
    """Fetch catalog tree from API."""
    url = CATALOG_API.format(lang=lang)
    payload = json.dumps({
        "catalogName": catalog_name,
        "language": lang,
        "showHide": 0
    }).encode("utf-8")
    req = urllib.request.Request(
        url, data=payload,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_document(object_id: str, lang: str = "cn") -> dict:
    """Fetch document content from API."""
    url = DOC_API.format(lang=lang)
    payload = json.dumps({
        "language": lang,
        "objectId": object_id
    }).encode("utf-8")
    req = urllib.request.Request(
        url, data=payload,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def print_catalog_tree(nodes: list, indent: int = 0, flat: bool = False, max_depth: int = 10):
    """Print catalog tree in a readable format."""
    if indent > max_depth:
        return
    for node in nodes:
        name = node.get("nodeName", "")
        slug = node.get("relateDocument", "")
        is_leaf = node.get("isLeaf", False)
        children = node.get("children", [])
        prefix = "  " * indent

        if is_leaf or flat:
            slug_info = f" [{slug}]" if slug else ""
            marker = "  " if is_leaf else ""
            print(f"{prefix}{marker}{name}{slug_info}")
        else:
            print(f"{prefix}{name}/")

        if children:
            if flat and not is_leaf:
                print_catalog_tree(children, indent + 1, flat=True, max_depth=max_depth)
            elif not flat:
                print_catalog_tree(children, indent + 1, flat=False, max_depth=max_depth)


class HTMLToMarkdown(HTMLParser):
    """Simple HTML to Markdown converter for Huawei doc content."""

    def __init__(self):
        super().__init__()
        self.output = StringIO()
        self.tag_stack = []
        self.in_code_block = False
        self.code_lang = ""
        self.in_table = False
        self.table_rows = []
        self.current_row = []
        self.current_cell = ""
        self.in_cell = False
        self.in_heading = False
        self.heading_level = 0
        self.list_depth = 0
        self.in_list_item = False
        self.skip_tags = {"head", "meta", "link", "style", "script"}
        self.skip_depth = 0
        self.in_pre = False

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        attrs_dict = dict(attrs)

        if tag in self.skip_tags:
            self.skip_depth += 1
            return

        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            level = int(tag[1])
            self.in_heading = True
            self.heading_level = level
            self.output.write(f"\n{'#' * level} ")

        elif tag == "p":
            self.output.write("\n")

        elif tag == "br":
            self.output.write("\n")

        elif tag in ("strong", "b"):
            self.output.write("**")

        elif tag in ("em", "i"):
            self.output.write("*")

        elif tag == "code":
            if not self.in_pre:
                self.output.write("`")

        elif tag == "pre":
            self.in_pre = True
            # Try to detect language from class
            cls = attrs_dict.get("class", "")
            lang_match = re.search(r'language-(\w+)', cls)
            self.code_lang = lang_match.group(1) if lang_match else ""
            self.output.write(f"\n```{self.code_lang}\n")

        elif tag == "a":
            href = attrs_dict.get("href", "")
            if href and not href.startswith("#"):
                self.output.write("[")
            self.tag_stack.append(("a", href))

        elif tag == "img":
            src = attrs_dict.get("src", "")
            alt = attrs_dict.get("alt", "")
            if src:
                self.output.write(f"\n![{alt}]({src})\n")

        elif tag in ("ul", "ol"):
            self.list_depth += 1
            self.output.write("\n")

        elif tag == "li":
            indent = "  " * (self.list_depth - 1)
            self.in_list_item = True
            self.output.write(f"{indent}- ")

        elif tag == "table":
            self.in_table = True
            self.table_rows = []

        elif tag == "tr":
            self.current_row = []

        elif tag in ("td", "th"):
            self.in_cell = True
            self.current_cell = ""

        elif tag == "div":
            cls = attrs_dict.get("class", "")
            if "note" in cls.lower() or "tip" in cls.lower() or "warning" in cls.lower():
                self.output.write("\n> ")

    def handle_endtag(self, tag):
        tag = tag.lower()

        if tag in self.skip_tags:
            self.skip_depth = max(0, self.skip_depth - 1)
            return

        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.in_heading = False
            self.output.write("\n")

        elif tag in ("strong", "b"):
            self.output.write("**")

        elif tag in ("em", "i"):
            self.output.write("*")

        elif tag == "code":
            if not self.in_pre:
                self.output.write("`")

        elif tag == "pre":
            self.in_pre = False
            self.output.write("\n```\n")

        elif tag == "a":
            if self.tag_stack:
                popped = self.tag_stack.pop()
                if popped[0] == "a" and popped[1] and not popped[1].startswith("#"):
                    self.output.write(f"]({popped[1]})")

        elif tag == "li":
            self.in_list_item = False
            self.output.write("\n")

        elif tag in ("ul", "ol"):
            self.list_depth = max(0, self.list_depth - 1)
            if self.list_depth == 0:
                self.output.write("\n")

        elif tag in ("td", "th"):
            self.in_cell = False
            self.current_row.append(self.current_cell.strip())
            self.current_cell = ""

        elif tag == "tr":
            self.table_rows.append(self.current_row)

        elif tag == "table":
            self.in_table = False
            self._render_table()

        elif tag == "p":
            self.output.write("\n")

    def handle_data(self, data):
        if self.skip_depth > 0:
            return
        if self.in_cell:
            self.current_cell += data
        elif self.in_pre:
            self.output.write(data)
        else:
            self.output.write(data)

    def _render_table(self):
        if not self.table_rows:
            return
        # Calculate column widths
        max_cols = max(len(row) for row in self.table_rows)
        for row in self.table_rows:
            while len(row) < max_cols:
                row.append("")

        self.output.write("\n")
        # Header row
        self.output.write("| " + " | ".join(self.table_rows[0]) + " |\n")
        self.output.write("| " + " | ".join(["---"] * max_cols) + " |\n")
        # Data rows
        for row in self.table_rows[1:]:
            self.output.write("| " + " | ".join(row) + " |\n")
        self.output.write("\n")

    def get_markdown(self) -> str:
        text = self.output.getvalue()
        # Clean up excessive newlines
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()


def html_to_markdown(html: str) -> str:
    """Convert HTML content to Markdown."""
    parser = HTMLToMarkdown()
    parser.feed(html)
    return parser.get_markdown()


def parse_url_to_slug(url: str) -> tuple:
    """
    Parse a Huawei developer doc URL to extract catalog and slug.

    Returns: (catalog_name, object_id)
    """
    # Pattern: /consumer/{lang}/doc/{catalog}[-V{n}]/{slug}[-V{n}]
    match = re.search(r'/doc/([a-z0-9-]+?)(?:-V\d+)?/([a-z0-9_-]+?)(?:-V\d+)?$', url)
    if match:
        return match.group(1), match.group(2)
    # Try without version suffix
    match = re.search(r'/doc/([a-z0-9-]+)/([a-z0-9_-]+)$', url)
    if match:
        return match.group(1), match.group(2)
    return None, None


def main():
    import argparse

    # Fix Windows terminal encoding (GBK cannot handle CJK + special chars like U+200C)
    if sys.platform == 'win32':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
            sys.stderr.reconfigure(encoding='utf-8')
        except Exception:
            pass

    parser = argparse.ArgumentParser(description="Fetch HarmonyOS developer documentation")
    parser.add_argument("object_id", nargs="?", help="Document slug (objectId)")
    parser.add_argument("--html", action="store_true", help="Output raw HTML instead of markdown")
    parser.add_argument("--lang", default="cn", choices=["cn", "en", "ru"], help="Language (default: cn)")
    parser.add_argument("--catalog", help="Browse catalog tree instead of fetching a document")
    parser.add_argument("--flat", action="store_true", help="List all leaf documents in flat mode")
    parser.add_argument("--url", help="Parse a Huawei doc URL and fetch the document")
    parser.add_argument("--json", action="store_true", help="Output raw JSON response")

    args = parser.parse_args()

    # Browse catalog mode
    if args.catalog:
        try:
            result = fetch_catalog(args.catalog, args.lang)
            if result.get("code") != 0:
                print(f"Error: {result.get('message', 'Unknown error')}", file=sys.stderr)
                sys.exit(1)

            nodes = result.get("value", {}).get("catalogTreeList", [])
            if args.json:
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                print(f"Catalog: {args.catalog} ({len(nodes)} top-level sections)\n")
                print_catalog_tree(nodes, flat=args.flat)
        except urllib.error.URLError as e:
            print(f"Network error: {e}", file=sys.stderr)
            sys.exit(1)
        return

    # URL parsing mode
    if args.url:
        catalog, slug = parse_url_to_slug(args.url)
        if not slug:
            print(f"Error: Could not parse URL: {args.url}", file=sys.stderr)
            sys.exit(1)
        args.object_id = slug
        print(f"Parsed URL: catalog={catalog}, objectId={slug}\n")

    # Document fetch mode
    if not args.object_id:
        parser.print_help()
        sys.exit(1)

    try:
        result = fetch_document(args.object_id, args.lang)
        if result.get("code") != 0:
            print(f"Error: {result.get('message', 'Unknown error')}", file=sys.stderr)
            sys.exit(1)

        value = result.get("value", {})
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return

        title = value.get("title", "Untitled")
        version = value.get("version", "")
        content_html = value.get("content", {}).get("content", "")

        if args.html:
            print(content_html)
        else:
            print(f"# {title}\n")
            if version:
                print(f"*Version: {version}*\n")
            markdown = html_to_markdown(content_html)
            print(markdown)

    except urllib.error.URLError as e:
        print(f"Network error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
