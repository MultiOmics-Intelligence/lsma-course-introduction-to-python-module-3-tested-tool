"""Lets your tests import from scripts/, e.g.  from fasta_stats import main"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
