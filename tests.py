import pytest
from hypothesis import given, settings, Verbosity
import hypothesis.strategies as st
from sf_id_convertor import sf18_from_15, SfId15, SfId18


@pytest.mark.parametrize('sf_id, expected', [
    ("0012A00001aaAaa", "0012A00001aaAaaQAE"),
    ("0012000001A10aA", "0012000001A10aAAAR"),
    ("a0D30000001n7Pi", "a0D30000001n7PiEAI"),
    ("0012000001A1AA0", "0012000001A1AA0AAN"),
    ("0012000001AAaa1", "0012000001AAaa1AAD")
    ])
def test_basic_id_correct(sf_id, expected):
    assert sf18_from_15(SfId15(sf_id)) == SfId18(expected)


@settings(verbosity=Verbosity.verbose)
@given(st.text(
    st.characters(whitelist_categories=("Lu", "Ll", "Nd")),
    min_size=15,
    max_size=15))
def test_18_char_id_returned(sf_id):
    result = sf18_from_15(SfId15(sf_id))
    assert len(result) == 18


@settings(verbosity=Verbosity.verbose)
@given(st.text(
    st.characters(blacklist_categories=("Lu", "Ll", "Nd")),
    min_size=15,
    max_size=15))
def test_none_returned_with_non_alnum_input(sf_id):
    assert sf18_from_15(SfId15(sf_id)) is None


@settings(verbosity=Verbosity.verbose)
@given(st.text(
    st.characters(whitelist_categories=("Lu", "Ll", "Nd")),
    min_size=0,
    max_size=14))
def test_none_returned_with_short_length_input(sf_id):
    assert sf18_from_15(SfId15(sf_id)) is None


@settings(verbosity=Verbosity.verbose)
@given(st.text(
    st.characters(whitelist_categories=("Lu", "Ll", "Nd")),
    min_size=16,
    max_size=1024))
def test_none_returned_with_long_length_input(sf_id):
    assert sf18_from_15(SfId15(sf_id)) is None
