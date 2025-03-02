import argparse
import sys
import urllib.error
import urllib.request
from typing import cast


def fetch_html(url: str) -> str:
    """
    Fetch HTML source code from a given URL.

    Args:
        url (str): The URL to fetch HTML from.

    Returns:
        str: The HTML source code as a string.

    Raises:
        urllib.error.URLError: If there's an error fetching the URL.
        urllib.error.HTTPError: If there's an HTTP error.
    """
    try:
        with urllib.request.urlopen(url) as response:
            html_bytes = response.read()
            html = cast(str, html_bytes.decode('utf-8'))
            return html
    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        print(f"Error fetching URL {url}: {e}")
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch HTML from a URL")
    parser.add_argument("url", help="URL to fetch HTML from")
    parser.add_argument("-o", "--output", help="Output file (default: stdout)")
    args = parser.parse_args()

    try:
        html = fetch_html(args.url)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(html)
            print(f"HTML saved to {args.output}")
        else:
            print(html)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
