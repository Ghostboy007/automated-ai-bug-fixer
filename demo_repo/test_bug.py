import pytest
from calculator import divide


def test_division_by_zero():
    with pytest.raises(ValueError):
        divide(10, 0)