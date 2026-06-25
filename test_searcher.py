"""Tests for the CodeSearcher and CodeIndex modules."""

from unittest.mock import MagicMock

import pytest

from ai_code_docs.searcher import CodeIndex, CodeSearcher, SearchResult
from ai_code_docs.client import AIClient


@pytest.fixture()
def mock_client() -> AIClient:
    client = MagicMock(spec=AIClient)
    client.complete.return_value = "This function adds two numbers."
    return client


class TestCodeIndex:
    def test_add_and_retrieve(self):
        index = CodeIndex()
        index.add("math.py", "def add(a, b): return a + b")
        assert "math.py" in index.entries

    def test_add_file(self, tmp_path):
        f = tmp_path / "util.py"
        f.write_text("x = 42")
        index = CodeIndex()
        index.add_file(f)
        assert "util.py" in index.entries

    def test_add_file_not_found(self):
        index = CodeIndex()
        with pytest.raises(FileNotFoundError):
            index.add_file("missing.py")

    def test_add_directory(self, tmp_path):
        (tmp_path / "a.py").write_text("a = 1")
        (tmp_path / "b.py").write_text("b = 2")
        index = CodeIndex()
        count = index.add_directory(tmp_path)
        assert count == 2

    def test_context_block_not_empty(self):
        index = CodeIndex()
        index.add("x.py", "print('hi')")
        ctx = index.context_block()
        assert "x.py" in ctx
        assert "print" in ctx


class TestCodeSearcher:
    def test_ask_returns_search_result(self, mock_client):
        searcher = CodeSearcher(mock_client)
        result = searcher.ask("What does add() do?")
        assert isinstance(result, SearchResult)
        assert result.answer == "This function adds two numbers."

    def test_ask_with_extra_context(self, mock_client):
        searcher = CodeSearcher(mock_client)
        searcher.ask("Explain this", extra_context="def foo(): pass")
        prompt = mock_client.complete.call_args[0][0]
        assert "foo" in prompt

    def test_ask_with_indexed_code(self, mock_client):
        index = CodeIndex()
        index.add("helpers.py", "def helper(): pass")
        searcher = CodeSearcher(mock_client, index)
        searcher.ask("What is helper?")
        prompt = mock_client.complete.call_args[0][0]
        assert "helper" in prompt
