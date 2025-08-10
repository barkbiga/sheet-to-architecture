#!/usr/bin/env python3
"""
Générateur de diagrammes de capacités métier et value streams
"""
import pandas as pd
import argparse
from pathlib import Path

def load_data(excel_file):
    """Charge les données capabilities et value streams"""
    wb = pd.ExcelFile(excel_file)
    data = {}
    
    for sheet in ['Capabilities', 'ValueStreams', 'Applications']:
        if sheet in wb.sheet_names:
            data[sheet.lower()] = wb.parse(sheet)
        else:
            data[sheet.lower()] = pd.DataFrame()
    
    return data

def generate_capabilities_map(data):
    """Génère une carte des capacités par domaine"""
    capabilities_df = data.get('capabilities', pd.DataFrame())
    
    if capabilities_df.empty:
        return None
    
    puml = ["@startuml capabilities_map"]
    puml.append("!theme plain")
    puml.append("")
    puml.append("title Cartographie des Capacités Métier")
    puml.append("")
    
    # Styles par niveau de capacité
    puml.append("skinparam rectangle<<core>> {")
    puml.append("  BackgroundColor #E8F5E8")
    puml.append("  BorderColor #2E8B2E")
    puml.append("  FontStyle bold")
    puml.append("}")
    puml.append("")
    puml.append("skinparam rectangle<<supporting>> {")
    puml.append("  BackgroundColor #FFF8DC")
    puml.append("  BorderColor #DAA520")
    puml.append("}")
    puml.append("")
    puml.append("skinparam rectangle<<infrastructure>> {")
    puml.append("  BackgroundColor #F0F8FF")
    puml.append("  BorderColor #4682B4")
    puml.append("}")
    puml.append("")
    
    # Grouper par domaine
    domains = capabilities_df.groupby('Domain')
    
    for domain, caps in domains:
        puml.append(f'package "{domain}" {{')
        
        for _, cap in caps.iterrows():
            level = cap['Level'].lower() if pd.notna(cap['Level']) else 'supporting'
            cap_id = cap['ID'].replace('-', '_')
            puml.append(f'  rectangle "{cap["Name"]}" as {cap_id} <<{level}>>')
        
        puml.append('}')
        puml.append("")
    
    puml.append("@enduml")
    return "\n".join(puml)

def generate_value_stream_diagram(data):
    """Génère un diagramme de value stream"""
    vs_df = data.get('valuestreams', pd.DataFrame())
    
    if vs_df.empty:
        return None
    
    puml = ["@startuml value_streams"]
    puml.append("!theme plain")
    puml.append("")
    puml.append("title Value Streams")
    puml.append("")
    
    # Styles pour les value streams
    puml.append("skinparam activity {")
    puml.append("  BackgroundColor #FFE4B5")
    puml.append("  BorderColor #CD853F")
    puml.append("}")
    puml.append("")
    
    for _, vs in vs_df.iterrows():
        puml.append(f"partition \"{vs['Name']}\" {{")
        puml.append(f"  start")
        puml.append(f"  :{vs['StartEvent']};")
        
        # Étapes du value stream
        if pd.notna(vs['Steps']):
            steps = [step.strip() for step in vs['Steps'].split(',')]
            for step in steps:
                puml.append(f"  :{step};")
        
        puml.append(f"  :{vs['EndEvent']};")
        puml.append(f"  stop")
        puml.append("}")
        puml.append("")
    
    puml.append("@enduml")
    return "\n".join(puml)

def generate_capability_to_application_matrix(data):
    """Génère une matrice capacités -> applications"""
    capabilities_df = data.get('capabilities', pd.DataFrame())
    applications_df = data.get('applications', pd.DataFrame())
    
    if capabilities_df.empty:
        return None
    
    puml = ["@startuml capability_app_matrix"]
    puml.append("!theme plain")
    puml.append("")
    puml.append("title Matrice Capacités → Applications")
    puml.append("")
    
    # Style pour les capacités et applications
    puml.append("skinparam rectangle<<capability>> {")
    puml.append("  BackgroundColor #E8F5E8")
    puml.append("  BorderColor #2E8B2E")
    puml.append("}")
    puml.append("")
    puml.append("skinparam rectangle<<application>> {")
    puml.append("  BackgroundColor #F0F8FF")
    puml.append("  BorderColor #4682B4")
    puml.append("}")
    puml.append("")
    
    # Créer un mapping app_id -> app_name
    app_names = {}
    if not applications_df.empty:
        app_names = dict(zip(applications_df['ID'], applications_df['Name']))
    
    for _, cap in capabilities_df.iterrows():
        cap_id = cap['ID'].replace('-', '_')
        puml.append(f'rectangle "{cap["Name"]}" as {cap_id} <<capability>>')
        
        # Applications liées
        if pd.notna(cap['Applications']):
            app_ids = [app_id.strip() for app_id in cap['Applications'].split(',')]
            for app_id in app_ids:
                app_name = app_names.get(app_id, app_id)
                app_alias = app_id.replace('-', '_')
                puml.append(f'rectangle "{app_name}" as {app_alias} <<application>>')
                puml.append(f'{cap_id} --> {app_alias}')
        
        puml.append("")
    
    puml.append("@enduml")
    return "\n".join(puml)

def main():
    parser = argparse.ArgumentParser(description='Génère les diagrammes de capacités et value streams')
    parser.add_argument('-i', '--input', default='petstore_archi_enhanced.xlsx', help='Fichier Excel source')
    parser.add_argument('-o', '--output', default='generated/diagrams', help='Répertoire de sortie')
    
    args = parser.parse_args()
    
    # Charger les données
    data = load_data(args.input)
    
    # Créer le répertoire de sortie
    output_dir = Path(args.output)
    output_dir.mkdir(exist_ok=True, parents=True)
    
    generated_files = []
    
    # Génération des diagrammes
    capabilities_map = generate_capabilities_map(data)
    if capabilities_map:
        (output_dir / 'capabilities_map.puml').write_text(capabilities_map, encoding='utf-8')
        generated_files.append('capabilities_map.puml')
    
    value_streams = generate_value_stream_diagram(data)
    if value_streams:
        (output_dir / 'value_streams.puml').write_text(value_streams, encoding='utf-8')
        generated_files.append('value_streams.puml')
    
    capability_matrix = generate_capability_to_application_matrix(data)
    if capability_matrix:
        (output_dir / 'capability_app_matrix.puml').write_text(capability_matrix, encoding='utf-8')
        generated_files.append('capability_app_matrix.puml')
    
    # Afficher les résultats
    for file in generated_files:
        print(f"📝 {output_dir}/{file}")
    
    if generated_files:
        print("✅ Diagrammes de capacités et value streams générés")
    else:
        print("⚠️  Aucune donnée de capacités trouvée")

if __name__ == '__main__':
    main()