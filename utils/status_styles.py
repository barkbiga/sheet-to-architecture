#!/usr/bin/env python3
"""
Utilitaire pour la gestion des styles de statuts dans les diagrammes PlantUML
"""

def get_status_styles():
    """Retourne les styles PlantUML pour les statuts NEW/CHANGED/UNCHANGED avec couleurs douces"""
    return [
        "' === Styles pour les statuts (couleurs douces et professionnelles) ===",
        "' Configuration pour masquer les étiquettes de stéréotypes",
        "hide stereotype",
        "",
        "' NEW - Vert doux (#2e8b57 - Vert forêt clair)",
        "skinparam rectangle<<NEW>> {",
        "  BackgroundColor #2e8b57",
        "  FontColor white",
        "  BorderColor #5A9934",
        "  FontStyle normal",
        "}",
        "",
        "skinparam component<<NEW>> {",
        "  BackgroundColor #2e8b57",
        "  FontColor white", 
        "  BorderColor #5A9934",
        "  FontStyle normal",
        "}",
        "",
        "skinparam person<<NEW>> {",
        "  BackgroundColor #2e8b57",
        "  FontColor white",
        "  BorderColor #5A9934",
        "  FontStyle normal",
        "}",
        "",
        "skinparam database<<NEW>> {",
        "  BackgroundColor #2e8b57",
        "  FontColor white",
        "  BorderColor #5A9934",
        "  FontStyle normal",
        "}",
        "",
        "skinparam queue<<NEW>> {",
        "  BackgroundColor #2e8b57",
        "  FontColor white",
        "  BorderColor #5A9934",
        "  FontStyle normal",
        "}",
        "",
        "skinparam storage<<NEW>> {",
        "  BackgroundColor #2e8b57",
        "  FontColor white",
        "  BorderColor #5A9934",
        "  FontStyle normal",
        "}",
        "",
        "' CHANGED - Orange doux (#f0e68c - Orange professionnel)",
        "skinparam rectangle<<CHANGED>> {",
        "  BackgroundColor #f0e68c",
        "  FontColor black",
        "  BorderColor #D68910",
        "  FontStyle normal",
        "}",
        "",
        "skinparam component<<CHANGED>> {",
        "  BackgroundColor #f0e68c",
        "  FontColor black",
        "  BorderColor #D68910", 
        "  FontStyle normal",
        "}",
        "",
        "skinparam person<<CHANGED>> {",
        "  BackgroundColor #f0e68c",
        "  FontColor black",
        "  BorderColor #D68910",
        "  FontStyle normal",
        "}",
        "",
        "skinparam database<<CHANGED>> {",
        "  BackgroundColor #f0e68c",
        "  FontColor black",
        "  BorderColor #D68910",
        "  FontStyle normal",
        "}",
        "",
        "skinparam queue<<CHANGED>> {",
        "  BackgroundColor #f0e68c",
        "  FontColor black", 
        "  BorderColor #D68910",
        "  FontStyle normal",
        "}",
        "",
        "skinparam storage<<CHANGED>> {",
        "  BackgroundColor #f0e68c",
        "  FontColor black",
        "  BorderColor #D68910",
        "  FontStyle normal",
        "}",
        "",
        "' UNCHANGED - Bleu gris doux (#5D6D7E - Bleu ardoise)",
        "skinparam rectangle<<UNCHANGED>> {",
        "  BackgroundColor #5D6D7E",
        "  FontColor white",
        "  BorderColor #4A5A6A",
        "}",
        "",
        "skinparam component<<UNCHANGED>> {",
        "  BackgroundColor #5D6D7E",
        "  FontColor white",
        "  BorderColor #4A5A6A",
        "}",
        "",
        "skinparam person<<UNCHANGED>> {",
        "  BackgroundColor #5D6D7E",
        "  FontColor white",
        "  BorderColor #4A5A6A",
        "}",
        "",
        "skinparam database<<UNCHANGED>> {",
        "  BackgroundColor #5D6D7E",
        "  FontColor white",
        "  BorderColor #4A5A6A",
        "}",
        "",
        "skinparam queue<<UNCHANGED>> {",
        "  BackgroundColor #5D6D7E", 
        "  FontColor white",
        "  BorderColor #4A5A6A",
        "}",
        "",
        "skinparam storage<<UNCHANGED>> {",
        "  BackgroundColor #5D6D7E",
        "  FontColor white",
        "  BorderColor #4A5A6A",
        "}",
        "",
        "' === Compatibilité avec anciens statuts ===",
        "",
        "' SaaS + New → NEW",
        "skinparam rectangle<<SaaS>> {",
        "  BackgroundColor #28A745",
        "  FontColor white",
        "  BorderColor #1E7E34",
        "  FontStyle bold",
        "}",
        "",
        "skinparam component<<SaaS>> {",
        "  BackgroundColor #28A745",
        "  FontColor white",
        "  BorderColor #1E7E34", 
        "  FontStyle bold",
        "}",
        "",
        "skinparam rectangle<<New>> {",
        "  BackgroundColor #28A745",
        "  FontColor white",
        "  BorderColor #1E7E34",
        "  FontStyle bold",
        "}",
        "",
        "skinparam component<<New>> {",
        "  BackgroundColor #28A745",
        "  FontColor white",
        "  BorderColor #1E7E34",
        "  FontStyle bold",
        "}",
        "",
        "' Existing → CHANGED",
        "skinparam rectangle<<Existing>> {",
        "  BackgroundColor #FFC107",
        "  FontColor #212529",
        "  BorderColor #E0A800",
        "  FontStyle bold",
        "}",
        "",
        "skinparam component<<Existing>> {",
        "  BackgroundColor #FFC107",
        "  FontColor #212529",
        "  BorderColor #E0A800",
        "  FontStyle bold",
        "}",
        "",
        "' Active → UNCHANGED", 
        "skinparam rectangle<<Active>> {",
        "  BackgroundColor #1168BD",
        "  FontColor white",
        "  BorderColor #0E5A9D",
        "}",
        "",
        "skinparam component<<Active>> {",
        "  BackgroundColor #1168BD",
        "  FontColor white",
        "  BorderColor #0E5A9D",
        "}",
        "",
        "skinparam person<<Active>> {",
        "  BackgroundColor #1168BD",
        "  FontColor white", 
        "  BorderColor #0E5A9D",
        "}",
        ""
    ]

def normalize_status(status):
    """Normalise un statut vers la nouvelle nomenclature"""
    mapping = {
        'SaaS': 'NEW',
        'New': 'NEW', 
        'Existing': 'CHANGED',
        'Active': 'UNCHANGED'
    }
    return mapping.get(status, status)

def generate_component_with_color_only(component_dict, alias):
    """Génère le code PlantUML d'un composant avec couleurs spécifiques SANS stéréotypes"""
    from component_filter import generate_component_puml
    
    # Générer le composant de base
    base_puml = generate_component_puml(component_dict, alias)
    
    # Récupérer le statut et le normaliser
    status = component_dict.get('Status', 'UNCHANGED')
    normalized_status = normalize_status(status)
    
    # Définir les couleurs directement
    color_styles = {
        'NEW': {'bg': '#2e8b57', 'fg': 'white', 'border': '#5A9934'},
        'CHANGED': {'bg': '#f0e68c', 'fg': 'black', 'border': '#D68910'},
        'UNCHANGED': {'bg': '#5D6D7E', 'fg': 'white', 'border': '#4A5A6A'}
    }
    
    colors = color_styles.get(normalized_status, color_styles['UNCHANGED'])
    
    # Ajouter les styles directement sur le composant
    styled_puml = f"{base_puml} #{colors['bg']}"
    
    return styled_puml

def get_component_puml_with_status(component_dict, alias, component_type='rectangle'):
    """Génère le code PlantUML d'un composant avec statut sans mention <<statut>>"""
    from component_filter import generate_component_puml
    
    # Générer le composant de base
    base_puml = generate_component_puml(component_dict, alias)
    
    # Récupérer le statut et le normaliser
    status = component_dict.get('Status', 'UNCHANGED')
    normalized_status = normalize_status(status)
    
    # Modifier le PUML pour inclure le statut sans l'afficher
    # Format: component "Name" as alias <<status>>
    if '<<' not in base_puml:
        # Ajouter le statut
        base_puml = base_puml.replace(f' as {alias}', f' as {alias} <<{normalized_status}>>')
    else:
        # Remplacer le statut existant
        import re
        base_puml = re.sub(r'<<[^>]+>>', f'<<{normalized_status}>>', base_puml)
    
    return base_puml