#!/usr/bin/env python3
"""
Utilitaires pour filtrer et styliser les composants selon leur type
"""
import pandas as pd

def load_applications_with_types(df):
    """Charge les applications en ajoutant les colonnes de type si manquantes"""
    # Valeurs par défaut si colonnes manquantes  
    if 'Type' not in df.columns:
        df['Type'] = 'APPLICATION'
    if 'ClientType' not in df.columns:
        df['ClientType'] = 'System'
    if 'ShowInDiagram' not in df.columns:
        df['ShowInDiagram'] = True
    if 'External' not in df.columns:
        df['External'] = False
    
    # Définir les valeurs par défaut pour les valeurs manquantes
    df['ClientType'] = df['ClientType'].fillna('System').infer_objects(copy=False)
    df['External'] = df['External'].fillna(False).infer_objects(copy=False)
        
    return df

def load_flows_with_types(df):
    """Charge les flux en ajoutant les colonnes de type si manquantes"""
    if 'FlowType' not in df.columns:
        df['FlowType'] = 'SYNC'
    if 'AsyncMessage' not in df.columns:
        df['AsyncMessage'] = None
        
    return df

def filter_applications(apps_df, exclude_types=None, client_types=None):
    """Filtre les applications selon les types à exclure et inclure"""
    if exclude_types is None:
        exclude_types = []
    if client_types is None:
        client_types = ['EndUser', 'Partner', 'System']
    
    # Exclure les types spécifiés
    if exclude_types:
        exclude_types_upper = [t.upper() for t in exclude_types]
        apps_df = apps_df[~apps_df['Type'].str.upper().isin(exclude_types_upper)]
    
    # Filtrer les types de clients si des clients sont présents
    if 'CLIENT' not in [t.upper() for t in exclude_types]:
        client_mask = (apps_df['Type'].str.upper() != 'CLIENT') | (apps_df['ClientType'].isin(client_types))
        apps_df = apps_df[client_mask]
    
    return apps_df

def aggregate_async_flows(flows_df, apps_df, excluded_types):
    """Agrège les flux asynchrones quand les topics sont exclus"""
    if 'topic' not in [t.lower() for t in excluded_types]:
        return flows_df
    
    # Identifier les topics
    topic_ids = apps_df[apps_df['Type'].str.upper() == 'TOPIC']['ID'].tolist()
    if not topic_ids:
        return flows_df
    
    aggregated_flows = []
    processed_flows = set()
    
    for topic_id in topic_ids:
        # Flux entrants vers le topic
        inbound_flows = flows_df[flows_df['Inbound'] == topic_id]
        # Flux sortants du topic  
        outbound_flows = flows_df[flows_df['Outbound'] == topic_id]
        
        # Créer des flux directs APP -> APP
        for _, in_flow in inbound_flows.iterrows():
            for _, out_flow in outbound_flows.iterrows():
                # Éviter les doublons
                flow_key = (in_flow['Outbound'], out_flow['Inbound'])
                if flow_key not in processed_flows:
                    async_message = in_flow.get('AsyncMessage', in_flow.get('Name', 'Async'))
                    
                    aggregated_flows.append({
                        'ID': f"ASYNC_{in_flow['Outbound']}_{out_flow['Inbound']}",
                        'Outbound': in_flow['Outbound'],
                        'Inbound': out_flow['Inbound'],
                        'Protocol': 'ASYNC',
                        'FlowType': 'ASYNC',
                        'Name': f"Async {async_message}",
                        'BusinessProcess': in_flow.get('BusinessProcess', ''),
                        'Status': in_flow.get('Status', ''),
                        'AsyncMessage': async_message
                    })
                    processed_flows.add(flow_key)
    
    # Supprimer les flux impliquant les topics
    filtered_flows = flows_df[
        ~flows_df['Outbound'].isin(topic_ids) & 
        ~flows_df['Inbound'].isin(topic_ids)
    ]
    
    # Ajouter les flux agrégés
    if aggregated_flows:
        aggregated_df = pd.DataFrame(aggregated_flows)
        filtered_flows = pd.concat([filtered_flows, aggregated_df], ignore_index=True)
    
    return filtered_flows

def generate_component_styles():
    """Génère les styles PlantUML pour différents types de composants"""
    return '''
' Styles pour les différents types de composants
skinparam person {
    BackgroundColor #87CEEB
    FontColor black
    BorderColor #4682B4
}

skinparam rectangle<<client>> {
    BackgroundColor #98FB98
    FontColor black
    BorderColor #32CD32
}

skinparam database {
    BackgroundColor #FFB6C1
    FontColor black
    BorderColor #DC143C
}

skinparam queue {
    BackgroundColor #DDA0DD
    FontColor black
    BorderColor #9932CC
}

skinparam rectangle<<application>> {
    BackgroundColor #1168BD
    FontColor white
    BorderColor #0E5A9D
}

skinparam rectangle<<external>> {
    BackgroundColor #999999
    FontColor white
    BorderColor #8A8A8A
}

skinparam rectangle<<cache>> {
    BackgroundColor #FF6347
    FontColor white
    BorderColor #DC143C
}

skinparam storage {
    BackgroundColor #32CD32
    FontColor white
    BorderColor #228B22
}
'''

def generate_component_puml(app, app_id):
    """Génère le code PlantUML pour un composant selon son type SANS tags de statut"""
    app_type = app.get('Type', 'APPLICATION').upper()
    name = app.get('Name', app.get('ID', 'Unknown'))
    is_external = app.get('Status') == 'SaaS' or app.get('External', False)
    
    if app_type == 'CLIENT':
        client_type = app.get('ClientType', 'EndUser')
        if client_type == 'EndUser':
            return f'person "{name}" as {app_id}'
        else:
            return f'rectangle "{name}" as {app_id}'
    elif app_type == 'DATABASE':
        return f'database "{name}" as {app_id}'
    elif app_type == 'TOPIC':
        return f'queue "{name}" as {app_id}'
    elif app_type == 'FILESTORAGE':
        return f'storage "{name}" as {app_id}'
    elif app_type == 'CACHE':
        return f'rectangle "{name}" as {app_id}'
    else:  # APPLICATION
        return f'rectangle "{name}" as {app_id}'

def generate_flow_puml(flow, source_id, target_id):
    """Génère le code PlantUML pour un flux selon son type"""
    flow_type = flow.get('FlowType', 'SYNC').upper()
    name = flow.get('Name', '')
    
    if flow_type == 'ASYNC':
        # Flèche pointillée pour async
        return f'{source_id} ..> {target_id} : "{name}"'
    else:
        # Flèche normale pour sync
        return f'{source_id} --> {target_id} : "{name}"'