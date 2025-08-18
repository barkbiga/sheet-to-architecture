#!/usr/bin/env python3
"""
Générateur de diagrammes et rapports pour le suivi des formations
"""
import pandas as pd
import argparse
from pathlib import Path
from datetime import datetime
import sys

def generate_training_timeline(df, output_dir):
    """Génère un diagramme de timeline des formations"""
    
    puml_content = """@startuml training_timeline
!theme plain
title Timeline des Formations

"""
    
    # Trier par date de début
    df_sorted = df.sort_values('PlannedStartDate', na_last=True)
    
    current_month = None
    for _, row in df_sorted.iterrows():
        if pd.notna(row['PlannedStartDate']):
            try:
                date = pd.to_datetime(row['PlannedStartDate'])
                month_year = date.strftime('%Y-%m')
                
                if month_year != current_month:
                    puml_content += f"\n== {date.strftime('%B %Y')} ==\n"
                    current_month = month_year
                
                status_color = {
                    'Planifié': '#87CEEB',
                    'En cours': '#FFD700', 
                    'Terminé': '#90EE90',
                    'Reporté': '#FFA500',
                    'Annulé': '#FF6B6B'
                }.get(row['Status'], '#D3D3D3')
                
                puml_content += f": {date.strftime('%d/%m')} - **{row['Subject']}**\\n"
                puml_content += f"  Responsable: {row['Owner']}\\n"
                puml_content += f"  Durée: {row['EstimatedDuration']}h\\n"
                puml_content += f"  Statut: {row['Status']};\n"
                
            except:
                continue
    
    puml_content += "\n@enduml\n"
    
    output_file = output_dir / 'training_timeline.puml'
    output_file.write_text(puml_content, encoding='utf-8')
    print(f"✅ Timeline généré: {output_file}")

def generate_training_dashboard(df, output_dir):
    """Génère un dashboard de suivi des formations"""
    
    # Statistiques
    stats = {
        'total': len(df),
        'by_status': df['Status'].value_counts().to_dict(),
        'by_priority': df['Priority'].value_counts().to_dict(),
        'by_category': df['Category'].value_counts().to_dict(),
        'avg_progress': df[df['Progress'].notna()]['Progress'].mean() if len(df) > 0 else 0
    }
    
    puml_content = f"""@startuml training_dashboard
!theme plain

title Dashboard Formations - {datetime.now().strftime('%d/%m/%Y')}

skinparam rectangle {{
    BackgroundColor lightblue
    BorderColor darkblue
}}

skinparam note {{
    BackgroundColor lightyellow
    BorderColor orange
}}

rectangle "📊 **Vue d'ensemble**" as overview {{
    **Total**: {stats['total']} formations
    **Progression moyenne**: {stats['avg_progress']:.1f}%
}}

"""
    
    # Section statuts
    puml_content += 'rectangle "📋 **Par Statut**" as status {\n'
    for status, count in stats['by_status'].items():
        percentage = (count / stats['total']) * 100 if stats['total'] > 0 else 0
        puml_content += f'  **{status}**: {count} ({percentage:.1f}%)\\n'
    puml_content += '}\n\n'
    
    # Section priorités
    puml_content += 'rectangle "🎯 **Par Priorité**" as priority {\n'
    for priority, count in stats['by_priority'].items():
        percentage = (count / stats['total']) * 100 if stats['total'] > 0 else 0
        puml_content += f'  **{priority}**: {count} ({percentage:.1f}%)\\n'
    puml_content += '}\n\n'
    
    # Section catégories
    puml_content += 'rectangle "📚 **Par Catégorie**" as category {\n'
    for cat, count in stats['by_category'].items():
        percentage = (count / stats['total']) * 100 if stats['total'] > 0 else 0
        puml_content += f'  **{cat}**: {count} ({percentage:.1f}%)\\n'
    puml_content += '}\n\n'
    
    # Formations urgentes
    urgent = df[(df['Priority'].isin(['Critique', 'Haute'])) & (df['Status'].isin(['Planifié', 'En cours']))]
    if not urgent.empty:
        puml_content += 'note as urgent\n'
        puml_content += '  **🚨 Formations urgentes**\n'
        for _, row in urgent.head(5).iterrows():
            puml_content += f'  • {row["Subject"]} ({row["Status"]})\n'
        puml_content += 'end note\n\n'
    
    puml_content += """
overview -[hidden]-> status
status -[hidden]-> priority  
priority -[hidden]-> category

@enduml
"""
    
    output_file = output_dir / 'training_dashboard.puml'
    output_file.write_text(puml_content, encoding='utf-8')
    print(f"✅ Dashboard généré: {output_file}")

def generate_training_matrix(df, output_dir):
    """Génère une matrice formations/composants"""
    
    puml_content = """@startuml training_matrix
!theme plain
title Matrice Formations / Composants

"""
    
    # Extraire les relations formations-composants
    training_components = {}
    for _, row in df.iterrows():
        if pd.notna(row['RelatedComponents']):
            components = [c.strip() for c in str(row['RelatedComponents']).split(',')]
            training_components[row['TrainingID']] = {
                'subject': row['Subject'],
                'components': components,
                'status': row['Status']
            }
    
    # Générer la matrice
    all_components = set()
    for data in training_components.values():
        all_components.update(data['components'])
    
    if all_components:
        puml_content += "package \"Formations\" {\n"
        for training_id, data in training_components.items():
            color = {
                'Planifié': '#87CEEB',
                'En cours': '#FFD700',
                'Terminé': '#90EE90',
                'Reporté': '#FFA500',
                'Annulé': '#FF6B6B'
            }.get(data['status'], '#D3D3D3')
            
            puml_content += f'  ["{training_id}\\n{data["subject"]}"] as {training_id} {color}\n'
        puml_content += "}\n\n"
        
        puml_content += "package \"Composants\" {\n"
        for component in sorted(all_components):
            puml_content += f'  [{component}]\n'
        puml_content += "}\n\n"
        
        # Relations
        for training_id, data in training_components.items():
            for component in data['components']:
                puml_content += f'{training_id} --> [{component}] : forme sur\n'
    
    puml_content += "\n@enduml\n"
    
    output_file = output_dir / 'training_matrix.puml'
    output_file.write_text(puml_content, encoding='utf-8')
    print(f"✅ Matrice généré: {output_file}")

def main():
    parser = argparse.ArgumentParser(description='Générateur de rapports de formation')
    parser.add_argument('-i', '--input', default='petstore_archi_enhanced.xlsx',
                      help='Fichier Excel source')
    parser.add_argument('-o', '--output', default='generated/diagrams',
                      help='Répertoire de sortie')
    parser.add_argument('--timeline', action='store_true',
                      help='Générer timeline des formations')
    parser.add_argument('--dashboard', action='store_true',
                      help='Générer dashboard de suivi')
    parser.add_argument('--matrix', action='store_true',
                      help='Générer matrice formations/composants')
    parser.add_argument('--all', action='store_true',
                      help='Générer tous les diagrammes')
    
    args = parser.parse_args()
    
    excel_file = Path(args.input)
    if not excel_file.exists():
        print(f"❌ Fichier Excel non trouvé: {excel_file}")
        sys.exit(1)
    
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        df = pd.read_excel(excel_file, sheet_name='Training')
        
        if args.all or args.timeline:
            generate_training_timeline(df, output_dir)
        
        if args.all or args.dashboard:
            generate_training_dashboard(df, output_dir)
        
        if args.all or args.matrix:
            generate_training_matrix(df, output_dir)
        
        if not any([args.timeline, args.dashboard, args.matrix, args.all]):
            print("Utilisation:")
            print("  --timeline    Générer timeline des formations")
            print("  --dashboard   Générer dashboard de suivi")  
            print("  --matrix      Générer matrice formations/composants")
            print("  --all         Générer tous les diagrammes")
        
    except Exception as e:
        print(f"❌ Erreur: feuille 'Training' non trouvée. Utilisez d'abord --add-sheet")
        sys.exit(1)

if __name__ == '__main__':
    main()