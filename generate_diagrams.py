
#!/usr/bin/env python3
"""generate_diagrams_v3.py
- lit la colonne Domain dans Applications
- groupe les composants par Domain dans des packages
- ignore les flux Deleted
"""
import argparse, pathlib, pandas as pd, shutil, subprocess, re, sys

COLOR_MAP = {
    'New': 'OliveDrab',
    'Existing': '#4472C4',
    'SaaS': 'LightGray',
    'Updated': 'Gold'
}

def safe_alias(name:str)->str:
    return re.sub(r'[^A-Za-z0-9_]', '_', name)

def header():
    lines=['@startuml','skinparam componentStyle rectangle']
    for st, col in COLOR_MAP.items():
        lines.append('skinparam component {')
        lines.append(f'    BackgroundColor<<{st}>> {col}')
        lines.append('}')
    return lines

def build_component_blocks(apps_df):
    blocks=[]
    for domain, group in apps_df.groupby('Domain', dropna=False):
        dom_name = domain if pd.notna(domain) and domain!='' else 'Unspecified'
        blocks.append(f'package "{dom_name}" {{')
        for _, row in group.iterrows():
            alias=safe_alias(row.ID)
            blocks.append(f'  component "{row.ID}" as {alias} <<{row.Status}>>')
        blocks.append('}')
    return blocks

def build_links(flows_df):
    links=[]
    for _, row in flows_df.iterrows():
        src=safe_alias(row.Outbound)
        dst=safe_alias(row.Inbound)
        links.append(f'{src} --> {dst} : {row.Protocol}')
    return links

def make_puml(flows_df, apps_df):
    lines=header()
    lines.extend(build_component_blocks(apps_df[apps_df['ID'].isin(set(flows_df['Outbound']).union(flows_df['Inbound']))]))
    lines.extend(build_links(flows_df))
    lines.append('@enduml')
    return "\n".join(lines)

def save(content, path):
    path.write_text(content, encoding='utf-8')
    print('📝', path)

def export_png(path):
    cli=shutil.which('plantuml')
    if cli:
        subprocess.run([cli,'-tpng',str(path)],check=False)

def generate(xlsx, out_dir):
    wb=pd.ExcelFile(xlsx)
    flows=wb.parse('Flows')
    apps=wb.parse('Applications')
    if 'Status' in flows.columns:
        flows=flows[flows['Status'].str.lower()!='deleted']
    out_dir.mkdir(parents=True, exist_ok=True)
    # overview
    ov_puml=make_puml(flows, apps)
    ov_path=out_dir/'overview.puml'
    save(ov_puml, ov_path)
    export_png(ov_path)
    # per process
    for proc in flows['BusinessProcess'].dropna().unique():
        sub=flows[flows['BusinessProcess']==proc]
        puml=make_puml(sub, apps)
        p_path=out_dir/f'process_{proc}.puml'
        save(puml, p_path)
        export_png(p_path)

if __name__=='__main__':
    import pandas as pd
    ap=argparse.ArgumentParser()
    ap.add_argument('-i','--input',default='petstore_archi_v5.xlsx')
    ap.add_argument('-o','--out',default='diagrams')
    args=ap.parse_args()
    generate(pathlib.Path(args.input), pathlib.Path(args.out))
