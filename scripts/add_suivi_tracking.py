#!/usr/bin/env python3
"""
Script pour ajouter le suivi des sujets à instruire
Ajoute une feuille Training dans le fichier Excel
"""
import pandas as pd
import openpyxl
from pathlib import Path
import sys
from datetime import datetime

def add_training_sheet(excel_file):
    """Ajoute la feuille Training au fichier Excel"""
    
    # Structure des colonnes pour le suivi des sujets
    suivi_columns = {
        'SuiviID': 'ID unique du sujet à instruire',
        'Subject': 'Sujet à instruire',
        'Description': 'Description détaillée du sujet',
        'Category': 'Catégorie (Technique, Fonctionnel, Sécurité, Processus)',
        'Priority': 'Priorité (Critique, Haute, Moyenne, Basse)',
        'Status': 'Statut (Planifié, En cours, Terminé, Reporté, Annulé)',
        'Owner': 'Responsable de la formation',
        'Trainers': 'Formateurs assignés',
        'Trainees': 'Participants ciblés',
        'TargetAudience': 'Public cible (Développeur, Ops, Business)',
        'EstimatedDuration': 'Durée estimée (heures)',
        'PlannedStartDate': 'Date de début prévue',
        'PlannedEndDate': 'Date de fin prévue',
        'ActualStartDate': 'Date de début réelle',
        'ActualEndDate': 'Date de fin réelle',
        'Prerequisites': 'Prérequis',
        'Materials': 'Matériel de formation',
        'DeliveryMethod': 'Mode de livraison (Présentiel, Virtuel, E-learning)',
        'Location': 'Lieu ou plateforme',
        'Notes': 'Notes et commentaires',
        'RelatedComponents': 'Composants liés',
        'RelatedProcesses': 'Processus liés',
        'CompletionCriteria': 'Critères de validation',
        'FeedbackScore': 'Score de satisfaction',
        'NextActions': 'Actions de suivi'
    }
    
    # Données d'exemple
    sample_data = [
        {
            'SuiviID': 'SUI-001',
            'Subject': 'Architecture microservices',
            'Description': 'Instruction sur les principes et bonnes pratiques des microservices',
            'Category': 'Technique',
            'Priority': 'Haute',
            'Status': 'Planifié',
            'Owner': 'Architecte Lead',
            'Instructors': 'Expert Architecture',
            'TargetTeam': 'Équipe développement',
            'TargetAudience': 'Développeur',
            'EstimatedDuration': 16,
            'PlannedStartDate': '2024-09-01',
            'PlannedEndDate': '2024-09-15',
            'Prerequisites': 'Connaissance Java/Spring',
            'Materials': 'Documentation, Labs pratiques',
            'DeliveryMethod': 'Présentiel',
            'Location': 'Salle formation A',
            'Notes': 'Sujet critique pour nouveau projet',
            'RelatedComponents': 'UserService, OrderService',
            'RelatedProcesses': 'Passage commande',
            'CompletionCriteria': 'Quiz + Projet pratique',
            'FeedbackScore': '',
            'NextActions': 'Programmer sessions pratiques'
        },
        {
            'SuiviID': 'SUI-002',
            'Subject': 'Sécurité API REST',
            'Description': 'Instruction sur la sécurisation des APIs REST',
            'Category': 'Sécurité',
            'Priority': 'Critique',
            'Status': 'En cours',
            'Owner': 'RSSI',
            'Instructors': 'Expert Sécurité',
            'TargetTeam': 'Développeurs Backend',
            'TargetAudience': 'Développeur',
            'EstimatedDuration': 8,
            'PlannedStartDate': '2024-08-15',
            'PlannedEndDate': '2024-08-22',
            'ActualStartDate': '2024-08-15',
            'Prerequisites': 'Connaissance APIs REST',
            'Materials': 'Documentation OWASP',
            'DeliveryMethod': 'Virtuel',
            'Location': 'Teams',
            'Notes': 'Sujet obligatoire avant MEP',
            'RelatedComponents': 'AuthService, GatewayAPI',
            'RelatedProcesses': 'Authentification user',
            'CompletionCriteria': 'Audit sécurité réussi',
            'FeedbackScore': '',
            'NextActions': 'Tests sécurité sur APIs'
        }
    ]
    
    try:
        # Charger le fichier Excel existant
        with pd.ExcelWriter(excel_file, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            # Créer le DataFrame avec les données d'exemple
            df = pd.DataFrame(sample_data)
            
            # Écrire dans la feuille Suivi
            df.to_excel(writer, sheet_name='Suivi', index=False)
            
            # Accéder au workbook pour formater
            workbook = writer.book
            worksheet = writer.sheets['Suivi']
            
            # Ajuster la largeur des colonnes
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width
            
            # Appliquer des styles
            from openpyxl.styles import Font, PatternFill, Border, Side
            
            # Style pour l'en-tête
            header_font = Font(bold=True, color="FFFFFF")
            header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
            
            for cell in worksheet[1]:
                cell.font = header_font
                cell.fill = header_fill
            
            # Ajouter une feuille de documentation
            doc_data = pd.DataFrame([
                ['Suivi', 'Feuille principale de suivi des sujets à instruire'],
                ['SuiviID', 'Identifiant unique (format: SUI-XXX)'],
                ['Status', 'Valeurs: Planifié, En cours, Terminé, Reporté, Annulé'],
                ['Priority', 'Valeurs: Critique, Haute, Moyenne, Basse'],
                ['Category', 'Valeurs: Technique, Fonctionnel, Sécurité, Processus'],
                ['TargetAudience', 'Valeurs: Développeur, Ops, Business, Manager'],
                ['DeliveryMethod', 'Valeurs: Présentiel, Virtuel, E-learning, Hybride'],
                ['FeedbackScore', 'Score de 1 à 5 étoiles']
            ], columns=['Champ', 'Description/Valeurs'])
            
            doc_data.to_excel(writer, sheet_name='Suivi_Doc', index=False)
            
        print(f"✅ Feuille Suivi ajoutée avec succès à {excel_file}")
        print(f"📋 {len(sample_data)} exemples de sujets d'instruction créés")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'ajout de la feuille Suivi: {e}")
        return False

def generate_training_report(excel_file, output_file=None):
    """Génère un rapport de suivi des formations"""
    try:
        df = pd.read_excel(excel_file, sheet_name='Training')
        
        if output_file is None:
            output_file = 'generated/training_report.md'
        
        # Créer le répertoire de sortie
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        
        # Statistiques
        stats = {
            'total': len(df),
            'by_status': df['Status'].value_counts().to_dict(),
            'by_priority': df['Priority'].value_counts().to_dict(),
            'by_category': df['Category'].value_counts().to_dict(),
            'in_progress': len(df[df['Status'] == 'En cours']),
            'completed': len(df[df['Status'] == 'Terminé']),
            'avg_progress': df[df['Progress'].notna()]['Progress'].mean() if 'Progress' in df.columns else 0
        }
        
        # Générer le rapport Markdown
        report = f"""# Rapport de Suivi des Formations

*Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}*

## Vue d'ensemble

- **Total des sujets**: {stats['total']}
- **En cours**: {stats['in_progress']}
- **Terminés**: {stats['completed']}
- **Progression moyenne**: {stats['avg_progress']:.1f}%

## Répartition par statut

"""
        for status, count in stats['by_status'].items():
            percentage = (count / stats['total']) * 100
            report += f"- **{status}**: {count} ({percentage:.1f}%)\n"

        report += f"""
## Répartition par priorité

"""
        for priority, count in stats['by_priority'].items():
            percentage = (count / stats['total']) * 100
            report += f"- **{priority}**: {count} ({percentage:.1f}%)\n"

        report += f"""
## Répartition par catégorie

"""
        for category, count in stats['by_category'].items():
            percentage = (count / stats['total']) * 100
            report += f"- **{category}**: {count} ({percentage:.1f}%)\n"

        # Formations en cours
        in_progress = df[df['Status'] == 'En cours']
        if not in_progress.empty:
            report += f"""
## Formations en cours

| ID | Sujet | Responsable | Progression | Date fin prévue |
|---|---|---|---|---|
"""
            for _, row in in_progress.iterrows():
                report += f"| {row['TrainingID']} | {row['Subject']} | {row['Owner']} | {row['Progress']}% | {row['PlannedEndDate']} |\n"

        # Formations à venir
        planned = df[df['Status'] == 'Planifié']
        if not planned.empty:
            report += f"""
## Formations planifiées

| ID | Sujet | Priorité | Date début | Responsable |
|---|---|---|---|---|
"""
            for _, row in planned.iterrows():
                report += f"| {row['TrainingID']} | {row['Subject']} | {row['Priority']} | {row['PlannedStartDate']} | {row['Owner']} |\n"

        # Écrire le rapport
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"✅ Rapport généré: {output_file}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération du rapport: {e}")
        return False

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Gestionnaire de suivi des formations')
    parser.add_argument('-i', '--input', default='petstore_archi_enhanced.xlsx',
                      help='Fichier Excel à modifier')
    parser.add_argument('--add-sheet', action='store_true',
                      help='Ajouter la feuille Training')
    parser.add_argument('--report', action='store_true',
                      help='Générer un rapport de suivi')
    parser.add_argument('-o', '--output', 
                      help='Fichier de sortie pour le rapport')
    
    args = parser.parse_args()
    
    excel_file = Path(args.input)
    if not excel_file.exists():
        print(f"❌ Fichier Excel non trouvé: {excel_file}")
        sys.exit(1)
    
    success = True
    
    if args.add_sheet:
        success &= add_training_sheet(excel_file)
    
    if args.report:
        success &= generate_training_report(excel_file, args.output)
    
    if not args.add_sheet and not args.report:
        print("Utilisation:")
        print("  python scripts/add_training_tracking.py --add-sheet    # Ajouter feuille Training")
        print("  python scripts/add_training_tracking.py --report       # Générer rapport")
        print("  python scripts/add_training_tracking.py --add-sheet --report  # Tout faire")
    
    if not success:
        sys.exit(1)

if __name__ == '__main__':
    main()