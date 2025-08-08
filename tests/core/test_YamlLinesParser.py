from pytest import mark, param

from core.yaml import YamlLinesParser


class TestYamlLinesParser:
    @mark.parametrize(
        "line, expected_result",
        [
            param(1, "root"),
            param(2, "root.key_a"),
            param(3, "root.key_b"),
        ],
    )
    def test_parse_simple(self, line, expected_result):
        # arrange
        yaml_data = """root:
            key_a: value_a
            key_b: value_b
        """
        sut = YamlLinesParser(yaml_data)

        # act
        key = sut.parse(line)

        # assert
        assert key == expected_result

    @mark.parametrize(
        "line, expected_result",
        [
            param(1, "root"),
            param(2, "root.list"),
            param(3, "root.list.0"),
            param(4, "root.list.1"),
        ],
    )
    def test_parse_list(self, line, expected_result):
        # arrange
        yaml_data = """root:
            list:
                - value_a
                - value_b
        """
        sut = YamlLinesParser(yaml_data)

        # act
        key = sut.parse(line)

        # assert
        assert key == expected_result

    @mark.parametrize(
        "line, expected_result",
        [
            param(1, "root"),
            param(2, "root.list"),
            param(3, "root.list.0.object_a"),
            param(4, "root.list.0.object_a.key_a"),
            param(5, "root.list.0.object_a.key_b"),
            param(6, "root.list.1.object_b"),
            param(7, "root.list.1.object_b.key_c"),
        ],
    )
    def test_parse_list_nested(self, line, expected_result):
        # arrange
        yaml_data = """root:
            list:
                - object_a:
                    key_a: value_a
                    key_b: value_b
                - object_b:
                    key_c: value_d
        """
        sut = YamlLinesParser(yaml_data)

        # act
        key = sut.parse(line)

        # assert
        assert key == expected_result

    @mark.parametrize(
        "line, expected_result",
        [
            param(2, "root"),
            param(3, "root.key_a"),
            param(5, "root.key_b"),
            param(8, "root.objects"),
            param(9, "root.objects.0.object_a"),
            param(10, "root.objects.0.object_a.key_a"),
            param(11, "root.objects.0.object_a.key_b"),
            param(12, "root.objects.0.object_a.children"),
            param(13, "root.objects.0.object_a.children.0"),
            param(15, "root.objects.0.object_a.children.1"),
            param(17, "root.objects.1.object_b"),
            param(18, "root.objects.1.object_b.key_c"),
            param(19, "root.objects.1.object_b.complex_children"),
            param(20, "root.objects.1.object_b.complex_children.0.child_a"),
            param(21, "root.objects.1.object_b.complex_children.0.child_a.key_a"),
            param(23, "root.objects.1.object_b.complex_children.0.child_a.key_b"),
            param(26, "root.objects.1.object_b.complex_children.1.child_b"),
            param(27, "root.objects.1.object_b.complex_children.1.child_b.key_a"),
            param(28, "root.objects.1.object_b.complex_children.1.child_b.key_b"),
        ],
    )
    def test_parse_full(self, line, expected_result):
        # arrange
        yaml_data = """# a comment
            root:
                key_a: value_a # another comment

                key_b: value_b


                objects:
                    - object_a:
                        key_a: value_a
                        key_b: value_b
                        children:
                            - child_a

                            - child_b

                    - object_b:
                        key_c: value_d
                        complex_children:
                            - child_a:
                                key_a: value_a

                                key_b: value_b


                            - child_b:
                                key_a: value_a
                                key_b: value_b
            """

        sut = YamlLinesParser(yaml_data)

        # act
        key = sut.parse(line)

        # assert
        assert key == expected_result
