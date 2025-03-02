def test_simple() -> None:
    """A simple test that should always pass."""
    assert 1 + 1 == 2
    print("This test passed!")


def test_simple_fail() -> None:
    """A simple test that should always fail."""
    print("This test will fail!")
    assert 1 + 1 == 3
