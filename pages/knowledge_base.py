"""
pages/knowledge_base.py — Alias / Entry point for Knowledge Base Page (LaptopExpert)
Redirects to or executes pages/3_Basis_Pengetahuan.py
"""
import runpy
from pathlib import Path

target_file = Path(__file__).parent / "3_Basis_Pengetahuan.py"
runpy.run_path(str(target_file), run_name="__main__")

