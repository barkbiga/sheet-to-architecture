#!/usr/bin/env python3
"""
Génération automatique de diagrammes de contexte PlantUML
"""
import pandas as pd
import argparse
from pathlib import Path
import sys
import os

# Ajouter le répertoire utils au chemin Python
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
from component_filter import (
    load_applications_with_types, load_flows_with_types,
    filter_applications, aggregate_async_flows,
    generate_component_styles, generate_component_puml, generate_flow_puml
)

def load_data(excel_file, exclude_types=None, client_types=None):
    """Charge les données depuis le fichier Excel avec filtrage"""
    wb = pd.ExcelFile(excel_file)
    data = {}
    
    # Chargement des onglets nécessaires pour C4 Context
    for sheet in ['Applications', 'Flows']:
        if sheet in wb.sheet_names:
            df = wb.parse(sheet)
            if sheet == 'Applications':
                df = load_applications_with_types(df)
                df = filter_applications(df, exclude_types, client_types)
            elif sheet == 'Flows':
                df = load_flows_with_types(df)
            data[sheet.lower()] = df
        else:
            data[sheet.lower()] = pd.DataFrame()
    
    # Agréger les flux asynchrones si nécessaire
    if exclude_types and data['applications'] is not None and data['flows'] is not None:
        data['flows'] = aggregate_async_flows(data['flows'], data['applications'], exclude_types)
    
    return data

# Fonctions supprimées - utiliser uniquement C4 Context

def create_subdomains_by_zone(apps_df):
    """Crée des sous-domaines quand un domaine traverse plusieurs zones réseau"""
    subdomains = {}
    
    # Ajouter une valeur par défaut pour les zones manquantes avec warning
    if 'Network_Zone' not in apps_df.columns:
        print("⚠️  WARNING: Colonne 'Network_Zone' manquante, utilisation de 'INTERNE' par défaut")
        apps_df = apps_df.copy()
        apps_df['Network_Zone'] = 'INTERNE'
    else:
        # Remplacer les valeurs null par défaut avec warning
        missing_zones = apps_df['Network_Zone'].isna().sum()
        if missing_zones > 0:
            missing_apps = apps_df[apps_df['Network_Zone'].isna()]['ID'].tolist()
            print(f"⚠️  WARNING: {missing_zones} applications sans zone réseau: {', '.join(missing_apps[:5])}{'...' if len(missing_apps) > 5 else ''}")
            print("   → Utilisation de 'INTERNE' par défaut")
            apps_df = apps_df.copy()
            apps_df['Network_Zone'] = apps_df['Network_Zone'].fillna('INTERNE')
    
    for domain in apps_df['Domain'].dropna().unique():
        domain_apps = apps_df[apps_df['Domain'] == domain]
        zones = domain_apps['Network_Zone'].unique()
        # Filtrer les zones null/NaN
        zones = [z for z in zones if pd.notna(z)]
        
        if len(zones) > 1:
            # Créer des sous-domaines par zone
            for zone in zones:
                subdomain_id = f"{domain}_{zone}"
                zone_apps = domain_apps[domain_apps['Network_Zone'] == zone]
                subdomains[subdomain_id] = {
                    'name': f"{domain} {zone}",
                    'original_domain': domain,
                    'zone': zone,
                    'apps': zone_apps,
                    'is_subdomain': True
                }
        else:
            # Garder le domaine unique
            default_zone = zones[0] if len(zones) > 0 else 'INTERNE'
            subdomains[domain] = {
                'name': domain,
                'original_domain': domain, 
                'zone': default_zone,
                'apps': domain_apps,
                'is_subdomain': False
            }
    
    return subdomains

def aggregate_flows_by_subdomains(flows_df, apps_df, subdomains):
    """Agrège les flux par paire de sous-domaines (incluant flux intra-domaine)"""
    # Créer un mapping ID -> Subdomain
    app_to_subdomain = {}
    for subdomain_id, subdomain_info in subdomains.items():
        for _, app in subdomain_info['apps'].iterrows():
            app_to_subdomain[app['ID']] = subdomain_id
    
    # Grouper les flux par paire source-target de sous-domaines
    subdomain_flows = {}
    
    for _, flow in flows_df.iterrows():
        source_subdomain = app_to_subdomain.get(flow['Outbound'])
        target_subdomain = app_to_subdomain.get(flow['Inbound'])
        
        # Inclure TOUS les flux (même intra-domaine si différentes zones)
        if source_subdomain and target_subdomain and source_subdomain != target_subdomain:
            flow_key = (source_subdomain, target_subdomain)
            
            if flow_key not in subdomain_flows:
                subdomain_flows[flow_key] = []
                
            # Utiliser la colonne Name ou BusinessProcess
            flow_name = flow.get('Name', flow.get('BusinessProcess', flow.get('ID', 'Flow')))
            if flow_name not in subdomain_flows[flow_key]:  # Éviter les doublons
                subdomain_flows[flow_key].append(flow_name)
    
    return subdomain_flows

def generate_c4_context_diagram(data):
    """Génère un diagramme C4 Context avec sous-domaines par zone réseau"""
    apps_df = data['applications']
    flows_df = data['flows']
    
    # Créer les sous-domaines par zone
    subdomains = create_subdomains_by_zone(apps_df)
    
    # Agréger les flux par sous-domaines
    subdomain_flows = aggregate_flows_by_subdomains(flows_df, apps_df, subdomains)
    
    
    puml = ["@startuml c4_context"]
    puml.append("!theme plain")
    puml.append("")
    puml.append("' Définitions des styles C4")
    puml.append("skinparam {")
    puml.append("  defaultFontSize 12")
    puml.append("  defaultFontName Arial")
    puml.append("}")
    puml.append("")
    puml.append("skinparam person {")
    puml.append("  BackgroundColor #08427B")
    puml.append("  FontColor white")
    puml.append("  BorderColor #073B6F")
    puml.append("}")
    puml.append("")
    puml.append("skinparam rectangle {")
    puml.append("  BackgroundColor #1168BD")
    puml.append("  FontColor white")
    puml.append("  BorderColor #0E5A9D")
    puml.append("}")
    puml.append("")
    puml.append("skinparam rectangle<<external>> {")
    puml.append("  BackgroundColor #999999")
    puml.append("  FontColor white")
    puml.append("  BorderColor #8A8A8A")
    puml.append("}")
    puml.append("")
    puml.append("' Zones réseau avec bordures pointillées")
    puml.append("skinparam rectangle<<zone>> {")
    puml.append("  BorderStyle dashed")
    puml.append("  BackgroundColor transparent")
    puml.append("  FontStyle bold")
    puml.append("  FontSize 14")
    puml.append("  BorderColor #666666")
    puml.append("}")
    puml.append("")
    puml.append("title Diagramme C4 - Contexte par Zones Réseau")
    puml.append("")
    puml.append("' Optimisations d'affichage")
    puml.append("!define RECTANGLE class")
    puml.append("skinparam minClassWidth 150")
    puml.append("skinparam packageStyle rectangle")
    puml.append("skinparam shadowing false")
    puml.append("")
    
    # Personnes/Acteurs
    puml.append("person \"Customer\" as customer")
    puml.append("note top of customer : End user")
    puml.append("")
    
    # Grouper les sous-domaines par zone réseau
    zones_domains = {}
    subdomain_ids = {}
    for subdomain_id, subdomain_info in subdomains.items():
        zone = subdomain_info['zone']
        if zone not in zones_domains:
            zones_domains[zone] = []
        
        # Créer un ID PlantUML valide
        plantuml_id = subdomain_id.lower().replace(' ', '_').replace('-', '_')
        subdomain_ids[subdomain_id] = plantuml_id
        
        zones_domains[zone].append((subdomain_id, subdomain_info, plantuml_id))
    
    # Générer les zones avec les domaines à l'intérieur
    for zone, domain_list in zones_domains.items():
        zone_id = f"zone_{zone.lower()}"
        
        # Utiliser package pour avoir un titre centré en haut
        puml.append(f'package "Zone {zone}" as {zone_id} <<zone>> {{')
        
        for subdomain_id, subdomain_info, plantuml_id in domain_list:
            name = subdomain_info['name']
            
            # Vérifier si c'est externe (basé sur les apps SaaS de ce sous-domaine)
            is_external = False
            if 'Status' in subdomain_info['apps'].columns:
                is_external = any(subdomain_info['apps']['Status'].fillna('') == 'SaaS')
            
            if is_external:
                puml.append(f'  rectangle "{name}" as {plantuml_id} <<external>>')
            else:
                puml.append(f'  rectangle "{name}" as {plantuml_id}')
        
        puml.append('}')
    
    puml.append("")
    
    # Relations utilisateur vers sous-domaines orientés client
    customer_patterns = ['Customer Experience', 'Customer  Experience']
    for subdomain_id, subdomain_info in subdomains.items():
        original_domain = subdomain_info['original_domain']
        if any(pattern in original_domain for pattern in customer_patterns):
            plantuml_id = subdomain_ids[subdomain_id]
            puml.append(f'customer --> {plantuml_id} : Uses')
    
    puml.append("")
    
    # Relations entre sous-domaines (flux agrégés sans numérotation)
    for (source_subdomain, target_subdomain), flow_names in subdomain_flows.items():
        source_id = subdomain_ids.get(source_subdomain)
        target_id = subdomain_ids.get(target_subdomain)
        
        if source_id and target_id:
            # Concaténer les noms des flux avec des retours à la ligne
            if len(flow_names) > 1:
                flow_content = '\\n'.join(flow_names)
                flow_label = f'"{flow_content}"'
            else:
                flow_label = f'"{flow_names[0]}"'
                
            puml.append(f'{source_id} --> {target_id} : {flow_label}')
    
    puml.append("")
    puml.append("@enduml")
    
    return "\n".join(puml)

def main():
    parser = argparse.ArgumentParser(description='Génère le diagramme de contexte C4')
    parser.add_argument('-i', '--input', default='petstore_archi_optimized.xlsx', help='Fichier Excel source')
    parser.add_argument('-o', '--output', default='generated/diagrams', help='Répertoire de sortie')
    
    # Options de filtrage des composants
    parser.add_argument('--exclude', nargs='*', 
                      choices=['client', 'application', 'topic', 'database'], 
                      default=[],
                      help='Types de composants à exclure des diagrammes')
    parser.add_argument('--client-types', nargs='*',
                      choices=['EndUser', 'Partner', 'System'],
                      default=['EndUser', 'Partner', 'System'],
                      help='Types de clients à inclure')
    
    args = parser.parse_args()
    
    # Charger les données avec filtrage
    data = load_data(args.input, args.exclude, args.client_types)
    
    # Créer le répertoire de sortie
    output_dir = Path(args.output)
    output_dir.mkdir(exist_ok=True)
    
    # Générer uniquement le diagramme C4 Context
    c4_puml = generate_c4_context_diagram(data)
    (output_dir / 'c4_context.puml').write_text(c4_puml, encoding='utf-8')
    print(f"📝 {output_dir}/c4_context.puml")
    
    print("✅ Diagramme de contexte C4 généré")

if __name__ == '__main__':
    main()