#!/usr/bin/env python3
"""
Optimisation du fichier Excel en consolidant et supprimant les onglets redondants
"""
import pandas as pd
from pathlib import Path

def optimize_excel(input_file, output_file):
    """Optimise le fichier Excel en consolidant les onglets"""
    
    # Charger le fichier Excel existant
    wb = pd.ExcelFile(input_file)
    
    # Onglets à conserver pour C4 Context (essentiels)
    essential_sheets = {
        'Applications': wb.parse('Applications'),
        'Flows': wb.parse('Flows')
    }
    
    # Onglets à fusionner dans Applications
    applications_df = essential_sheets['Applications'].copy()
    
    # 1. Fusionner External_Actors dans Applications
    if 'External_Actors' in wb.sheet_names:
        external_actors = wb.parse('External_Actors')
        
        # Créer des entrées applications pour les acteurs externes
        for _, actor in external_actors.iterrows():
            if actor['Actor_Type'] == 'External_System':
                # Ajouter comme application externe
                new_app = {
                    'ID': actor['Actor_ID'],
                    'Name': actor['Actor_Name'], 
                    'Department': 'External',
                    'Status': 'SaaS',  # Marquer comme externe
                    'Domain': 'External Systems',
                    'Network_Zone': 'EXTERNAL',
                    'External': True,
                    'Description': actor.get('Description', '')
                }
                applications_df = pd.concat([applications_df, pd.DataFrame([new_app])], ignore_index=True)
    
    # 2. Enrichir avec Context_Mapping si nécessaire
    if 'Context_Mapping' in wb.sheet_names and 'Contexts' in wb.sheet_names:
        context_mapping = wb.parse('Context_Mapping')
        contexts = wb.parse('Contexts')
        
        # Créer un mapping Context_ID -> Context_Name
        context_names = dict(zip(contexts['Context_ID'], contexts['Context_Name']))
        
        # Enrichir Applications avec les contextes (pour domaines plus précis)
        for _, mapping in context_mapping.iterrows():
            app_id = mapping['Application_ID']
            context_id = mapping['Context_ID']
            role = mapping['Role']
            
            if role == 'Primary':  # Utiliser le contexte principal comme domaine
                context_name = context_names.get(context_id, context_id)
                # Mettre à jour le domaine si c'est plus précis
                mask = applications_df['ID'] == app_id
                if mask.any() and context_name != context_id:
                    applications_df.loc[mask, 'Domain'] = context_name
    
    # Nettoyer les doublons
    applications_df = applications_df.drop_duplicates(subset=['ID'], keep='first')
    
    # Onglets complémentaires à garder pour d'autres types de diagrammes
    additional_sheets = {}
    sheets_to_keep = [
        'Project', 'Objectives', 'Constraints',
        'FunctionalReq', 'NFR', 'SecReq',
        'Components', 'Integrations', 'Infra', 'SecurityArch', 'Ops',
        'Data', 'DataClass', 'DataRetention', 'DataGovernance'
    ]
    
    for sheet in sheets_to_keep:
        if sheet in wb.sheet_names:
            additional_sheets[sheet] = wb.parse(sheet)
    
    # Créer le fichier Excel optimisé
    final_sheets = {
        'Applications': applications_df,
        'Flows': essential_sheets['Flows'],
        **additional_sheets
    }
    
    # Écrire le fichier optimisé
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        for sheet_name, df in final_sheets.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    print(f"✅ Fichier Excel optimisé créé: {output_file}")
    print(f"📊 Onglets avant: {len(wb.sheet_names)}")
    print(f"📊 Onglets après: {len(final_sheets)}")
    print(f"🗑️  Onglets supprimés: {len(wb.sheet_names) - len(final_sheets)}")
    
    # Afficher les onglets supprimés
    removed = set(wb.sheet_names) - set(final_sheets.keys())
    if removed:
        print(f"📝 Supprimés: {', '.join(removed)}")

if __name__ == '__main__':
    optimize_excel('petstore_archi_v7.xlsx', 'petstore_archi_optimized.xlsx')