
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

def clean_nan(value):
    """Remplace les valeurs nan/null par une chaîne vide"""
    try:
        if value is None or (pd.notna(value) == False) or str(value).lower() in ['nan', 'none', 'null']:
            return ''
    except:
        # Si on ne peut pas tester avec pandas, utiliser une approche simple
        if value is None or str(value).lower() in ['nan', 'none', 'null']:
            return ''
    return str(value)

def format_steps(value):
    """Formate les étapes de valuestream pour meilleure lisibilité"""
    try:
        if value is None or (pd.notna(value) == False) or str(value).lower() in ['nan', 'none', 'null']:
            return ''
    except:
        if value is None or str(value).lower() in ['nan', 'none', 'null']:
            return ''
    
    # Remplacer les virgules par des puces avec retour à la ligne
    steps = str(value).split(',')
    if len(steps) > 1:
        return '<br/>• ' + '<br/>• '.join(step.strip() for step in steps)
    return str(value)

def render(tpl_name, ctx, out_path):
    env = Environment(loader=FileSystemLoader(TPL_DIR),
                      trim_blocks=True, lstrip_blocks=True)
    
    # Ajouter des filtres personnalisés
    env.filters['clean_nan'] = clean_nan
    env.filters['format_steps'] = format_steps
    
    text = env.get_template(tpl_name).render(**ctx)
    out_path.write_text(text, encoding='utf-8')

# Fonction copy_diagrams supprimée - les diagrammes sont déjà dans generated/diagrams

def main(xlsx, output_dir=None, diagrams_dir=None):
    # Définir les répertoires de sortie
    out_path = pathlib.Path(output_dir) if output_dir else OUT
    diag_path = pathlib.Path(diagrams_dir) if diagrams_dir else DIAG
    
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
    
    out_path.mkdir(exist_ok=True, parents=True)
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
            render(tpl, ctx, out_path / name)
    # copy_diagrams() supprimé - les diagrammes sont déjà dans generated/diagrams
    print('✅ Documents générés :', ", ".join([f[1] for f in files]))

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-i','--input',default='petstore_archi_v3.xlsx')
    ap.add_argument('-o','--output', help='Répertoire de sortie pour la documentation')
    args = ap.parse_args()
    
    # Appeler main avec les répertoires de sortie
    main(pathlib.Path(args.input), args.output, args.output + '/diagrams' if args.output else None)
