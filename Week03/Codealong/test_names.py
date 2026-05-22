from names import make_full_name, extract_family_name , extract_given_name
import pytest

def test_make_full_name():
    assert make_full_name("Sally", "Brown") == "Brown; Sally"


def test_extract_family_name():
    assert extract_family_name("Brown; Sally") == "Brown"

def test_extract_given_name():
    assert extract_given_name("Brown; Sally") == "Sally"


pytest.main(["-v", "--tb=line", "-rN", __file__])