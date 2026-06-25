"""Tests for the DocGenerator module."""

from unittest.mock import MagicMock

import pytest

from ai_code_docs.generator import DocGenerator, DocStyle, DocDetail
from ai_code_docs.client import AIClient


SAMPLE_CODE = """\
def add(a: int, b: int) -> int:
    return a + b
"""


@pytest.fixture()
def mock_client() -> AIClient:
    client = MagicMock(spec=AIClient)
    client.complete.return_value = '"""Add two integers."""'
    return client


def test_generate_returns_string(mock_client):
    gen = DocGenerator(mock_client)
    result = gen.generate(SAMPLE_CODE)
    assert isinstance(result, str)
    assert len(result) > 0


def test_generate_calls_client_once(mock_client):
    gen = DocGenerator(mock_client)
    gen.generate(SAMPLE_CODE, style=DocStyle.GOOGLE, detail=DocDetail.CONCISE)
    mock_client.complete.assert_called_once()


def test_generate_includes_style_in_prompt(mock_client):
    gen = DocGenerator(mock_client)
    gen.generate(SAMPLE_CODE, style=DocStyle.NUMPY)
    call_args = mock_client.complete.call_args[0][0]
    assert "NumPy" in call_args


def test_generate_file_not_found(mock_client):
    gen = DocGenerator(mock_client)
    with pytest.raises(FileNotFoundError):
        gen.generate_file("nonexistent.py")


def test_generate_file_wrong_extension(mock_client, tmp_path):
    f = tmp_path / "code.txt"
    f.write_text("x = 1")
    gen = DocGenerator(mock_client)
    with pytest.raises(ValueError):
        gen.generate_file(f)


def test_generate_file_reads_and_generates(mock_client, tmp_path):
    f = tmp_path / "module.py"
    f.write_text(SAMPLE_CODE)
    gen = DocGenerator(mock_client)
    result = gen.generate_file(f)
    assert isinstance(result, str)
    call_args = mock_client.complete.call_args[0][0]
    assert "add" in call_args
