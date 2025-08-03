
#!/usr/bin/env python3
"""generate_diagrams_v2.py
Génère des diagrammes PlantUML pour l'overview et pour chaque processus métier,
avec couleurs de composants basées sur leur statut et exclusion des flux 'Deleted'.
"""
import argparse, pathlib, pandas as pd, subprocess, shutil, re, sys

COLOR_MAP = {
    'New': 'OliveDrab',
    'Existing': '#4472C4',
    'SaaS': 'LightGray',
    'Updated': 'Gold'
}

def safe_alias(name: str) -> str:
    return re.sub(r'[^A-Za-z0-9_]', '_', name)

def plantuml_header():
    lines = ['@startuml', 'skinparam componentStyle rectangle']
    for status, color in COLOR_MAP.items():
        lines.append(f'skinparam component {{')
        lines.append(f'    BackgroundColor<<{status}>> {color}')
        lines.append(f'    BorderColor<<{status}>> black')
        lines.append('}')
    return lines

def declare_components(app_ids, apps_df):
    decl = []
    for app_id in sorted(app_ids):
        row = apps_df.loc[apps_df['ID'] == app_id].iloc[0]
        alias = safe_alias(app_id)
        status = row['Status']
        decl.append(f'component "{app_id}" as {alias} <<{status}>>')
    return decl

def flows_to_puml(flows_df, apps_df):
    lines = plantuml_header()
    app_ids = set(flows_df['Outbound']).union(flows_df['Inbound'])
    lines.extend(declare_components(app_ids, apps_df))
    for _, row in flows_df.iterrows():
        src = safe_alias(row.Outbound)
        dst = safe_alias(row.Inbound)
        lines.append(f'{src} --> {dst} : {row.Protocol}')
    lines.append('@enduml')
    return "\n".join(lines)

def save_puml(path, content):
    path.write_text(content, encoding='utf-8')
    print('📝', path)

def export_png(puml_path):
    cli = shutil.which('plantuml')
    if not cli:
        return
    subprocess.run([cli, '-tpng', str(puml_path)], check=False)

def generate(xlsx, out_dir):
    wb = pd.ExcelFile(xlsx)
    flows = wb.parse('Flows')
    apps = wb.parse('Applications')
    # Nettoyage flux Deleted
    if 'Status' in flows.columns:
        flows = flows[flows['Status'].str.lower() != 'deleted']
    out_dir.mkdir(parents=True, exist_ok=True)

    # Overview
    overview = flows_to_puml(flows, apps)
    ov_path = out_dir / 'overview.puml'
    save_puml(ov_path, overview)
    export_png(ov_path)

    # Diagrammes par processus
    for proc in flows['BusinessProcess'].dropna().unique():
        sub = flows[flows['BusinessProcess'] == proc]
        puml = flows_to_puml(sub, apps)
        p_path = out_dir / f'process_{proc}.puml'
        save_puml(p_path, puml)
        export_png(p_path)

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-i','--input', default='petstore_archi_v4.xlsx')
    ap.add_argument('-o','--out', default='diagrams')
    args = ap.parse_args()
    generate(pathlib.Path(args.input), pathlib.Path(args.out))
