from typing import List

import pytest

from core.repository import RepoAnalyzer


class TestRepoAnalyzer:
    def test_get_changed_files(self, sut: RepoAnalyzer):
        changed_files = sut.get_changed_files(
            commit_a="c32fdc6266f075a15dad84b3bca3e237085629a3",
            commit_b="c85bad286af9023c510ed3f5ddcfaed5503c4a6c",
        )
        # Check for a few known changed files for robustness
        assert ".python-version" in changed_files
        assert "README.md" in changed_files
        assert "pyproject.toml" in changed_files
        assert "uv.lock" in changed_files

    @pytest.fixture
    def sut(self) -> RepoAnalyzer:
        return RepoAnalyzer(".")
