from urllib.error import URLError

import pytest

from src.fetch import fetch_html


def test_fetch_html_example_site() -> None:
    """Test that fetch_html can retrieve content from example.com."""
    url = "https://example.com"
    html = fetch_html(url)

    # Verify we got a non-empty string
    assert isinstance(html, str)
    assert len(html) > 0

    # Verify the content looks like HTML
    assert "<!doctype html>" in html.lower()
    assert "<html" in html.lower()
    assert "<head" in html.lower()
    assert "<title>Example Domain</title>" in html

    # Verify some expected content
    assert "Example Domain" in html


def test_fetch_html_error_handling() -> None:
    """Test that fetch_html properly handles invalid URLs."""
    with pytest.raises(URLError, match=".*"):
        # This should raise an exception
        fetch_html("https://this-domain-does-not-exist-123456789.com")
