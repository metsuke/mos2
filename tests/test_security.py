"""Tests de seguridad de imports."""

from moslib.core.security import analyze_imports, validate_command_source


def test_allowed_stdlib():
    source = """
import os
import sys
from pathlib import Path
import json
"""
    ok, errors = analyze_imports(source)
    assert ok is True
    assert errors == []


def test_allowed_moslib():
    source = """
import moslib
from moslib.core import user
from moslib.core.user import get_username
"""
    ok, errors = analyze_imports(source)
    assert ok is True
    assert errors == []


def test_forbidden_third_party():
    source = """
import requests
import numpy as np
from flask import Flask
"""
    ok, errors = analyze_imports(source)
    assert ok is False
    assert len(errors) >= 3


def test_forbidden_mixed():
    source = """
import os
import requests
from moslib.core.user import get_username
"""
    ok, errors = analyze_imports(source)
    assert ok is False
    assert any("requests" in e for e in errors)


def test_relative_import_rejected():
    source = """
from . import something
from ..core import user
"""
    ok, errors = analyze_imports(source)
    assert ok is False
    assert len(errors) >= 1