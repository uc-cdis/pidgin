import pytest
from pidgin.app import *

def test_translate_dict_to_json():
    input = {"key1": "value1", "key2": "value2", "key3": {"key4": "value4"}}
    output = translate_dict_to_json(input)
    expected = '{"key1": "value1", "key2": "value2", "key3": {"key4": "value4"}}'
    assert output == expected

def test_translate_dict_to_bibtex():
    input = {"object_id": "object_id_test", "key2": "value2", "key3": "value3"}
    output = translate_dict_to_bibtex(input)
    expected = '@misc {object_id_test, object_id = "object_id_test", key2 = "value2", key3 = "value3", }'
    assert output == expected

def test_flatten_dict():
    input = {"data": {"data_type_test": [{"core_metadata_collections": [{"creator": "creator_test", "description": "description_test"}], "file_name_test": "file_name", "object_id": "object_id_test"}]}}
    output = flatten_dict(input)
    expected = {"creator": "creator_test", "description": "description_test", "file_name_test": "file_name", "object_id": "object_id_test"}
    assert output == expected

def test_flatten_dict_raises_exception():
    input = {"data": "null", "errors": ["Cannot query field \"core_metadata_collections\" on type \"data_type_test\"." ]}
    with pytest.raises(Exception):
        flatten_dict(input)
