import re
from typing import List, Optional

from git import Repo


class RepoAnalyzer:
    def __init__(self, repo_path: str):
        self._repo = Repo(repo_path)

    def get_changed_files(
        self,
        commit_a: Optional[str] = "HEAD",
        commit_b: Optional[str] = None,
    ) -> List[str]:
        return self._repo.git.diff("--name-only", commit_a, commit_b).split("\n")
