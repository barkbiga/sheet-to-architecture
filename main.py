#!/usr/bin/env python3
"""
main.py – Point d’entrée du conteneur
1. Génère les diagrammes PlantUML/PNG
2. Construit les documents (architecture, executive, runbook)

Variables d’environnement (override possibles) :
  EXCEL_FILE : chemin vers le classeur   (défaut petstore_archi_v5.xlsx)
  DIAG_DIR   : dossier diagrammes        (défaut diagrams)
  OUT_DIR    : dossier docs générés      (défaut docs_multi)
"""
import subprocess, pathlib, argparse, os, sys
THIS_DIR = pathlib.Path(__file__).resolve().parent

def run(cmd: list[str]) -> None:
    print("▶", " ".join(cmd), flush=True)
    res = subprocess.run(cmd)
    if res.returncode:
        sys.exit(res.returncode)

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", default=os.getenv("EXCEL_FILE", "petstore_archi_v5.xlsx"))
    ap.add_argument("-d", "--diagrams", default=os.getenv("DIAG_DIR", "diagrams"))
    ap.add_argument("-o", "--output", default=os.getenv("OUT_DIR", "docs_multi"))
    args = ap.parse_args()

    excel = pathlib.Path(args.input).resolve()
    if not excel.exists():
        print(f"❌ Excel file not found: {excel}")
        sys.exit(1)

    # 1 – Diagrammes
    run(["python", str(THIS_DIR / "generate_diagrams.py"), "-i", str(excel), "-o", args.diagrams])

    # 2 – Documentation
    run(["python", str(THIS_DIR / "build_docs.py"), "-i", str(excel)])

    print("✅ Build complete. Output in", args.output)

if __name__ == "__main__":
    main()
