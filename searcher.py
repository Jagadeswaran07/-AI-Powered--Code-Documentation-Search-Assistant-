
"""Search and explain code using natural-language queries."""
 
from __future__ import annotations
 
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
 
from .client import AIClient
 
 
SYSTEM_PROMPT = (
    "You are a senior Python engineer acting as a code search and explanation engine. "
    "Answer concisely with code examples where helpful. "
    "Use plain text with inline code blocks."
)
 
 
@dataclass
class SearchResult:
    question: str
    answer: str
    context_file: Optional[str] = None
 
 
@dataclass
class CodeIndex:
    """In-memory index of code snippets for contextual search."""
 
    entries: dict[str, str] = field(default_factory=dict)
 
    def add(self, name: str, code: str) -> None:
        """Add a named code snippet to the index.
 
        Args:
            name: Logical name or path for the snippet.
            code: Source code to index.
        """
        self.entries[name] = code
 
    def add_file(self, path: str | Path) -> None:
        """Index an entire Python file.
 
        Args:
            path: Path to the .py file.
 
        Raises:
            FileNotFoundError: If the file does not exist.
        """
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        self.add(path.name, path.read_text(encoding="utf-8"))
 
    def add_directory(self, directory: str | Path, recursive: bool = True) -> int:
        """Index all Python files in a directory.
 
        Args:
            directory: Root directory to scan.
            recursive: Whether to walk subdirectories.
 
        Returns:
            Number of files indexed.
        """
        directory = Path(directory)
        pattern = "**/*.py" if recursive else "*.py"
        files = list(directory.glob(pattern))
        for f in files:
            self.add(str(f.relative_to(directory)), f.read_text(encoding="utf-8"))
        return len(files)
 
    def context_block(self, max_chars: int = 8000) -> str:
        """Build a context string from all indexed entries."""
        parts: list[str] = []
        total = 0
        for name, code in self.entries.items():
            snippet = f"# --- {name} ---\n{code}\n"
            if total + len(snippet) > max_chars:
                break
            parts.append(snippet)
            total += len(snippet)
        return "\n".join(parts)
 
 
class CodeSearcher:
    """Answer natural-language questions about code."""
 
    def __init__(self, client: AIClient, index: Optional[CodeIndex] = None) -> None:
        self._client = client
        self.index = index or CodeIndex()
 
    def ask(self, question: str, extra_context: str = "") -> SearchResult:
        """Ask a question about code.
 
        Args:
            question: Natural-language question.
            extra_context: Optional extra source code to include.
 
        Returns:
            SearchResult containing the answer.
        """
        ctx_parts: list[str] = []
 
        indexed = self.index.context_block()
        if indexed:
            ctx_parts.append(f"Indexed codebase:\n```python\n{indexed}\n```")
 
        if extra_context.strip():
            ctx_parts.append(f"Additional context:\n```python\n{extra_context}\n```")
 
        ctx = "\n\n".join(ctx_parts)
        prompt = f"{ctx}\n\nQuestion: {question}" if ctx else f"Question: {question}"
 
        answer = self._client.complete(prompt, SYSTEM_PROMPT, max_tokens=1024)
        return SearchResult(question=question, answer=answer)
 
