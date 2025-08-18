#!/usr/bin/env python3
"""
Générateur de diagramme de regroupement des applications par BusinessApp
"""
import pandas as pd
import argparse
from pathlib import Path
import sys
import os

# Ajouter le répertoire utils au chemin Python
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
from component_filter import generate_component_puml, generate_component_styles
from status_styles import get_status_styles, normalize_status, generate_component_with_color_only

def load_data(excel_file):
    """Charge les données applications"""
    wb = pd.ExcelFile(excel_file)
    data = {}
    
    if 'Applications' in wb.sheet_names:
        data['applications'] = wb.parse('Applications')
    else:
        data['applications'] = pd.DataFrame()
    
    return data

def generate_business_app_diagram(data):
    """Génère un diagramme de regroupement des applications par BusinessApp"""
    apps_df = data.get('applications', pd.DataFrame())
    
    if apps_df.empty:
        return None
    
    puml = ["@startuml business_apps_map"]
    puml.append("!theme plain")
    puml.append("")
    puml.append("title 📊 Cartographie des Applications par Domaine Métier")
    puml.append("")
    
    # Styles unifiés pour tous les statuts - couleurs douces
    status_styles = get_status_styles()
    puml.extend(status_styles)
    
    # Style pour les packages de domaines métier - optimisé
    puml.append("skinparam package {")
    puml.append("  BackgroundColor #F8F9FA")
    puml.append("  BorderColor #495057")
    puml.append("  BorderThickness 2")
    puml.append("  FontStyle bold")
    puml.append("  FontSize 13")
    puml.append("  FontColor #212529")
    puml.append("}")
    puml.append("")
    
    # Optimisations d'affichage
    puml.append("skinparam minClassWidth 150")
    puml.append("skinparam packageStyle rectangle") 
    puml.append("skinparam shadowing false")
    puml.append("skinparam componentStyle rectangle")
    puml.append("")
    
    # Filtrer uniquement les applications (exclure clients, databases, topics)
    if 'Type' in apps_df.columns:
        filtered_apps = apps_df[apps_df['Type'] == 'APPLICATION'].copy()
    else:
        filtered_apps = apps_df.copy()
    
    if filtered_apps.empty:
        puml.append("note as N1")
        puml.append("  Aucune application trouvée")
        puml.append("end note")
    else:
        # Mapping des noms de domaines pour plus de clarté
        domain_mapping = {
            'Bus1': '🛍️ Expérience Client',
            'Bus2': '📦 Supply Chain', 
            'Bus3': '🎧 Support Client',
            'Bus4': '💰 Finance',
            'Non défini': '🔧 Services Transverses'
        }
        
        # Grouper par BusinessApp avec disposition optimisée (2 par ligne)
        if 'BusinessApp' in filtered_apps.columns:
            # Remplacer les NaN par 'Non défini' avant le groupby
            filtered_apps_copy = filtered_apps.copy()
            filtered_apps_copy['BusinessApp'] = filtered_apps_copy['BusinessApp'].fillna('Non défini')
            business_apps = filtered_apps_copy.groupby('BusinessApp', dropna=False)
            business_apps_list = list(business_apps)
            
            # Organiser en lignes de 2 business apps
            for i in range(0, len(business_apps_list), 2):
                # Première business app de la ligne
                bus_app1, apps_group1 = business_apps_list[i]
                bus_app_key1 = bus_app1 if pd.notna(bus_app1) and bus_app1 != '' else 'Non défini'
                bus_app_name1 = domain_mapping.get(bus_app_key1, bus_app_key1)
                
                # Deuxième business app de la ligne (si elle existe)
                if i + 1 < len(business_apps_list):
                    bus_app2, apps_group2 = business_apps_list[i + 1]  
                    bus_app_key2 = bus_app2 if pd.notna(bus_app2) and bus_app2 != '' else 'Non défini'
                    bus_app_name2 = domain_mapping.get(bus_app_key2, bus_app_key2)
                    
                    # Créer deux packages côte à côte
                    puml.append(f'package "{bus_app_name1}" {{')
                    
                    # Apps de la première business app
                    apps_sorted1 = apps_group1.sort_values('Name')
                    for _, app in apps_sorted1.iterrows():
                        app_alias = app['ID'].replace('-', '_')
                        status = normalize_status(app.get('Status', 'UNCHANGED'))
                        component_puml = generate_component_puml(app.to_dict(), app_alias)
                        component_puml = component_puml.replace(f' as {app_alias}', f' as {app_alias} <<{status}>>')
                        puml.append(f'  {component_puml}')
                    
                    puml.append('}')
                    puml.append("")
                    
                    puml.append(f'package "{bus_app_name2}" {{')
                    
                    # Apps de la deuxième business app  
                    apps_sorted2 = apps_group2.sort_values('Name')
                    for _, app in apps_sorted2.iterrows():
                        app_alias = app['ID'].replace('-', '_')
                        status = normalize_status(app.get('Status', 'UNCHANGED'))
                        component_puml = generate_component_puml(app.to_dict(), app_alias)
                        component_puml = component_puml.replace(f' as {app_alias}', f' as {app_alias} <<{status}>>')
                        puml.append(f'  {component_puml}')
                    
                    puml.append('}')
                    puml.append("")
                    
                    # Ajout d'un saut de ligne pour améliorer la disposition
                    puml.append("' --- Ligne suivante ---")
                    
                else:
                    # Dernière business app seule
                    puml.append(f'package "{bus_app_name1}" {{')
                    
                    apps_sorted1 = apps_group1.sort_values('Name')
                    for _, app in apps_sorted1.iterrows():
                        app_alias = app['ID'].replace('-', '_')
                        status = normalize_status(app.get('Status', 'UNCHANGED'))
                        component_puml = generate_component_puml(app.to_dict(), app_alias)
                        component_puml = component_puml.replace(f' as {app_alias}', f' as {app_alias} <<{status}>>')
                        puml.append(f'  {component_puml}')
                    
                    puml.append('}')
                    puml.append("")
        else:
            # Fallback si pas de colonne BusinessApp
            puml.append("note as N1")
            puml.append("  Colonne BusinessApp non trouvée")
            puml.append("end note")
    
    # Ajouter une légende pour les statuts
    puml.append("")
    puml.append("' === Légende des statuts ===")
    puml.append("legend bottom")
    puml.append("  |= Statut |= Description |")
    puml.append("  | <back:#2e8b57><color:white><b> NEW </b></color></back> | Nouvelle application |")
    puml.append("  | <back:#f0e68c><color:black><b> EXISTING </b></color></back> | Application existante |") 
    puml.append("  | <back:#28A745><color:white><b> SAAS </b></color></back> | Service externe |")
    puml.append("endlegend")
    
    puml.append("")
    puml.append("@enduml")
    return "\n".join(puml)

def main():
    parser = argparse.ArgumentParser(description='Génère le diagramme de regroupement des applications par BusinessApp')
    parser.add_argument('-i', '--input', default='petstore_archi_enhanced.xlsx', help='Fichier Excel source')
    parser.add_argument('-o', '--output', default='generated/diagrams', help='Répertoire de sortie')
    
    args = parser.parse_args()
    
    # Charger les données
    data = load_data(args.input)
    
    # Créer le répertoire de sortie
    output_dir = Path(args.output)
    output_dir.mkdir(exist_ok=True, parents=True)
    
    # Génération du diagramme
    business_app_diagram = generate_business_app_diagram(data)
    if business_app_diagram:
        (output_dir / 'business_apps_map.puml').write_text(business_app_diagram, encoding='utf-8')
        print(f"📝 {output_dir}/business_apps_map.puml")
        print("✅ Diagramme de regroupement BusinessApp généré")
    else:
        print("⚠️  Aucune donnée d'applications trouvée")

if __name__ == '__main__':
    main()