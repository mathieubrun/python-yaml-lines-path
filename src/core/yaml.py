from typing import Any, Dict, List

from ruamel.yaml import YAML, CommentedMap, CommentedSeq

type YamlData = str
type YamlPath = str
type YamlPathParts = List[str]


class YamlLinesParser:
    def __init__(self, data: YamlData):
        yaml = YAML()
        self._yaml = yaml.load(data)
        self._line_map: Dict[int, YamlPathParts] = {}
        self._populate_line_map(self._yaml)

    def _populate_line_map(self, data: object, current_path: YamlPathParts | None = None) -> None:
        path = current_path or []
        match data:
            case CommentedMap():
                for key, value in data.items():
                    new_path = path + [key]
                    line = data.lc.key(key)[0] + 1
                    self._line_map[line] = new_path
                    self._populate_line_map(value, new_path)
            case CommentedSeq():
                for i, item in enumerate(data):
                    new_path = path + [str(i)]
                    line = data.lc.data[i][0] + 1
                    self._line_map[line] = new_path
                    self._populate_line_map(item, new_path)

    def parse(self, line: int) -> YamlPath:
        return ".".join(self._line_map.get(line, []))


class YamlPathEvaluator:
    def __init__(self, data: object):
        self._data = data

    def evaluate(self, path: YamlPath) -> Any:
        if not path:
            return self._data

        parts = path.split(".")

        current_obj = self._data
        for part in parts:
            match current_obj:
                case dict():
                    current_obj = current_obj[part]
                case list():
                    current_obj = current_obj[int(part)]
                case _:
                    raise TypeError(f"Cannot access part '{part}' in path '{path}' on a scalar value.")
        return current_obj


class LineMapper:
    def __init__(self, parser: YamlLinesParser, evaluator: YamlPathEvaluator):
        pass
