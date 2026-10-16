"""
pages/recommendation.py — Alias / Entry point for Recommendation Page (LaptopExpert)
Redirects to or executes pages/2_Rekomendasi.py
"""
import runpy
from pathlib import Path

target_file = Path(__file__).parent / "2_Rekomendasi.py"
runpy.run_path(str(target_file), run_name="__main__")

