
"""Generate docstrings and documentation for source code."""
 
from __future__ import annotations
 
from enum import Enum
from pathlib import Path
 
from .client import AIClient
 
 
class DocStyle(str, Enum):
    GOOGLE = "google"
    NUMPY = "numpy"
    SPHINX = "sphinx"
    MARKDOWN = "markdown"
 
 
class DocDetail(str, Enum):
    CONCISE = "concise"
    DETAILED = "detailed"
    EXAMPLES = "examples"
 
 
SYSTEM_PROMPT = (
    "You are an expert Python documentation writer. "
    "Produce clean, accurate documentation in the requested format. "
    "Return only the documentation block — no surrounding explanation."
)
 
STYLE_INSTRUCTIONS: dict[DocStyle, str] = {
    DocStyle.GOOGLE: "Google-style Python docstring (Args / Returns / Raises / Example sections).",
    DocStyle.NUMPY: "NumPy-style docstring (Parameters / Returns / Raises / Examples sections).",
    DocStyle.SPHINX: "Sphinx reStructuredText docstring (:param:, :type:, :returns:, :rtype:).",
    DocStyle.MARKDOWN: "Markdown documentation section with headers, param table, and code example.",
}
 
DETAIL_INSTRUCTIONS: dict[DocDetail, str] = {
    DocDetail.CONCISE: "Be brief — one-line summary plus essential params/returns only.",
    DocDetail.DETAILED: "Be thorough: full description, all parameters with types, return types, and edge cases.",
    DocDetail.EXAMPLES: "Include a runnable usage example section with realistic values.",
}
 
 
class DocGenerator:
    """Generate documentation for Python source code."""
 
    def __init__(self, client: AIClient) -> None:
        self._client = client
 
    def generate(
        self,
        code: str,
        style: DocStyle = DocStyle.GOOGLE,
        detail: DocDetail = DocDetail.DETAILED,
    ) -> str:
        """Generate documentation for the supplied code snippet.
 
        Args:
            code: The Python source code to document.
            style: Documentation style to use.
            detail: Level of detail to include.
 
        Returns:
            The generated documentation string.
        """
        prompt = (
            f"Generate {STYLE_INSTRUCTIONS[style]}\n"
            f"{DETAIL_INSTRUCTIONS[detail]}\n\n"
            f"Code:\n```python\n{code}\n```"
        )
        return self._client.complete(prompt, SYSTEM_PROMPT)
 
    def generate_file(
        self,
        path: str | Path,
        style: DocStyle = DocStyle.GOOGLE,
        detail: DocDetail = DocDetail.DETAILED,
    ) -> str:
        """Read a Python file and generate documentation for its contents.
 
        Args:
            path: Path to the .py file.
            style: Documentation style to use.
            detail: Level of detail to include.
 
        Returns:
            The generated documentation string.
 
        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file is not a .py file.
        """
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        if path.suffix != ".py":
            raise ValueError(f"Expected a .py file, got: {path.suffix}")
        return self.generate(path.read_text(encoding="utf-8"), style, detail)
