
#!/usr/bin/env python3
"""Construit trois documents : architecture_full.md, executive.md, runbook.md
puis copie les diagrammes générés.

Prérequis : pandas, jinja2
"""
import argparse, pathlib, pandas as pd, sys, os
from jinja2 import Environment, FileSystemLoader
import subprocess, shutil

# Ajouter le répertoire generators au chemin Python
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'generators'))
from generate_infrastructure_diagrams import generate_flows_table, generate_security_table, deduplicate_flows

BASE = pathlib.Path(__file__).resolve().parent.parent
TPL_DIR = BASE / 'templates_multi'
CHAPTERS_DIR = BASE / 'templates_multi' / 'chapters'
OUT = BASE / 'generated'
DIAG = BASE / 'generated' / 'diagrams'

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

# Fonction copy_diagrams supprimée - les diagrammes sont déjà dans generated/diagrams

def main(xlsx):
    ctx = load_ctx(xlsx)
    
    # Enrichir le contexte avec les tableaux infrastructure et sécurité
    if 'flows' in ctx and 'applications' in ctx:
        flows_df = pd.DataFrame(ctx['flows'])
        apps_df = pd.DataFrame(ctx['applications'])
        ctx['infrastructure_table'] = generate_flows_table(flows_df, apps_df)
        ctx['security_table'] = generate_security_table(flows_df, apps_df)
        
        # Ajouter des alias pour les templates
        ctx['data_entities'] = ctx.get('data', [])
        ctx['businessprocesses'] = ctx.get('businessprocesses', [])
        
        # Ajouter les nouvelles données pour capacités et value streams
        ctx['capabilities'] = ctx.get('capabilities', [])
        ctx['valuestreams'] = ctx.get('valuestreams', [])
        
        # Nettoyer les BusinessApp pour éviter les erreurs de tri
        apps = ctx.get('applications', [])
        for app in apps:
            if pd.isna(app.get('BusinessApp')):
                app['BusinessApp'] = 'Non défini'
    
    OUT.mkdir(exist_ok=True, parents=True)
    files = [('architecture_simplified.md.j2','architecture.md'),
#             ('architecture_full_improved.md.j2','architecture_complete.md'),
             ('executive_summary.md.j2','executive_summary.md'),
             ('technology_view.md.j2','technology_view.md'),
#             ('traceability_matrix.md.j2','traceability_matrix.md'),
#             ('architecture_full.md.j2','architecture_legacy.md'),
#             ('runbook.md.j2','runbook.md'),
             ('infrastructure_view.md.j2','infrastructure_view.md'),
             ('security_view.md.j2','security_view.md')]
    for tpl, name in files:
        # Ignorer les templates qui n'existent pas encore
        if (TPL_DIR / tpl).exists():
            render(tpl, ctx, OUT / name)
    # copy_diagrams() supprimé - les diagrammes sont déjà dans generated/diagrams
    print('✅ Documents générés :', ", ".join([f[1] for f in files]))

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-i','--input',default='petstore_archi_v3.xlsx')
    args = ap.parse_args()
    main(pathlib.Path(args.input))
