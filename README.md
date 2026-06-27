# 🤖 AI-Powered Code Documentation & Search Assistant

> Instantly generate docstrings, answer questions about your codebase, and build beautiful GitHub READMEs — all from the command line, powered by Claude AI.


## 📖 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Generate Docs](#1-generate-docs)
  - [Ask Questions](#2-ask-questions)
  - [Build README](#3-build-readme)
- [Running Tests](#running-tests)
- [How It Works](#how-it-works)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

**ai-code-docs** is a Python CLI tool that uses the [Anthropic Claude API](https://anthropic.com) to automate the most tedious parts of developer documentation:

| Task | What it does |
|---|---|
| `generate` | Reads a `.py` file and writes Google / NumPy / Sphinx / Markdown docs |
| `ask` | Answers natural-language questions about any codebase |
| `readme` | Builds a full `README.md` from your project metadata |

All three commands work from your terminal with a single `ANTHROPIC_API_KEY` environment variable.

---

## ✨ Features

- **Multi-style docstring generation** — Google, NumPy, Sphinx reST, and Markdown
- **Three detail levels** — Concise, Detailed, or With Examples
- **Codebase Q&A** — Index files or whole directories, then ask anything in plain English
- **README builder** — Generates polished GitHub READMEs from prompts
- **Stdin support** — Pipe code directly: `cat myfile.py | ai-code-docs generate -`
- **File & directory indexing** — Search across your entire project in one command
- **Clean architecture** — Thin wrappers, fully mockable, easy to extend

---

## 🗂 Project Structure

```
ai-code-docs/
├── src/
│   └── ai_code_docs/
│       ├── __init__.py        # Package metadata
│       ├── client.py          # Anthropic SDK wrapper
│       ├── generator.py       # Docstring / doc generation
│       ├── searcher.py        # Codebase indexing & Q&A
│       ├── readme_builder.py  # README.md generation
│       └── cli.py             # Click CLI entry point
├── tests/
│   ├── test_generator.py
│   └── test_searcher.py
├── pyproject.toml
├── requirements.txt
└── README.md
```

---

## ✅ Requirements

- Python **3.9+**
- An [Anthropic API key](https://console.anthropic.com/)

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-code-docs.git
cd ai-code-docs
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate           # Windows
```

### 3. Install the package

```bash
pip install -e ".[dev]"
```

This installs the `ai-code-docs` CLI command and all dependencies.

---

## ⚙️ Configuration

Export your Anthropic API key before running any command:

```bash
export ANTHROPIC_API_KEY="sk-ant-..."   # macOS / Linux
set ANTHROPIC_API_KEY=sk-ant-...        # Windows CMD
$env:ANTHROPIC_API_KEY="sk-ant-..."     # PowerShell
```

You can also add it to a `.env` file and load it with `python-dotenv` or `direnv`.

---

## 🛠 Usage

### 1. Generate Docs

Generate documentation for any Python file:

```bash
# Google-style docstrings (default)
ai-code-docs generate src/ai_code_docs/searcher.py

# NumPy-style, detailed, saved to a file
ai-code-docs generate mymodule.py --style numpy --detail detailed --output docs/mymodule.md

# Pipe from stdin
cat utils.py | ai-code-docs generate -

# Available styles:  google | numpy | sphinx | markdown
# Available details: concise | detailed | examples
```

**Example output (Google style):**

```python
def add(a: int, b: int) -> int:
    """Add two integers and return their sum.

    Args:
        a: The first integer operand.
        b: The second integer operand.

    Returns:
        The sum of a and b.

    Example:
        >>> add(2, 3)
        5
    """
    return a + b
```

---

### 2. Ask Questions

Ask natural-language questions about your code:

```bash
# Simple question (no context)
ai-code-docs ask "What is memoization?"

# With a specific file as context
ai-code-docs ask "How does token verification work?" -f src/auth.py

# Index a whole directory
ai-code-docs ask "Where is pagination handled?" -d src/

# Multiple files
ai-code-docs ask "What does the cache layer do?" -f db.py -f cache.py
```

**Example output:**

```
The `cache.memoize` function wraps any callable with Redis-backed memoization.
It serialises the function arguments into a cache key, checks Redis for a hit,
and on a miss calls the original function and stores the result with the given TTL.
```

---

### 3. Build README

Generate a `README.md` interactively:

```bash
ai-code-docs readme
```

You will be prompted for:

```
Project name: my-awesome-api
Short description: A blazing-fast REST API for task management
Tech stack (comma-separated): Python, FastAPI, PostgreSQL, Redis
Key features (comma-separated): JWT auth, rate limiting, async endpoints
```

Or pass everything as flags for scripting:

```bash
ai-code-docs readme \
  --name "my-awesome-api" \
  --description "A blazing-fast REST API for task management" \
  --tech "Python, FastAPI, PostgreSQL, Redis" \
  --features "JWT auth, rate limiting, async endpoints" \
  --style detailed \
  --output README.md
```

---

## 🧪 Running Tests

```bash
# Run all tests
pytest

# With coverage report
pytest --cov=ai_code_docs --cov-report=term-missing

# Run a specific test file
pytest tests/test_generator.py -v
```

All tests mock the Anthropic API — no real API calls are made during testing.

---

## 🔍 How It Works

```
Your code / question
       │
       ▼
  ai_code_docs CLI  (Click)
       │
       ▼
  AIClient  ──────────►  Anthropic API (Claude Sonnet)
       │                        │
  ┌────┴─────┐                  │ structured prompt
  │generator │◄─────────────────┘
  │searcher  │   answer / docs / README
  │readme_   │
  │builder   │
  └──────────┘
       │
       ▼
  stdout / file
```

1. **`client.py`** wraps the Anthropic SDK and manages the API key.
2. **`generator.py`** builds a structured prompt with your code + chosen style/detail and returns the doc block.
3. **`searcher.py`** maintains an in-memory `CodeIndex`, assembles context from indexed files, and calls Claude with your question.
4. **`readme_builder.py`** takes a `ProjectInfo` dataclass and produces a full Markdown README.
5. **`cli.py`** wires everything together with a Click command group.

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/my-feature`
3. Make your changes with tests
4. Run `pytest` and ensure all tests pass
5. Open a pull request

Please open an issue first for major changes so we can discuss the approach.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<p align="center">Built with ❤️ and <a href="https://anthropic.com">Claude AI</a></p>
