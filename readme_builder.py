
"""Generate README.md files for GitHub projects."""
 
from __future__ import annotations
 
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional
 
 
from .client import AIClient
 
 
class ReadmeStyle(str, Enum):
    STANDARD = "standard"
    MINIMAL = "minimal"
    DETAILED = "detailed"
 
 
SYSTEM_PROMPT = (
    "You are an expert technical writer. "
    "Generate clean, professional GitHub README files that developers love. "
    "Return only raw Markdown — no explanation or surrounding text."
)
 
 
@dataclass
class ProjectInfo:
    name: str
    description: str = ""
    tech_stack: list[str] = field(default_factory=list)
    features: list[str] = field(default_factory=list)
    install_cmd: str = ""
    usage_example: str = ""
    license_name: str = "MIT"
    author: str = ""
    repo_url: str = ""
 
 
class ReadmeBuilder:
    """Build README.md content from project metadata."""
 
    def __init__(self, client: AIClient) -> None:
        self._client = client
 
    def build(
        self,
        info: ProjectInfo,
        style: ReadmeStyle = ReadmeStyle.STANDARD,
    ) -> str:
        """Generate a README.md string.
 
        Args:
            info: Structured project metadata.
            style: Output style — standard, minimal, or detailed.
 
        Returns:
            Markdown string ready to write to README.md.
        """
        tech = ", ".join(info.tech_stack) if info.tech_stack else "not specified"
        features = (
            "\n".join(f"- {f}" for f in info.features)
            if info.features
            else "not provided"
        )
 
        prompt = (
            f"Create a {style.value} GitHub README.md for this project:\n\n"
            f"Name: {info.name}\n"
            f"Description: {info.description or 'not provided'}\n"
            f"Tech stack: {tech}\n"
            f"Features:\n{features}\n"
            f"Install command: {info.install_cmd or 'not provided'}\n"
            f"Usage example: {info.usage_example or 'not provided'}\n"
            f"License: {info.license_name}\n"
            f"Author: {info.author or 'not provided'}\n"
            f"Repo URL: {info.repo_url or 'not provided'}\n"
        )
        return self._client.complete(prompt, SYSTEM_PROMPT, max_tokens=2048)
 
    def build_and_write(
        self,
        info: ProjectInfo,
        output_path: str | Path = "README.md",
        style: ReadmeStyle = ReadmeStyle.STANDARD,
    ) -> Path:
        """Generate a README.md and write it to disk.
 
        Args:
            info: Structured project metadata.
            output_path: Where to write the file.
            style: Output style.
 
        Returns:
            Path to the written file.
        """
        content = self.build(info, style)
        path = Path(output_path)
        path.write_text(content, encoding="utf-8")
        return path
