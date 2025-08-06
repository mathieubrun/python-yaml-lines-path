import re
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from git import Repo


class LineChangeType(Enum):
    ADDITION = "addition"
    DELETION = "deletion"


class FileChangeType(Enum):
    ADDED = "added"
    MODIFIED = "modified"
    DELETED = "deleted"
    RENAMED = "renamed"


@dataclass
class ChangedFile:
    path: str
    type: FileChangeType


@dataclass
class ChangedLine:
    number: int
    type: LineChangeType
    content: str


class RepoAnalyzer:
    def __init__(self, repo_path: str):
        self._repo = Repo(repo_path)

    def get_changed_files(self, commit_a: Optional[str] = "HEAD", commit_b: Optional[str] = None) -> List[ChangedFile]:
        diff_output = self._repo.git.diff("--name-status", commit_a, commit_b)
        if not diff_output:
            return []

        return self._get_changed_files(diff_output.split("\n"))

    def _get_changed_files(self, lines: List[str]) -> List[ChangedFile]:
        changed_files = []
        for line in lines:
            if not line:
                continue
            status, path = line.split(None, 1)

            change_type = FileChangeType.MODIFIED
            match status[0]:
                case "A":
                    change_type = FileChangeType.ADDED
                case "D":
                    change_type = FileChangeType.DELETED
                case "R":
                    change_type = FileChangeType.RENAMED

            changed_files.append(ChangedFile(path=path, type=change_type))

        return changed_files

    def get_file_diff(self, file_path: str, commit_a: Optional[str] = "HEAD", commit_b: Optional[str] = None) -> List[ChangedLine]:
        commit_obj_a = self._repo.commit(commit_a)
        # create_patch=True is essential to get the diff content
        diff_list = commit_obj_a.diff(commit_b, paths=file_path, create_patch=True)

        if not diff_list:
            return []

        # A single file path should result in at most one Diff object
        diff = diff_list[0]

        # diff.diff is bytes or None
        if diff.diff is None:
            return []

        lines = diff.diff.decode("utf-8", "ignore").splitlines()  # type: ignore

        return self._get_file_diff(lines)

    def _get_file_diff(self, lines: List[str]) -> List[ChangedLine]:
        # Regex to parse hunk headers like "@@ -1,1 +1,4 @@"
        hunk_header_re = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")

        source_line = 0
        target_line = 0
        changed_lines = []

        for line in lines:
            match = hunk_header_re.match(line)
            if match:
                source_line = int(match.group(1))
                target_line = int(match.group(3))
                continue

            # We are inside a hunk.
            if line.startswith("---") or line.startswith("+++") or line.startswith("\\"):
                continue

            if line.startswith(" "):
                source_line += 1
                target_line += 1
            elif line.startswith("-"):
                changed_lines.append(ChangedLine(number=source_line, type=LineChangeType.DELETION, content=line[1:]))
                source_line += 1
            elif line.startswith("+"):
                changed_lines.append(ChangedLine(number=target_line, type=LineChangeType.ADDITION, content=line[1:]))
                target_line += 1

        return changed_lines
