import pytest
from ruamel.yaml import YAML

from core.yaml import YamlPathEvaluator

yaml_data = YAML().load("""
root:
  key_a: value_a
  key_b: value_b
  list:
    - list_value_0
    - list_value_1
    - nested_object:
        nested_key: nested_value
""")


class TestYamlPathEvaluator:
    @pytest.mark.parametrize(
        "path_parts, expected_result",
        [
            pytest.param("", yaml_data, id="no path"),
            pytest.param("root", yaml_data["root"]),
            pytest.param("root.key_a", "value_a"),
            pytest.param("root.list", yaml_data["root"]["list"]),
            pytest.param("root.list.0", yaml_data["root"]["list"][0]),
            pytest.param("root.list.2", yaml_data["root"]["list"][2]),
            pytest.param("root.list.2.nested_object", yaml_data["root"]["list"][2]["nested_object"]),
            pytest.param("root.list.2.nested_object.nested_key", yaml_data["root"]["list"][2]["nested_object"]["nested_key"]),
        ],
    )
    def test_evaluate_successful(self, path_parts, expected_result):
        # arrange
        # act
        evaluator = YamlPathEvaluator(yaml_data)

        # assert
        assert evaluator.evaluate(path_parts) == expected_result

    @pytest.mark.parametrize(
        "path_parts, exception, match_str",
        [
            ("root.non_existent_key", KeyError, "non_existent_key"),
            ("root.list.99", IndexError, "list index out of range"),
            ("root.key_a.sub_key", TypeError, "Cannot access part 'sub_key'"),
        ],
    )
    def test_evaluate_errors(self, path_parts, exception, match_str):
        # arrange
        evaluator = YamlPathEvaluator(yaml_data)

        # act
        # assert
        with pytest.raises(exception, match=match_str):
            evaluator.evaluate(path_parts)
