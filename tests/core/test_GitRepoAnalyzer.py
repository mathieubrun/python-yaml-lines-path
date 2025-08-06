import pytest

from core.repository import ChangedLine, FileChangeType, LineChangeType, RepoAnalyzer


class TestGitRepoAnalyzer:
    def test_get_changed_files(self, sut: RepoAnalyzer):
        # arrange
        diff_output = [
            "A\tdata/test.yaml",
        ]

        # act
        changed_files = sut._get_changed_files(diff_output)

        # assert
        assert changed_files[0].path == "data/test.yaml"
        assert changed_files[0].type == FileChangeType.ADDED

    def test_get_file_diff_1(self, sut: RepoAnalyzer):
        # arrange
        lines = [
            "@@ -7 +6,0 @@ root:",
            "-            key_a: value_a",
            "@@ -10 +9 @@ root:",
            "-                - child_a",
            "+                - child_c",
            "@@ -11,0 +11 @@ root:",
            "+                - child_a",
            "@@ -16,0 +17,2 @@ root:",
            "+",
            "+",
        ]
        # act
        changed_lines = sut._get_file_diff(lines)

        # assert
        assert changed_lines == [
            ChangedLine(number=7, type=LineChangeType.DELETION, content="            key_a: value_a"),
            ChangedLine(number=10, type=LineChangeType.DELETION, content="                - child_a"),
            ChangedLine(number=9, type=LineChangeType.ADDITION, content="                - child_c"),
            ChangedLine(number=11, type=LineChangeType.ADDITION, content="                - child_a"),
            ChangedLine(number=17, type=LineChangeType.ADDITION, content=""),
            ChangedLine(number=18, type=LineChangeType.ADDITION, content=""),
        ]

    def test_get_file_diff_2(self, sut: RepoAnalyzer):
        # arrange
        lines = [
            "@@ -12 +12 @@ root:",
            "-        - object_b:",
            "+        - object_c:",
            "@@ -22 +22 @@ root:",
            "-                    key_b: value_b",
            "\\ No newline at end of file",
            "+                    key_b: value_c",
            "\\ No newline at end of file",
        ]
        # act
        changed_lines = sut._get_file_diff(lines)

        # assert
        assert changed_lines == [
            ChangedLine(number=12, type=LineChangeType.DELETION, content="        - object_b:"),
            ChangedLine(number=12, type=LineChangeType.ADDITION, content="        - object_c:"),
            ChangedLine(number=22, type=LineChangeType.DELETION, content="                    key_b: value_b"),
            ChangedLine(number=22, type=LineChangeType.ADDITION, content="                    key_b: value_c"),
        ]

    @pytest.fixture
    def sut(self) -> RepoAnalyzer:
        return RepoAnalyzer(".")
