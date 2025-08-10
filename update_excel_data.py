#!/usr/bin/env python3
"""
Met à jour le fichier Excel avec les nouvelles colonnes et des données de test
"""
import pandas as pd
from pathlib import Path

def create_enhanced_excel():
    """Crée un fichier Excel enrichi avec toutes les nouvelles fonctionnalités"""
    
    # 1. APPLICATIONS - Enrichi avec nouveaux types
    applications_data = [
        # Applications existantes enrichies
        {'ID': 'APP-WEB', 'Name': 'PetStore-Web', 'Type': 'APPLICATION', 'ClientType': None, 'ShowInDiagram': True, 'Department': 'Customer Experience', 'Status': 'New', 'Domain': 'Customer Experience', 'Network_Zone': 'DMZ', 'External': False, 'BusinessApp': 'Bus1', 'Description': 'Interface web principale'},
        {'ID': 'APP-INV', 'Name': 'Inventory-Service', 'Type': 'APPLICATION', 'ClientType': None, 'ShowInDiagram': True, 'Department': 'Supply Chain', 'Status': 'Existing', 'Domain': 'Supply Chain', 'Network_Zone': 'INTERNE', 'External': False, 'BusinessApp': 'Bus2', 'Description': 'Service de gestion des stocks'},
        {'ID': 'APP-PAY', 'Name': 'Payment-Gateway', 'Type': 'APPLICATION', 'ClientType': None, 'ShowInDiagram': True, 'Department': 'Finance', 'Status': 'SaaS', 'Domain': 'Finance', 'Network_Zone': 'PCI', 'External': True, 'BusinessApp': None, 'Description': 'Passerelle de paiement externe'},
        {'ID': 'APP-MOB', 'Name': 'Mobile-App', 'Type': 'APPLICATION', 'ClientType': None, 'ShowInDiagram': True, 'Department': 'Customer Experience', 'Status': 'New', 'Domain': 'Customer Experience', 'Network_Zone': 'DMZ', 'External': False, 'BusinessApp': 'Bus1', 'Description': 'Application mobile'},
        {'ID': 'APP-CAT', 'Name': 'Catalog-Service', 'Type': 'APPLICATION', 'ClientType': None, 'ShowInDiagram': True, 'Department': 'Supply Chain', 'Status': 'Existing', 'Domain': 'Supply Chain', 'Network_Zone': 'INTERNE', 'External': False, 'BusinessApp': 'Bus2', 'Description': 'Service catalogue'},
        {'ID': 'APP-SUP', 'Name': 'Support-Portal', 'Type': 'APPLICATION', 'ClientType': None, 'ShowInDiagram': True, 'Department': 'Support', 'Status': 'New', 'Domain': 'Support', 'Network_Zone': 'DMZ', 'External': False, 'BusinessApp': 'Bus3', 'Description': 'Portail de support'},
        {'ID': 'APP-BILL', 'Name': 'Billing-Service', 'Type': 'APPLICATION', 'ClientType': None, 'ShowInDiagram': True, 'Department': 'Finance', 'Status': 'Existing', 'Domain': 'Finance', 'Network_Zone': 'INTERNE', 'External': False, 'BusinessApp': 'Bus4', 'Description': 'Service facturation'},
        {'ID': 'APP-CRM', 'Name': 'Customer-CRM', 'Type': 'APPLICATION', 'ClientType': None, 'ShowInDiagram': True, 'Department': 'Support', 'Status': 'Existing', 'Domain': 'Support', 'Network_Zone': 'INTERNE', 'External': False, 'BusinessApp': 'Bus3', 'Description': 'Gestion relation client'},
        
        # Nouveaux types pour tests
        {'ID': 'CLI-WEB', 'Name': 'Web Customer', 'Type': 'CLIENT', 'ClientType': 'EndUser', 'ShowInDiagram': True, 'Department': 'External', 'Status': 'Active', 'Domain': 'External', 'Network_Zone': 'EXTERNAL', 'External': True, 'BusinessApp': None, 'Description': 'Client web final'},
        {'ID': 'CLI-PART', 'Name': 'Partner API', 'Type': 'CLIENT', 'ClientType': 'Partner', 'ShowInDiagram': True, 'Department': 'External', 'Status': 'Active', 'Domain': 'External', 'Network_Zone': 'EXTERNAL', 'External': True, 'BusinessApp': None, 'Description': 'API partenaire'},
        {'ID': 'CLI-SYS', 'Name': 'System Monitor', 'Type': 'CLIENT', 'ClientType': 'System', 'ShowInDiagram': False, 'Department': 'IT', 'Status': 'Active', 'Domain': 'Monitoring', 'Network_Zone': 'INTERNE', 'External': False, 'BusinessApp': None, 'Description': 'Monitoring système'},
        
        {'ID': 'TOPIC-ORDER', 'Name': 'Order Events', 'Type': 'TOPIC', 'ClientType': None, 'ShowInDiagram': False, 'Department': 'Infrastructure', 'Status': 'New', 'Domain': 'Messaging', 'Network_Zone': 'INTERNE', 'External': False, 'BusinessApp': None, 'Description': 'Topic événements commandes'},
        {'ID': 'TOPIC-INV', 'Name': 'Inventory Events', 'Type': 'TOPIC', 'ClientType': None, 'ShowInDiagram': False, 'Department': 'Infrastructure', 'Status': 'New', 'Domain': 'Messaging', 'Network_Zone': 'INTERNE', 'External': False, 'BusinessApp': None, 'Description': 'Topic événements stock'},
        
        {'ID': 'DB-USER', 'Name': 'User Database', 'Type': 'DATABASE', 'ClientType': None, 'ShowInDiagram': True, 'Department': 'Infrastructure', 'Status': 'Existing', 'Domain': 'Data', 'Network_Zone': 'INTERNE', 'External': False, 'BusinessApp': None, 'Description': 'Base utilisateurs'},
        {'ID': 'DB-PROD', 'Name': 'Product Database', 'Type': 'DATABASE', 'ClientType': None, 'ShowInDiagram': True, 'Department': 'Infrastructure', 'Status': 'Existing', 'Domain': 'Data', 'Network_Zone': 'INTERNE', 'External': False, 'BusinessApp': None, 'Description': 'Base produits'},
    ]
    
    # 2. FLOWS - Enrichi avec nouveaux types
    flows_data = [
        # Flux synchrones existants
        {'ID': 'FL-01', 'Outbound': 'CLI-WEB', 'Inbound': 'APP-WEB', 'Protocol': 'HTTPS', 'FlowType': 'SYNC', 'AsyncMessage': None, 'Format': 'JSON', 'BusinessProcess': 'Navigation catalogue', 'Status': 'Active', 'Name': 'Navigation catalogue'},
        {'ID': 'FL-02', 'Outbound': 'APP-WEB', 'Inbound': 'APP-PAY', 'Protocol': 'HTTPS', 'FlowType': 'SYNC', 'AsyncMessage': None, 'Format': 'JSON', 'BusinessProcess': 'Traitement paiement', 'Status': 'Active', 'Name': 'Traitement paiement'},
        {'ID': 'FL-03', 'Outbound': 'CLI-WEB', 'Inbound': 'APP-SUP', 'Protocol': 'HTTPS', 'FlowType': 'SYNC', 'AsyncMessage': None, 'Format': 'JSON', 'BusinessProcess': 'Demande support', 'Status': 'Active', 'Name': 'Demande support'},
        
        # Nouveaux flux asynchrones avec topics
        {'ID': 'FL-04', 'Outbound': 'APP-WEB', 'Inbound': 'TOPIC-ORDER', 'Protocol': 'KAFKA', 'FlowType': 'ASYNC', 'AsyncMessage': 'Order Placed Event', 'Format': 'AVRO', 'BusinessProcess': 'Passage commande', 'Status': 'New', 'Name': 'Publication commande'},
        {'ID': 'FL-05', 'Outbound': 'TOPIC-ORDER', 'Inbound': 'APP-INV', 'Protocol': 'KAFKA', 'FlowType': 'ASYNC', 'AsyncMessage': 'Order Placed Event', 'Format': 'AVRO', 'BusinessProcess': 'Passage commande', 'Status': 'New', 'Name': 'Consommation commande'},
        {'ID': 'FL-06', 'Outbound': 'TOPIC-ORDER', 'Inbound': 'APP-BILL', 'Protocol': 'KAFKA', 'FlowType': 'ASYNC', 'AsyncMessage': 'Order Placed Event', 'Format': 'AVRO', 'BusinessProcess': 'Génération facture', 'Status': 'New', 'Name': 'Facturation commande'},
        
        {'ID': 'FL-07', 'Outbound': 'APP-INV', 'Inbound': 'TOPIC-INV', 'Protocol': 'KAFKA', 'FlowType': 'ASYNC', 'AsyncMessage': 'Stock Updated Event', 'Format': 'AVRO', 'BusinessProcess': 'Mise à jour catalogue', 'Status': 'New', 'Name': 'Publication stock'},
        {'ID': 'FL-08', 'Outbound': 'TOPIC-INV', 'Inbound': 'APP-CAT', 'Protocol': 'KAFKA', 'FlowType': 'ASYNC', 'AsyncMessage': 'Stock Updated Event', 'Format': 'AVRO', 'BusinessProcess': 'Mise à jour catalogue', 'Status': 'New', 'Name': 'Mise à jour catalogue'},
        
        # Flux avec bases de données
        {'ID': 'FL-09', 'Outbound': 'APP-WEB', 'Inbound': 'DB-USER', 'Protocol': 'SQL', 'FlowType': 'SYNC', 'AsyncMessage': None, 'Format': 'SQL', 'BusinessProcess': 'Authentification user', 'Status': 'Active', 'Name': 'Authentification user'},
        {'ID': 'FL-10', 'Outbound': 'APP-CAT', 'Inbound': 'DB-PROD', 'Protocol': 'SQL', 'FlowType': 'SYNC', 'AsyncMessage': None, 'Format': 'SQL', 'BusinessProcess': 'Navigation catalogue', 'Status': 'Active', 'Name': 'Lecture produits'},
        
        # Flux partenaires
        {'ID': 'FL-11', 'Outbound': 'CLI-PART', 'Inbound': 'APP-WEB', 'Protocol': 'HTTPS', 'FlowType': 'SYNC', 'AsyncMessage': None, 'Format': 'JSON', 'BusinessProcess': 'Navigation catalogue', 'Status': 'Active', 'Name': 'API partenaire'},
    ]
    
    # 3. CAPABILITIES - Nouveau minimaliste
    capabilities_data = [
        {'ID': 'CAP-001', 'Name': 'Gestion Catalogue', 'Description': 'Capacité de gestion du catalogue produits', 'Domain': 'Supply Chain', 'Level': 'Core', 'Applications': 'APP-CAT,APP-INV'},
        {'ID': 'CAP-002', 'Name': 'Expérience Client', 'Description': 'Capacité d\'interface utilisateur', 'Domain': 'Customer Experience', 'Level': 'Core', 'Applications': 'APP-WEB,APP-MOB'},
        {'ID': 'CAP-003', 'Name': 'Paiement', 'Description': 'Capacité de traitement des paiements', 'Domain': 'Finance', 'Level': 'Supporting', 'Applications': 'APP-PAY,APP-BILL'},
        {'ID': 'CAP-004', 'Name': 'Support Client', 'Description': 'Capacité de support et relation client', 'Domain': 'Support', 'Level': 'Supporting', 'Applications': 'APP-SUP,APP-CRM'},
        {'ID': 'CAP-005', 'Name': 'Data Management', 'Description': 'Capacité de gestion des données', 'Domain': 'Data', 'Level': 'Infrastructure', 'Applications': 'DB-USER,DB-PROD'},
    ]
    
    # 4. VALUE STREAMS - Nouveau minimaliste  
    value_streams_data = [
        {'ID': 'VS-001', 'Name': 'Commande Client', 'Description': 'De la découverte produit à la livraison', 'StartEvent': 'Client browse catalog', 'EndEvent': 'Order delivered', 'Steps': 'Navigation catalogue,Passage commande,Traitement paiement,Génération facture', 'Capabilities': 'CAP-002,CAP-001,CAP-003'},
        {'ID': 'VS-002', 'Name': 'Support Client', 'Description': 'De la demande à la résolution', 'StartEvent': 'Client requests help', 'EndEvent': 'Issue resolved', 'Steps': 'Demande support,Création ticket', 'Capabilities': 'CAP-004,CAP-002'},
        {'ID': 'VS-003', 'Name': 'Gestion Stock', 'Description': 'Mise à jour et synchronisation stock', 'StartEvent': 'Stock change', 'EndEvent': 'Catalog updated', 'Steps': 'Mise à jour catalogue,Calcul coût stock', 'Capabilities': 'CAP-001,CAP-005'},
    ]
    
    # Charger le fichier existant pour garder les autres onglets
    wb = pd.ExcelFile('petstore_archi_optimized.xlsx')
    all_sheets = {}
    
    # Copier les onglets existants sauf Applications et Flows
    for sheet in wb.sheet_names:
        if sheet not in ['Applications', 'Flows']:
            all_sheets[sheet] = wb.parse(sheet)
    
    # Ajouter les nouveaux onglets
    all_sheets['Applications'] = pd.DataFrame(applications_data)
    all_sheets['Flows'] = pd.DataFrame(flows_data)
    all_sheets['Capabilities'] = pd.DataFrame(capabilities_data)
    all_sheets['ValueStreams'] = pd.DataFrame(value_streams_data)
    
    # Écrire le nouveau fichier Excel
    with pd.ExcelWriter('petstore_archi_enhanced.xlsx', engine='openpyxl') as writer:
        for sheet_name, df in all_sheets.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    print("✅ Fichier Excel enrichi créé: petstore_archi_enhanced.xlsx")
    print(f"📊 Nouvelles données:")
    print(f"   - Applications: {len(applications_data)} (dont {len([a for a in applications_data if a['Type']=='CLIENT'])} clients, {len([a for a in applications_data if a['Type']=='TOPIC'])} topics, {len([a for a in applications_data if a['Type']=='DATABASE'])} DB)")
    print(f"   - Flows: {len(flows_data)} (dont {len([f for f in flows_data if f['FlowType']=='ASYNC'])} asynchrones)")
    print(f"   - Capabilities: {len(capabilities_data)}")
    print(f"   - Value Streams: {len(value_streams_data)}")
    
    return 'petstore_archi_enhanced.xlsx'

if __name__ == '__main__':
    create_enhanced_excel()