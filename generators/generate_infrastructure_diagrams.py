#!/usr/bin/env python3
"""generate_infrastructure_diagrams.py
Génère des diagrammes et tableaux pour les vues infrastructure et sécurité.
- Déduplique les flux entre composants
- Groupe par zones réseau
- Génère des tableaux explicatifs
"""
import argparse, pathlib, pandas as pd, shutil, subprocess, re, sys, os

# Ajouter le répertoire utils au chemin Python
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
from component_filter import generate_component_puml, generate_component_styles
from status_styles import get_status_styles, normalize_status, generate_component_with_color_only

ZONE_COLORS = {
    'PCI': '#FF6B6B',
    'HORS_PCI': '#4ECDC4', 
    'DMZ': '#FFE66D',
    'INTERNET': '#A8E6CF',
    'INTERNE': '#95A5A6'
}

SECURITY_COLORS = {
    'High': '#E74C3C',
    'Medium': '#F39C12',
    'Low': '#27AE60'
}

def safe_alias(name: str) -> str:
    return re.sub(r'[^A-Za-z0-9_]', '_', name)

def deduplicate_flows(flows_df):
    """Déduplique les flux et agrège les protocoles/ports"""
    # Créer un dictionnaire d'agrégation basé sur les colonnes disponibles
    agg_dict = {
        'Protocol': lambda x: ', '.join(sorted(set(x.astype(str)))),
        'BusinessProcess': 'first',
        'Status': 'first'
    }
    
    # Ajouter les colonnes optionnelles si elles existent
  #  if 'Port' in flows_df.columns:
 #       agg_dict['Port'] = lambda x: ', '.join(sorted(set(str(p) for p in x if pd.notna(p))))
    if 'Source_Zone' in flows_df.columns:
        agg_dict['Source_Zone'] = 'first'
    if 'Target_Zone' in flows_df.columns:
        agg_dict['Target_Zone'] = 'first'
    if 'Security_Controls' in flows_df.columns:
        agg_dict['Security_Controls'] = lambda x: ', '.join(sorted(set(str(s) for s in x if pd.notna(s))))
    if 'Authentication' in flows_df.columns:
        agg_dict['Authentication'] = lambda x: ', '.join(sorted(set(str(a) for a in x if pd.notna(a)))) 
    if 'Encryption' in flows_df.columns:
        agg_dict['Encryption'] = lambda x: ', '.join(sorted(set(str(e) for e in x if pd.notna(e))))
    if 'ValidationStatus' in flows_df.columns:
        agg_dict['ValidationStatus'] = 'first'
    
    # Grouper par source/destination et agréger
    dedup = flows_df.groupby(['Outbound', 'Inbound']).agg(agg_dict).reset_index()
    
    return dedup

def build_infrastructure_header():
    lines = ['@startuml', 'skinparam componentStyle rectangle']
    
    # Ajouter les styles unifiés pour les statuts - couleurs douces
    status_styles = get_status_styles()
    lines.extend(status_styles)
    
    # Style pointillé pour les rectangles de zones
    lines.append('skinparam rectangle {')
    lines.append('    BorderStyle dashed')
    lines.append('    BorderColor Black')
    lines.append('    FontStyle bold')
    lines.append('}')
    
    return lines

def build_security_header():
    lines = ['@startuml', 'skinparam componentStyle rectangle']
    
    # Ajouter les styles unifiés pour les statuts - couleurs douces
    status_styles = get_status_styles()
    lines.extend(status_styles)
    
    # Couleurs pour les niveaux de sécurité (complément aux statuts) - gardées pour compatibilité
    lines.append('skinparam component {')
    lines.append('    BackgroundColor<<High>> #E74C3C')
    lines.append('    BackgroundColor<<Medium>> #F39C12') 
    lines.append('    BackgroundColor<<Low>> #27AE60')
    lines.append('}')
    
    return lines

def build_infrastructure_zones(apps_df, flows_df):
    """Construit les zones réseau avec les composants"""
    blocks = []
    
    # Obtenir tous les composants utilisés dans les flux
    used_components = set(flows_df['Outbound']).union(flows_df['Inbound'])
    relevant_apps = apps_df[apps_df['ID'].isin(used_components)]
    
    # Grouper par zone réseau
    zone_col = 'Network_Zone' if 'Network_Zone' in apps_df.columns else 'Domain'
    
    for zone, group in relevant_apps.groupby(zone_col, dropna=False):
        zone_name = zone if pd.notna(zone) and zone != '' else 'Unspecified'
        zone_alias = safe_alias(zone_name)
        
        # Utiliser rectangle avec style pointillé au lieu de package
        blocks.append(f'rectangle "{zone_name}" as {zone_alias} {{')
        
        for _, row in group.iterrows():
            alias = safe_alias(row['ID'])
            status = normalize_status(row.get('Status', 'UNCHANGED'))
            # Utiliser la fonction utilitaire pour générer le bon type de composant
            component_puml = generate_component_puml(row.to_dict(), alias)
            # Ajouter le statut pour les couleurs
            component_puml = component_puml.replace(f' as {alias}', f' as {alias} <<{status}>>')
            blocks.append(f'  {component_puml}')
        
        blocks.append('}')
    
    return blocks

def build_security_components(apps_df, flows_df):
    """Construit les composants avec niveaux de sécurité"""
    blocks = []
    
    used_components = set(flows_df['Outbound']).union(flows_df['Inbound'])
    relevant_apps = apps_df[apps_df['ID'].isin(used_components)]
    
    for _, row in relevant_apps.iterrows():
        alias = safe_alias(row['ID'])
        status = normalize_status(row.get('Status', 'UNCHANGED'))
        # Utiliser la fonction utilitaire pour générer le bon type de composant
        component_puml = generate_component_puml(row.to_dict(), alias)
        # Ajouter le statut pour les couleurs
        component_puml = component_puml.replace(f' as {alias}', f' as {alias} <<{status}>>')
        blocks.append(f'{component_puml}')
    
    return blocks

def build_infrastructure_links(flows_df):
    """Construit les liens avec protocoles et ports"""
    links = []
    
    for _, row in flows_df.iterrows():
        src = safe_alias(row['Outbound'])
        dst = safe_alias(row['Inbound'])
        protocol = row.get('Protocol', '')
        port = row.get('Port', '')
        
        label = protocol
        if port and str(port) != 'nan':
            label += f":{port}"
        
        links.append(f'{src} --> {dst} : {label}')
    
    return links

def build_security_links(flows_df):
    """Construit les liens avec contrôles de sécurité"""
    links = []
    
    for _, row in flows_df.iterrows():
        src = safe_alias(row['Outbound'])
        dst = safe_alias(row['Inbound'])
        protocol = row.get('Protocol', '')
        controls = row.get('Security_Controls', '')
        
        label = protocol
        if controls and str(controls) != 'nan':
            label += f"\\n[{controls}]"
        
        links.append(f'{src} --> {dst} : {label}')
    
    return links

def generate_infrastructure_puml(flows_df, apps_df):
    """Génère le diagramme d'infrastructure"""
    dedup_flows = deduplicate_flows(flows_df)
    
    lines = build_infrastructure_header()
    lines.extend(build_infrastructure_zones(apps_df, dedup_flows))
    lines.extend(build_infrastructure_links(dedup_flows))
    lines.append('@enduml')
    
    return "\n".join(lines)

def generate_security_puml(flows_df, apps_df):
    """Génère le diagramme de sécurité"""
    dedup_flows = deduplicate_flows(flows_df)
    
    lines = build_security_header()
    lines.extend(build_security_components(apps_df, dedup_flows))
    lines.extend(build_security_links(dedup_flows))
    lines.append('@enduml')
    
    return "\n".join(lines)

def generate_flows_table(flows_df, apps_df):
    """Génère un tableau markdown des flux infrastructure"""
    dedup_flows = deduplicate_flows(flows_df)
    
    # Créer un mapping ID -> Network_Zone depuis Applications
    app_zones = {}
    zone_col = 'Network_Zone' if 'Network_Zone' in apps_df.columns else 'Domain'
    for _, app in apps_df.iterrows():
        zone = app.get(zone_col, 'INTERNE')
        app_zones[app['ID']] = zone
    
    table = ["| Source | Destination | Protocole |",
             "|--------|-------------|-----------|"]
    
    for _, row in dedup_flows.iterrows():
        # Récupérer la zone depuis l'application source
        source = row['Outbound']
        cible = row['Inbound'] 
        zone_source = app_zones.get(source, 'INTERNE')
        zone_cible = app_zones.get(cible, 'INTERNE')

        protocole = row['Protocol']
        
        table.append(f"| {source}({zone_source}) | {cible} ({zone_cible}) | {protocole} |")
    
    return "\n".join(table)

def generate_security_table(flows_df, apps_df):
    """Génère un tableau markdown des mesures de sécurité"""
    dedup_flows = deduplicate_flows(flows_df)
    
    # Créer un mapping ID -> Network_Zone depuis Applications
    app_zones = {}
    zone_col = 'Network_Zone' if 'Network_Zone' in apps_df.columns else 'Domain'
    for _, app in apps_df.iterrows():
        zone = app.get(zone_col, 'INTERNE')
        app_zones[app['ID']] = zone
    
    table = ["|Source | Destination | Protocole | Chiffrement | Authentification | Statut Validation |",
             "|-------|-------------|-----------|-------------|------------------|-------------------|"]
    
    for _, row in dedup_flows.iterrows():
        # Récupérer la zone depuis l'application source
        source = row['Outbound']
        cible = row['Inbound']
        authentication = row.get('Authentication', 'Basic Auth')
        validation_status = row.get('ValidationStatus', 'À valider')
        zone_source = app_zones.get(source, 'INTERNE')
        zone_cible = app_zones.get(cible, 'INTERNE')

        protocole = row['Protocol']
        chiffrement = row.get('Encryption', 'TLS')
        
        # Ajouter des emojis pour le statut de validation
        if validation_status == 'Validé':
            status_display = f"🟢 {validation_status}"
        elif validation_status == 'En cours':
            status_display = f"🟡 {validation_status}"
        else:
            status_display = f"🔴 {validation_status}"
        
        table.append(f"| {source}({zone_source}) | {cible}({zone_cible}) | {protocole} | {chiffrement} | {authentication} | {status_display} |")
    
    return "\n".join(table)

def save_content(content, path):
    """Sauvegarde le contenu dans un fichier"""
    path.write_text(content, encoding='utf-8')
    print(f'📝 {path}')

def export_png(path):
    """Exporte le diagramme en PNG si PlantUML est disponible"""
    cli = shutil.which('plantuml')
    if cli:
        subprocess.run([cli, '-tpng', str(path)], check=False)

def generate_infrastructure_views(xlsx, out_dir=None):
    """Point d'entrée principal"""
    wb = pd.ExcelFile(xlsx)
    flows = wb.parse('Flows')
    apps = wb.parse('Applications')
    
    # Filtrer les flux actifs
    if 'Status' in flows.columns:
        flows = flows[flows['Status'].str.lower() != 'deleted']
    
    # Utiliser le répertoire de sortie fourni ou le répertoire par défaut
    if out_dir:
        diagrams_dir = pathlib.Path(out_dir)
    else:
        diagrams_dir = pathlib.Path('generated/diagrams')
    diagrams_dir.mkdir(parents=True, exist_ok=True)
    
    # Vue Infrastructure
    infra_puml = generate_infrastructure_puml(flows, apps)
    infra_path = diagrams_dir / 'infrastructure_view.puml'
    save_content(infra_puml, infra_path)
    export_png(infra_path)
    
    # Vue Sécurité
    security_puml = generate_security_puml(flows, apps)
    security_path = diagrams_dir / 'security_view.puml'
    save_content(security_puml, security_path)
    export_png(security_path)
    
    # Tableaux
    flows_table = generate_flows_table(flows, apps)
    flows_table_path = diagrams_dir / 'flows_table.md'
    save_content(flows_table, flows_table_path)
    
    security_table = generate_security_table(flows, apps)
    security_table_path = diagrams_dir / 'security_table.md'
    save_content(security_table, security_table_path)
    
    print(f'✅ Vues infrastructure et sécurité générées dans {diagrams_dir}/')

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-i', '--input', default='petstore_archi_v6.xlsx')
    ap.add_argument('-o', '--out', default='diagrams')
    args = ap.parse_args()
    generate_infrastructure_views(pathlib.Path(args.input), pathlib.Path(args.out))