#!/usr/bin/env python3
"""
Script principal paramétrable pour la génération de diagrammes et documentation
Permet de spécifier quels composants générer via des paramètres
"""
import argparse
import subprocess
import sys
from pathlib import Path

def run_command(cmd, description):
    """Exécute une commande avec gestion d'erreur"""
    print(f"▶ {description}")
    print(f"  {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ Erreur lors de {description}")
        print(f"Sortie d'erreur: {result.stderr}")
        return False
    else:
        print(f"✅ {description} - terminé")
        if result.stdout:
            print(f"  {result.stdout.strip()}")
        return True

def main():
    parser = argparse.ArgumentParser(
        description='Génère des diagrammes et documentation de manière paramétrable',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  %(prog)s --diagrams context infrastructure  # Génère contexte et infrastructure
  %(prog)s --docs architecture security       # Génère doc architecture et sécurité  
  %(prog)s --all                              # Génère tout
  %(prog)s --diagrams all                     # Tous les diagrammes seulement
        """
    )
    
    # Paramètres généraux
    parser.add_argument('-i', '--input', 
                      default='petstore_archi_optimized.xlsx',
                      help='Fichier Excel source (défaut: petstore_archi_optimized.xlsx)')
    parser.add_argument('-o', '--output-diagrams', 
                      help='Répertoire des diagrammes (défaut: generated/diagrams)')
    parser.add_argument('-d', '--output-docs', 
                      help='Répertoire des docs (défaut: generated)')
    parser.add_argument('--output-dir', 
                      help='Répertoire racine de sortie (remplace -o et -d)')
    
    # Options d'affichage des composants
    parser.add_argument('--exclude', nargs='*', 
                      choices=['client', 'application', 'topic', 'database'], 
                      default=[],
                      help='Types de composants à exclure des diagrammes')
    parser.add_argument('--client-types', nargs='*',
                      choices=['EndUser', 'Partner', 'System'],
                      default=['EndUser', 'Partner', 'System'],
                      help='Types de clients à inclure')
    
    # Options de génération
    parser.add_argument('--diagrams', nargs='*', 
                      choices=['context', 'overview', 'infrastructure', 'security', 'process', 'capabilities', 'all'],
                      help='Types de diagrammes à générer')
    parser.add_argument('--docs', nargs='*',
                      choices=['architecture', 'executive', 'infrastructure', 'security', 'technology', 'traceability', 'all'],
                      help='Types de documentation à générer')
    parser.add_argument('--all', action='store_true',
                      help='Génère tous les diagrammes et toute la documentation')
    
    # Options de nettoyage
    parser.add_argument('--clean', action='store_true',
                      help='Nettoie les répertoires de sortie avant génération')
    
    args = parser.parse_args()
    
    # Gestion des répertoires de sortie
    if args.output_dir:
        base_output = Path(args.output_dir)
        output_diagrams = base_output / 'diagrams'
        output_docs = base_output / 'docs'
    else:
        output_diagrams = Path(args.output_diagrams) if args.output_diagrams else Path('generated/diagrams')
        output_docs = Path(args.output_docs) if args.output_docs else Path('generated')
    
    # Vérifier le fichier d'entrée
    input_file = Path(args.input)
    if not input_file.exists():
        print(f"❌ Fichier Excel non trouvé: {input_file}")
        sys.exit(1)
    
    # Créer les répertoires de sortie
    output_diagrams.mkdir(parents=True, exist_ok=True)
    output_docs.mkdir(parents=True, exist_ok=True)
    
    success = True
    
    # Déterminer ce qui doit être généré
    generate_all_diagrams = args.all or (args.diagrams and 'all' in args.diagrams)
    generate_all_docs = args.all or (args.docs and 'all' in args.docs)
    
    diagram_types = []
    if generate_all_diagrams:
        diagram_types = ['context', 'overview', 'infrastructure', 'security', 'process', 'capabilities']
    elif args.diagrams:
        diagram_types = args.diagrams
    
    doc_types = []
    if generate_all_docs:
        doc_types = ['architecture', 'executive', 'infrastructure', 'security', 'technology', 'traceability']
    elif args.docs:
        doc_types = args.docs
    
    # Nettoyage si demandé
    if args.clean:
        print("🧹 Nettoyage des répertoires de sortie...")
        import shutil
        if output_diagrams.exists():
            shutil.rmtree(output_diagrams)
            output_diagrams.mkdir(parents=True)
        if output_docs.exists():
            for file in output_docs.glob('*.md'):
                file.unlink()
    
    # Génération des diagrammes
    if diagram_types:
        print(f"\n📊 Génération des diagrammes: {', '.join(diagram_types)}")
        
        # Préparer les options communes pour les générateurs
        generator_options = []
        if args.exclude:
            generator_options.extend(['--exclude'] + args.exclude)
        if args.client_types != ['EndUser', 'Partner', 'System']:
            generator_options.extend(['--client-types'] + args.client_types)
        
        if 'context' in diagram_types:
            cmd = ['python3', 'generators/generate_context_diagram.py', '-i', str(input_file), '-o', str(output_diagrams)] + generator_options
            success &= run_command(cmd, "Diagrammes de contexte C4")
        
        if any(t in diagram_types for t in ['overview', 'process']):
            cmd = ['python3', 'generators/generate_diagrams.py', '-i', str(input_file), '-o', str(output_diagrams)] + generator_options
            success &= run_command(cmd, "Diagrammes d'aperçu et processus")
        
        if any(t in diagram_types for t in ['infrastructure', 'security']):
            cmd = ['python3', 'generators/generate_infrastructure_diagrams.py', '-i', str(input_file), '-o', str(output_diagrams)] + generator_options
            success &= run_command(cmd, "Diagrammes infrastructure et sécurité")
        
        if 'capabilities' in diagram_types:
            cmd = ['python3', 'generators/generate_capabilities_diagram.py', '-i', str(input_file), '-o', str(output_diagrams)]
            success &= run_command(cmd, "Diagrammes de capacités et value streams")
    
    # Génération de la documentation
    if doc_types:
        print(f"\n📝 Génération de la documentation: {', '.join(doc_types)}")
        
        # Le script build_docs.py génère toute la documentation
        # On peut l'appeler avec des paramètres pour filtrer
        cmd = ['python3', 'scripts/build_docs.py', '-i', str(input_file), '-o', str(output_docs)]
        success &= run_command(cmd, "Documentation complète")
        
        # Filtrage post-génération si nécessaire
        if not generate_all_docs and doc_types:
            print("📄 Filtrage des documents générés...")
            all_docs = {
                'architecture': ['architecture.md', 'architecture_complete.md'],
                'executive': ['executive_summary.md'],
                'infrastructure': ['infrastructure_view.md'],
                'security': ['security_view.md'],
                'technology': ['technology_view.md'],
                'traceability': ['traceability_matrix.md']
            }
            
            # Supprimer les docs non demandés
            for doc_type, files in all_docs.items():
                if doc_type not in doc_types:
                    for file in files:
                        file_path = output_docs / file
                        if file_path.exists():
                            file_path.unlink()
                            print(f"  🗑️  Supprimé: {file}")
    
    # Résumé final
    print("\n" + "="*60)
    if success:
        print("✅ Génération terminée avec succès!")
        print(f"📊 Diagrammes: {output_diagrams}")
        print(f"📝 Documents: {output_docs}")
        
        # Afficher les fichiers générés
        if output_diagrams.exists():
            diagrams = list(output_diagrams.glob('*'))
            print(f"   {len(diagrams)} diagrammes générés")
        
        if output_docs.exists():
            docs = list(output_docs.glob('*.md'))
            print(f"   {len(docs)} documents générés")
    else:
        print("❌ Certaines étapes ont échoué")
        sys.exit(1)

if __name__ == '__main__':
    main()