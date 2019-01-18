import pytest

from ...parse_utils import Result, retrieve_data, retrieve_int


def test_retrieve_data_well_formed():
    raw_data = ["this", "is", "a", "test", "Add", "there", "should", "be", "two", "chunked",
                "segments", "Add"]
    result1 = ["this", "is", "a", "test"]
    result2 = ["there", "should", "be", "two", "chunked", "segments"]
    data_chunks = list(retrieve_data(raw_data))
    assert len(data_chunks) == 2
    assert data_chunks[0] == result1
    assert data_chunks[1] == result2


def test_retrieve_data_poorly_formed():
    raw_data = ["this", "is", "a", "test", "Add", "there", "should", "be", "two", "chunked",
                "segments", "Add", "This", "should", "not", "be", "considered", "valid"]
    result1 = ["this", "is", "a", "test"]
    result2 = ["there", "should", "be", "two", "chunked", "segments"]
    data_chunks = list(retrieve_data(raw_data))
    assert len(data_chunks) == 2
    assert data_chunks[0] == result1
    assert data_chunks[1] == result2


def test_parser_retrieve_int_well_formed():
    result = retrieve_int("2")
    assert result.iterate == 1
    assert not result.tuple
    assert result.value == 2


def test_parser_retrieve_int_poorly_formed():
    with pytest.raises(ValueError) as excinfo:
        result = retrieve_int("2.3")
        assert "Not a valid int string!" in excinfo.value
    with pytest.raises(ValueError) as excinfo:
        result = retrieve_int(" 500 W")
        assert "Not a valid int string!" in excinfo.value


def test_parser_retrieve_int_none():
    result = retrieve_int(None)
    assert isinstance(result, Result)
    assert not result.value
    assert result.iterate == 0
    assert not result.tuple
