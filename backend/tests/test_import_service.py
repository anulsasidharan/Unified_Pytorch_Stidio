"""Unit tests for notebook import parsing."""

import pytest

from app.services.import_service import (
    ImportValidationError,
    extract_notebook_fields,
    parse_csv_content,
    parse_json_payload,
    resolve_notebook_fetch_url,
)


def test_parse_csv_minimal() -> None:
    csv = (
        "title,problem_statement,starter_code\n"
        '"A","Do X","import torch"\n'
    )
    items = parse_csv_content(csv)
    assert len(items) == 1
    assert items[0].title == "A"
    assert items[0].solution_code == "import torch"


def test_parse_json_spec_format() -> None:
    data = {
        "questions": [
            {
                "title": "BatchNorm",
                "topic_slug": "nn-module",
                "difficulty": "advanced",
                "problem_statement": "Implement BN",
                "starter_code": "import torch",
            }
        ]
    }
    items = parse_json_payload(data)
    assert items[0].difficulty == "advanced"


def test_extract_notebook_fields() -> None:
    nb = {
        "nbformat": 4,
        "nbformat_minor": 5,
        "cells": [
            {"cell_type": "markdown", "source": "# My Challenge\n\nSolve this."},
            {"cell_type": "code", "source": "import torch\nx = 1"},
        ],
        "metadata": {},
    }
    parsed = extract_notebook_fields(nb)
    assert parsed.title == "My Challenge"
    assert "Solve this" in parsed.problem_statement
    assert "import torch" in (parsed.solution_code or "")


def test_resolve_nbviewer_url() -> None:
    url = "https://nbviewer.org/github/org/repo/blob/main/demo.ipynb"
    raw = resolve_notebook_fetch_url(url)
    assert "github.com" in raw or "raw" in raw


def test_csv_missing_columns() -> None:
    with pytest.raises(ImportValidationError):
        parse_csv_content("foo,bar\n1,2\n")
