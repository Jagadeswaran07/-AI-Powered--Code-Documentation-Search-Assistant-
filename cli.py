"""Command-line interface for ai-code-docs."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

import click

from .client import AIClient
from .generator import DocGenerator, DocStyle, DocDetail
from .searcher import CodeIndex, CodeSearcher
from .readme_builder import ProjectInfo, ReadmeBuilder, ReadmeStyle


def _make_client() -> AIClient:
    try:
        return AIClient()
    except EnvironmentError as exc:
        click.echo(f"Error: {exc}", err=True)
        sys.exit(1)


@click.group()
@click.version_option()
def cli() -> None:
    """AI-Powered Code Documentation & Search Assistant."""


# ---------------------------------------------------------------------------
# docs generate
# ---------------------------------------------------------------------------

@cli.command("generate")
@click.argument("path", type=click.Path(exists=True))
@click.option(
    "--style",
    type=click.Choice([s.value for s in DocStyle]),
    default=DocStyle.GOOGLE.value,
    show_default=True,
    help="Documentation style.",
)
@click.option(
    "--detail",
    type=click.Choice([d.value for d in DocDetail]),
    default=DocDetail.DETAILED.value,
    show_default=True,
    help="Level of detail.",
)
@click.option(
    "--output", "-o",
    type=click.Path(),
    default=None,
    help="Write output to this file instead of stdout.",
)
def generate_cmd(path: str, style: str, detail: str, output: Optional[str]) -> None:
    """Generate documentation for a Python file or snippet.

    PATH can be a .py file or '-' to read from stdin.
    """
    if path == "-":
        code = sys.stdin.read()
    else:
        code = Path(path).read_text(encoding="utf-8")

    client = _make_client()
    gen = DocGenerator(client)
    click.echo("Generating documentation…", err=True)
    result = gen.generate(code, DocStyle(style), DocDetail(detail))

    if output:
        Path(output).write_text(result, encoding="utf-8")
        click.echo(f"Saved to {output}", err=True)
    else:
        click.echo(result)


# ---------------------------------------------------------------------------
# docs ask
# ---------------------------------------------------------------------------

@cli.command("ask")
@click.argument("question")
@click.option(
    "--file", "-f",
    "files",
    multiple=True,
    type=click.Path(exists=True),
    help="Python file(s) to use as context (repeatable).",
)
@click.option(
    "--dir", "-d",
    "directories",
    multiple=True,
    type=click.Path(exists=True, file_okay=False),
    help="Directory/ies to index (repeatable).",
)
def ask_cmd(question: str, files: tuple[str, ...], directories: tuple[str, ...]) -> None:
    """Ask a natural-language question about your codebase.

    \b
    Examples:
      ai-code-docs ask "What does auth.py do?"
      ai-code-docs ask "How do I paginate results?" -f db.py
      ai-code-docs ask "Explain the cache layer" -d src/
    """
    client = _make_client()
    index = CodeIndex()

    for f in files:
        index.add_file(f)
        click.echo(f"Indexed: {f}", err=True)

    for d in directories:
        n = index.add_directory(d)
        click.echo(f"Indexed {n} file(s) from {d}", err=True)

    searcher = CodeSearcher(client, index)
    click.echo("Thinking…\n", err=True)
    result = searcher.ask(question)
    click.echo(result.answer)


# ---------------------------------------------------------------------------
# docs readme
# ---------------------------------------------------------------------------

@cli.command("readme")
@click.option("--name", prompt="Project name", help="Name of the project.")
@click.option("--description", prompt="Short description", default="", help="One-line description.")
@click.option("--tech", prompt="Tech stack (comma-separated)", default="", help="e.g. Python, FastAPI, Redis")
@click.option("--features", prompt="Key features (comma-separated)", default="", help="Feature list.")
@click.option("--install", default="", help="Installation command.")
@click.option("--usage", default="", help="Short usage example.")
@click.option("--license-name", default="MIT", show_default=True, help="License name.")
@click.option("--author", default="", help="Author name.")
@click.option(
    "--style",
    type=click.Choice([s.value for s in ReadmeStyle]),
    default=ReadmeStyle.STANDARD.value,
    show_default=True,
    help="README style.",
)
@click.option(
    "--output", "-o",
    default="README.md",
    show_default=True,
    help="Output file path.",
)
def readme_cmd(
    name: str,
    description: str,
    tech: str,
    features: str,
    install: str,
    usage: str,
    license_name: str,
    author: str,
    style: str,
    output: str,
) -> None:
    """Generate a README.md for your GitHub project."""
    info = ProjectInfo(
        name=name,
        description=description,
        tech_stack=[t.strip() for t in tech.split(",") if t.strip()],
        features=[f.strip() for f in features.split(",") if f.strip()],
        install_cmd=install,
        usage_example=usage,
        license_name=license_name,
        author=author,
    )
    client = _make_client()
    builder = ReadmeBuilder(client)
    click.echo("Building README…", err=True)
    path = builder.build_and_write(info, output, ReadmeStyle(style))
    click.echo(f"README written to {path}")


def main() -> None:
    cli()


if __name__ == "__main__":
    main()
