
#!/usr/bin/env python3
"""Construit trois documents : architecture_full.md, executive.md, runbook.md
puis copie les diagrammes générés.

Prérequis : pandas, jinja2
"""
import argparse, pathlib, pandas as pd
from jinja2 import Environment, FileSystemLoader
import subprocess, shutil

BASE = pathlib.Path(__file__).resolve().parent
TPL_DIR = BASE / 'templates_multi'
CHAPTERS_DIR = BASE / 'templates_multi' / 'chapters'
OUT = BASE / 'generated'
DIAG = BASE / 'diagrams'

def load_ctx(xlsx):
    wb = pd.ExcelFile(xlsx)
    ctx = {s.lower(): wb.parse(s).to_dict('records') for s in wb.sheet_names}
    ctx['project'] = wb.parse('Project').iloc[0].to_dict() if 'Project' in wb.sheet_names else {}
    # alias tables
    for s in wb.sheet_names:
        ctx[s] = ctx[s.lower()]
    return ctx

def render(tpl_name, ctx, out_path):
    env = Environment(loader=FileSystemLoader(TPL_DIR),
                      trim_blocks=True, lstrip_blocks=True)
    
    text = env.get_template(tpl_name).render(**ctx)
    out_path.write_text(text, encoding='utf-8')

def copy_diagrams():
    if not DIAG.exists():
        return
    dest = OUT / 'diagrams'
    dest.mkdir(exist_ok=True, parents=True)
    for f in DIAG.glob('*.*'):
        (dest / f.name).write_bytes(f.read_bytes())

def main(xlsx):
    ctx = load_ctx(xlsx)
    OUT.mkdir(exist_ok=True, parents=True)
    files = [('architecture_full.md.j2','architecture.md'),
             ('executive.md.j2','executive.md'),
             ('runbook.md.j2','runbook.md')]
    for tpl, name in files:
        render(tpl, ctx, OUT / name)
    copy_diagrams()
    print('✅ Documents générés :', ", ".join([f[1] for f in files]))

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-i','--input',default='petstore_archi_v3.xlsx')
    args = ap.parse_args()
    main(pathlib.Path(args.input))
