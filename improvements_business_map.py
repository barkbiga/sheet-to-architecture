#!/usr/bin/env python3
"""
Améliorations suggérées pour la business app map
"""

def generate_improved_business_app_diagram(data):
    """Version améliorée du diagramme business app"""
    apps_df = data.get('applications', pd.DataFrame())
    
    if apps_df.empty:
        return None
    
    puml = ["@startuml business_apps_map"]
    puml.append("!theme plain")
    puml.append("")
    puml.append("title 📊 Cartographie des Applications par Domaine Métier")
    puml.append("")
    
    # === AMÉLIORATION 1: Styles simplifiés et contrastés ===
    puml.append("' === Styles optimisés pour la lisibilité ===")
    puml.append("skinparam rectangle<<NEW>> {")
    puml.append("  BackgroundColor #28A745")  # Vert plus vif
    puml.append("  FontColor white")
    puml.append("  BorderColor #1E7E34")
    puml.append("  FontStyle bold")
    puml.append("}")
    puml.append("")
    
    puml.append("skinparam rectangle<<EXISTING>> {")
    puml.append("  BackgroundColor #FFC107")  # Orange plus visible
    puml.append("  FontColor #212529") 
    puml.append("  BorderColor #E0A800")
    puml.append("  FontStyle bold")
    puml.append("}")
    puml.append("")
    
    puml.append("skinparam rectangle<<SAAS>> {")
    puml.append("  BackgroundColor #17A2B8")  # Cyan pour SaaS
    puml.append("  FontColor white")
    puml.append("  BorderColor #138496")
    puml.append("  FontStyle bold")
    puml.append("}")
    puml.append("")
    
    # === AMÉLIORATION 2: Packages avec domaines métier explicites ===
    puml.append("skinparam package {")
    puml.append("  BackgroundColor #F8F9FA")
    puml.append("  BorderColor #495057")
    puml.append("  BorderThickness 3")
    puml.append("  FontStyle bold")
    puml.append("  FontSize 14")
    puml.append("  FontColor #212529")
    puml.append("}")
    puml.append("")
    
    # === AMÉLIORATION 3: Optimisations d'affichage ===
    puml.append("skinparam minClassWidth 150")  # Plus large
    puml.append("skinparam packageStyle rectangle")
    puml.append("skinparam shadowing false")
    puml.append("skinparam componentStyle rectangle")
    puml.append("skinparam maxMessageSize 50")
    puml.append("")
    
    # === AMÉLIORATION 4: Organisation intelligente par domaine ===
    if 'Type' in apps_df.columns:
        filtered_apps = apps_df[apps_df['Type'] == 'APPLICATION'].copy()
    else:
        filtered_apps = apps_df.copy()
    
    if filtered_apps.empty:
        puml.append("note as N1 #FFEAA7")
        puml.append("  ⚠️ Aucune application trouvée")
        puml.append("  Vérifiez les données Excel")
        puml.append("end note")
    else:
        # Créer un mapping domaine → nom lisible
        domain_mapping = {
            'Bus1': '🛍️ Expérience Client',
            'Bus2': '📦 Supply Chain', 
            'Bus3': '🎧 Support Client',
            'Bus4': '💰 Finance',
            'Non défini': '🔧 Services Transverses'
        }
        
        # Grouper par domaine métier
        if 'BusinessApp' in filtered_apps.columns:
            filtered_apps_copy = filtered_apps.copy()
            filtered_apps_copy['BusinessApp'] = filtered_apps_copy['BusinessApp'].fillna('Non défini')
            business_apps = filtered_apps_copy.groupby('BusinessApp', dropna=False)
            
            # === AMÉLIORATION 5: Disposition adaptative ===
            domains = list(business_apps)
            
            # Organiser en grille 2x2 ou adaptative selon le nombre
            if len(domains) <= 4:
                # Disposition 2x2 optimale
                for i in range(0, len(domains), 2):
                    domain1_key, apps_group1 = domains[i]
                    domain1_name = domain_mapping.get(domain1_key, domain1_key)
                    
                    if i + 1 < len(domains):
                        domain2_key, apps_group2 = domains[i + 1]
                        domain2_name = domain_mapping.get(domain2_key, domain2_key)
                        
                        # Deux domaines côte à côte
                        generate_domain_package(puml, domain1_name, apps_group1)
                        generate_domain_package(puml, domain2_name, apps_group2)
                        
                        if i + 2 < len(domains):  # Pas dernière ligne
                            puml.append("")
                            puml.append("' === Ligne suivante ===")
                            puml.append("")
                    else:
                        # Dernier domaine seul
                        generate_domain_package(puml, domain1_name, apps_group1)
            else:
                # Disposition en ligne pour plus de 4 domaines
                for domain_key, apps_group in business_apps:
                    domain_name = domain_mapping.get(domain_key, domain_key)
                    generate_domain_package(puml, domain_name, apps_group)
        
        # === AMÉLIORATION 6: Légende des statuts ===
        puml.append("")
        puml.append("' === Légende ===")
        puml.append("legend bottom")
        puml.append("  |= Statut |= Description |")
        puml.append("  | <back:#28A745><color:white><b> NEW </b></color></back> | Nouvelle application |")
        puml.append("  | <back:#FFC107><color:#212529><b> EXISTING </b></color></back> | Application existante |") 
        puml.append("  | <back:#17A2B8><color:white><b> SAAS </b></color></back> | Service externe |")
        puml.append("endlegend")
    
    puml.append("")
    puml.append("@enduml")
    return "\n".join(puml)

def generate_domain_package(puml, domain_name, apps_group):
    """Génère un package de domaine avec applications optimisées"""
    puml.append(f'package "{domain_name}" {{')
    
    # Trier les applications par nom
    apps_sorted = apps_group.sort_values('Name')
    for _, app in apps_sorted.iterrows():
        app_name = app.get('Name', app.get('ID', 'Unknown'))
        app_alias = app['ID'].replace('-', '_')
        
        # Raccourcir les noms trop longs
        if len(app_name) > 20:
            app_display = app_name[:17] + "..."
        else:
            app_display = app_name
            
        # Status normalisé
        status = normalize_status_simple(app.get('Status', 'EXISTING'))
        
        # Description courte si disponible  
        description = app.get('Description', '')
        if description and len(description) > 0:
            tooltip = f'\\n<i>{description[:30]}...</i>' if len(description) > 30 else f'\\n<i>{description}</i>'
            app_display += tooltip
        
        puml.append(f'  rectangle "{app_display}" as {app_alias} <<{status}>>')
    
    puml.append('}')
    puml.append("")

def normalize_status_simple(status):
    """Normalisation simplifiée des statuts"""
    if not status or pd.isna(status):
        return 'EXISTING'
    
    status_str = str(status).upper().strip()
    
    if status_str in ['NEW', 'NOUVEAU']:
        return 'NEW'
    elif status_str in ['SAAS', 'SaaS', 'EXTERNAL', 'EXTERNE']:
        return 'SAAS' 
    else:
        return 'EXISTING'