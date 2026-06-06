"""Colab URL generation and notebook handling."""

from __future__ import annotations

import base64
import json
from dataclasses import dataclass

import nbformat

from app.config import get_settings
from app.models.question import Question


@dataclass
class ColabResult:
    colab_url: str
    nbviewer_url: str | None
    source: str


def _notebook_json(question: Question, module_name: str) -> str:
    nb = nbformat.v4.new_notebook()
    nb.cells.append(
        nbformat.v4.new_markdown_cell(
            f"# {question.title}\n\n"
            f"**Module**: {module_name}  \n"
            f"**Difficulty**: {question.difficulty}  \n"
            f"**Type**: {question.question_type}\n\n"
            f"---\n\n{question.problem_statement}"
        )
    )
    nb.cells.append(
        nbformat.v4.new_code_cell(
            "# Python 3 is pre-installed on Colab\n"
            "# !pip install <package>  # uncomment if you need extra packages"
        )
    )
    nb.cells.append(
        nbformat.v4.new_code_cell(question.starter_code or "# Your code here\n")
    )
    if question.constraints:
        nb.cells.append(
            nbformat.v4.new_markdown_cell(f"**Constraints:** {question.constraints}")
        )
    return nbformat.writes(nb, version=nbformat.NO_CONVERT)


def generate_colab_url(question: Question, module_name: str = "Python Learning Studio") -> str:
    """Build a Colab-open URL from an in-memory notebook."""
    settings = get_settings()
    nb_str = _notebook_json(question, module_name)
    encoded = base64.urlsafe_b64encode(nb_str.encode("utf-8")).decode("ascii")
    return f"{settings.colab_notebook_base_url}{encoded}"


def resolve_colab_url(question: Question, module_name: str | None = None) -> ColabResult:
    """Return stored Colab link or generate a notebook URL."""
    if question.colab_link:
        nbviewer = None
        link = question.colab_link
        if link.startswith("http"):
            settings = get_settings()
            nbviewer = f"{settings.nbviewer_base_url}{link}"
        return ColabResult(colab_url=link, nbviewer_url=nbviewer, source="stored")

    name = module_name or "Python Learning Studio"
    url = generate_colab_url(question, name)
    return ColabResult(colab_url=url, nbviewer_url=None, source="generated")


def notebook_metadata(question: Question, module_name: str) -> dict:
    """Lightweight notebook preview for API responses."""
    return {
        "title": question.title,
        "module": module_name,
        "cell_count": 3 + (1 if question.constraints else 0),
        "format": "nbformat-v4",
    }


def parse_colab_import_payload(raw: str) -> dict:
    """Validate minimal notebook import JSON (Phase 4 extends this)."""
    data = json.loads(raw)
    if "cells" not in data and "nbformat" not in data:
        raise ValueError("Not a valid notebook JSON")
    return data
