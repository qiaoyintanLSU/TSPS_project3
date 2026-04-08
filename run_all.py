"""
run_all.py  — Master pipeline runner
======================================
Runs all five analysis scripts in the correct order.
Usage:  python run_all.py
"""
import subprocess, sys, pathlib

SCRIPTS = [
    "scripts/01_load_clean.py",
    "scripts/02_classify.py",
    "scripts/03_descriptive_stats.py",
    "scripts/04_visualize.py",
    "scripts/05_methods_summary.py",
]

BASE = pathlib.Path(__file__).resolve().parent

for script in SCRIPTS:
    print(f"\n{'='*60}\nRunning: {script}\n{'='*60}")
    result = subprocess.run([sys.executable, str(BASE / script)], check=False)
    if result.returncode != 0:
        print(f"ERROR: {script} exited with code {result.returncode}. Stopping.")
        sys.exit(result.returncode)

print("\n✓ Full pipeline complete. Check data/cleaned/, tables/, figures/, and docs/.")
