import streamlit as st
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import calendar
from calendar import monthrange

# Monthly consumption data
electricity = pd.DataFrame({'Month': ['january','february','march','april','may','june','july','august','september','october','november','december'],
                                 'Consumption': [127000, 124000, 123000, 122000, 169000, 229000, 224000, 225000, 226000, 187000, 125000, 129000]})
gas = pd.DataFrame({'Month': ['january','february','march','april','may','june','july','august','september','october','november','december'],
                         'Consumption': [48347, 48250, 48340, 44500, 42500, 31700, 31500, 31400, 37000, 47500, 48500, 48000]})
water = pd.DataFrame({'Month': ['january','february','march','april','may','june','july','august','september','october','november','december'],
                           'Consumption': [75, 75, 77, 78, 77, 80, 82, 85, 82, 81, 86, 75]})


# Function to generate random daily consumption data for each month
def generate_daily_consumption(months, mean_consumption, std_dev):
    data = {}
    for month in months:
        year = 2023
        num_days = monthrange(year, list(calendar.month_name).index(month.capitalize()))[1]  # Get the number of days in the month
        data[month] = np.random.normal(mean_consumption, std_dev, num_days).astype(int)
    return data

# Calculate daily consumption
electricity_daily = {key: value.tolist() for key, value in generate_daily_consumption(electricity['Month'], mean_consumption=4000, std_dev=1000).items()}
gas_daily = {key: value.tolist() for key, value in generate_daily_consumption(gas['Month'], mean_consumption=2000, std_dev=500).items()}
water_daily = {key: value.tolist() for key, value in generate_daily_consumption(water['Month'], mean_consumption=50, std_dev=10).items()}

consumption_data = {'Electricity': electricity_daily,'Gas':gas_daily,'Water': water_daily}

import datetime
st.set_option('deprecation.showPyplotGlobalUse', False)

# Replace with your Heroku app URL

# Tarifs unitaires en euros/kWh
unit_costs = {'electricity': 0.27, 'gas': 0.0913, 'water': 4.34}

# Calculer le coût total de la consommation en euros pour chaque ressource
def calculate_total_cost(consumption_data):
    total_cost = {}
    for resource, data in consumption_data.items():
        total_cost[resource] = sum(item['Consumption'] for item in data) * unit_costs[resource]
    return total_cost

# Créer un diagramme circulaire à partir des totaux de coût
def plot_pie_chart(total_cost):
    labels = list(total_cost.keys())
    sizes = list(total_cost.values())

    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    st.pyplot()

 # Visualiser les relevés de conso Enertiques
def visualize_consumption(data):
    selected_option = st.selectbox('Select Visualization', ['Monthly Consumption','Annual Consumption'])
    selected_resource = st.selectbox('Select Resource', ['Electricity','Gas','Water'])
    
    if selected_option == 'Monthly Consumption':
        selected_month = st.selectbox('Select Month', sorted(list(data[selected_resource].keys())))
        max_days = len(data[selected_resource][selected_month])
        interval = st.slider('Select Interval (in days)', 1, max_days, max_days)
        
        plt.plot(range(interval), data[selected_resource][selected_month][:interval])
        plt.xlabel('Day')
        plt.ylabel('Consumption')
        plt.title(f'{selected_resource} Consumption in {selected_month}')
        st.pyplot()
    
    elif selected_option == 'Annual Consumption':
      
       # Données
        months_data = data[selected_resource]
        # Liste des mois
        months = list(months_data.keys())
        
        # Trier les mois en utilisant datetime.strptime pour obtenir le mois numérique
        sorted_months = sorted(months, key=lambda x: datetime.datetime.strptime(x, '%B').month)
        
        
        month_index_map = {month: index+1 for index, month in enumerate(list(sorted_months))}
                                                                        
        start_month, end_month = st.slider('Select Months Range', 1, 12, (1, 12))
        
        start_month_name = list(month_index_map.keys())[start_month]
        
        end_month_name = list(month_index_map.keys())[end_month-1]

                
        start_index = month_index_map[start_month_name]
        end_index = month_index_map[end_month_name]
        
               
        # Trier les données de consommation selon l'ordre des mois
        sorted_consumptions = [months_data[month] for month in sorted_months]
        # Extraire les mois triés et les consommations associées
           
        # Somme de consommation pour chaque mois
        consumptions = [sum(data) for data in sorted_consumptions]
        # Création du graphique à barres
                
        plt.figure(figsize=(10, 6))
        plt.bar(sorted_months, consumptions, color='skyblue')  # Largeur de la barre ajustée

        # Ajout des titres et labels
        plt.title(f'Annual {selected_resource} Consumption')
        plt.xlabel('Mois')
        plt.ylabel('Consommation')
        plt.xticks(rotation=45, ha='right')  # Rotation des labels sur l'axe x pour une meilleure lisibilité

        # Affichage du graphique
        st.pyplot()


def main():
    menu = ['Introduction','Environnement_d_un_Projet Smart Building','Audit Energie + Deploiement Iot','Solutions Iot + Plan Comptage','Bilan Conso Energies(Elec/Gaz/Eau)',"Diagnostic Performance Energétique","Bilan GES(Gaz à effet de serre)"," Axes d'amélioration identifiés",'Visu Suivi des KPI Conso(Elec/Gaz/Eau)','Visu objectifs Réduction Conso Energies','Info + contacts utiles sites']
    st.sidebar.markdown("<h1 style='font-weight: bold;'>Menu</h1>", unsafe_allow_html=True)
    choice=st.sidebar.selectbox(" ",menu)
    if choice=="Introduction":
       st.markdown(''' ## Démarche de mise en oeuvre d'un cabinet de conseil spécialisé en stratégie de management  Data ,Energie ,Environnement et Maintenance  en faveur de la transition écologique en France et dans le monde ! ''') 
       st.markdown(f"<u><h4><b> Promoteur du projet: </u></h4></b>", unsafe_allow_html=True)
       st.markdown(''' ######  Qui suis je? Je suis Landry Didier GAMASSA,mon parcours et experiences me présentent, comme un Data Scientist,Spécialiste en Energie,Ingénieur Génaraliste en Génie Electrique de l'Université des Sciences et Technologies de Lille ,Chef Projet Senior AMOA de l'Institut Poly Informatique de Paris ,Expert Asset Maintenance et Management des Cycles de vie des ouvrages technologiques dans tout secteur industriel .Très admiratif des grands batisseurs de notre planète,je milite pour des innovations technologiques respectueuses de l'environnement et au service du bien etre de l'humanité .''')    
       st.markdown(f"<u><h4><b> Genèse du projet: </u></h4></b>", unsafe_allow_html=True)
       st.markdown('''###### Projet laissé en jachère  par le Docteur Alain Pensé GAMASSA qui n'est plus de ce monde mais tenait à transmettre le témoin de son engagement écologique en faveur de la protection de notre planète à l'un de ses proches. En 2017, son ONG, engagée dans la lutte contre les changements climatiques, va déléguer Landry Didier GAMASSA comme réprésentant à la Conférence de la Terre qui se tenait du 6 au 17 Novembre 2017 à Bonn en Allemagne.15000 scientifiques,décideurs économiques et leaders politiques du monde y étaient conviés pour débattre sur les moyens de lutte contre les  changements climatiques.Il était apparu que la trajectoire de maintien du rechauffement de la planète à 1.5°C par rapport l'ére pré-industrielle, convenue à la conférence du climat de Paris ,présentait des écarts qui exigeaient des mesures contraignantes envers les pays les plus pollueurs de notre planète.Cette Conférence organisée sous l'initiative du PNUE (Programme des Nations Unies pour l’Environnement) étayait encore une fois la gravité des dégats causés depuis la révolution industrielle  par les activités humaines sur notre planète.2017 à 2024 ,le temps,les rencontres et les expériences bonnes ou mauvaises  ont bati les fondations de ce projet.''' )
       st.markdown(f"<u><h4><b> Contexte et enjeux liés aux gaz à effet de serre: </u></h4></b>", unsafe_allow_html=True)
       st.markdown(''' ######  En France, le secteur de l'immobilier tertiaire se classe au deuxième rang des émetteurs de gaz à effet de serre. Dès le 1er janvier 2025, le décret BACS obligera les acteurs de ce secteur, qu'ils soient propriétaires ou locataires, à poursuivre des objectifs de réduction drastique de leur consommation énergétique. Depuis la signature de l'Accord de Paris sur le climat, la transition écologique et énergétique en France a ouvert un marché colossal, composé de plusieurs milliards de mètres carrés de bâtiments nécessitant des audits approfondis. Ce marché appelle à la mobilisation de tous les acteurs capables d'apporter des solutions innovantes.
''') 
       st.markdown(f"<u><h4><b> Evaluation des problématiques de consommation d'énergie des batiments tertiaires: </u></h4></b>", unsafe_allow_html=True)
       st.markdown(''' ######  1.Je vous présente le Campus Technologique d'Orange,un modèle de site tertiaire qui m'a permis d'évaluer les besoins énergétiques d'un hypersite professionnel  de 70000 mètres carrés de surfaces de bureaux cumulés  et d'autre part leurs impacts environnementaux ''') 
       st.video('https://youtu.be/ivZyb9hcd-8?si=tS4MExQDdEO5m5rx') 
       st.markdown(''' ######  2.A partir de 4 Postes Haute Tension HTA/BT 20000 Volts/400 Volts Triphasé ,le campus Technologique d'Orange est équipé des systèmes énergétiques de dernière génération dont les performances énergétiques peuvent encore etre optimisées par le suivi en temps réel des consommations electriques de son parc matériel composé de la liste non exhaustive des équipements énergivores suivants: ''')                                                        
       st.markdown(''' ######  >> 3000 Ventilo-convecteurs pour le chauffage et climatisation des bureaux ''')
       st.markdown(''' ######  >> 40 Centrales de traitement d'air''') 
       st.markdown(''' ######  >> 50 Ascenceurs OTIS ''')
       st.markdown(''' ######  >> 25000 lampes  à peu près pour l'éclairage du site''' )
       st.markdown(''' ######  La liste non exhaustive  des équipements mentionnés ci-dessus  vous présente une ville dans une ville et j'y ai officié en qualité de Responsable Energie et Maintenance.''')                                  
       st.markdown(f"<u><h4><b> Solutions de reduction des consommations d'énergie dans le secteur de l'immobilier tertiaire: </u></h4></b>", unsafe_allow_html=True)
       st.markdown(''' ###### Les solutions se déclinent en deux axes''')
       st.markdown(''' ###### 1. Axe reglementaire: Le Gouvernement fait recours  aux decrets reglementaires afin d'accélérer le processus de decarbonation du secteur de l'immobilier tertiaire''')
       st.markdown(''' ###### 2. Axe technologique: Les technologies Iot sont les meilleurs alliés de la transition écologique. Des capteurs discrets reliés à des plateformes IoT permettent aux acteurs de suivre en temps reel leurs consommations énergétiques''')                                                                                                                             
       st.markdown(f"<u><h4><b> Stratégie de developpement: </u></h4></b>", unsafe_allow_html=True)
       st.markdown(''' ######  Afin de mieux accompagner nos futurs clients ,notre démarche se déclinera en deux axes stratégiques:''')
       st.markdown(''' ######  1.D'une part,mettre la Data au coeur du pilotage de l'Energie ,de l'Environnement et de la Maintenance du parc matériel de tout site tertiaire. C'est ce qui se fait déja mais nos prestations s'effectuerons avec l'expertise des professionnels ayant des compétences reconnues en Management Data ,Energie ,Environnement et Maintenance que nous accompagnerons nos futurs clients''')                                                                
       st.markdown(''' ######  2.D'autre part, de par des milliards de mètres carrés de surface à auditer, promouvoir un partenariat gagnant-gagnant avec des cabinets reconnus dans le secteur du Conseil et Management de l'Energie tels que CITRON ou IQSPOT. ''')
       st.markdown(f"<u><h4><b> Contact: </u></h4></b>", unsafe_allow_html=True)
       st.markdown(''' ###### Mon contact mail: dgamassa.thermo@orange.fr ''')
       st.markdown(''' ###### Une citation très célèbre:<<La persistance est la force la plus puissante sur terre ,elle peut déplacer des montagnes . J'y ajouterais ceci:<< L'intelligence collective ou en réseau  peut aussi déplacer des montagnes et peut etre accélératrice des projets complexes.Et enfin ,le socle d'un projet est constitué d'une part  de belles idées et d'autre part  de belles finances!Je reste à l'écoute principalement de vos conseils en financement.Le business plan est ficelé ,les fournisseurs d'instruments IOT sélectionnés et ne reste plus qu'à trouver les meilleures solutions de financement pour que cette démarche se concrétise en un grand pas vers une planète de plus en plus  verte.!!''' )
       st.markdown(f"<u><h4><b> 2017_Congo-Brazzaville : Cérémonie d'Hommage au Docteur Alain Pensé GAMASSA: </u></h4></b>", unsafe_allow_html=True)
       url1='https://youtu.be/HG3E4GKHu2g?si=vTK307XMF-Spjt0c'
       st.markdown(f'<a href="{url1}" target="_blank">{"Cliquez ici pour visualiser "}</a>', unsafe_allow_html=True)
       
       
       if choice=="Environnement_d_un_Projet Smart Building":         
        st.title('Environnement d un Projet Smart Building')
        
        if st.button("Enjeux de la reduction de la consommations énergétique en France"):
            st.text("Quelles sont les villes les plus consommatrices d’énergie en France ?") 
            st.text(" Fréjus dans le Var                                   3.15Mwh/habitant")
            st.text(" Narbonne en Occitanie                                2.77Mwh/habitant")
            st.text(" La Rochelle en Nouvelle-Aquitaine                    2.08Mwh/habitant")
            st.text(" Issy Les Moulineaux dans les Hauts de Seine 92       2.05Mwh/habitant")
            st.text(" Paris en Ile de France                               1.85Mwh/habitant")
            st.text(" Nancy dans le Grand Est                              1.83Mwh/habitant")
            st.text(" Lille dans les Hauts-de-France                       1.87Mwh/habitant")
            st.text("......................................................................")
            st.text("Pourquoi plus de consommation dans les régions du sud que dans les régions du nord?") 
            st.text("Il existe plusieurs hypothèses pour tenter d'expliquer ce phénomène:")
            st.text(">Le rôle de la démographie dans la consommation d electricité") 
            st.text(">Dans les régions du nord,la majorité du matériel de chauffage n'est pas electrique")
            st.text(">La thermosensibilité des Français.-1°C en hiver =hausse de 3.2% de MW d'électricité")
            st.text(">La qualité de l'isolation des maisons serait renforcée dans les régions du Nord")
            st.text("................................................................................")
            st.text("Source:https://www.forbes.fr/environnement/" )
            
        if st.button("Enjeux de la transition énergétique"):
            
           # Affichage de l'image dans Streamlit
           # image = get_image_from_backend()
           # st.image(image, caption="Enjeux de la transition énergétique = Protection de l'environnement")
            st.text("Réduction les émissions de CO2 en vue de réduire le phénomène  des gaz à effet  serre ") 
            
        if st.button("Repartition de la consommation énergétique par secteur economique"):
            st.markdown('''
                       Tertiare et résidentiel       42% 
                       / Transports                  30%
                       / Industrie                   25%
                       / Agriculture                  3%
                       ''')     
        if st.button("Smart Building"):
                st.write("Le projet Smart building permet d'apporter de l'intelligence dans un batiment ")
                st.write("Il promeut l'Installation des capeturs et une gestion technique centralisée du batiment afin de piloter les actionneurs et controler la régulation de température en tout point du batiment")
                st.write("Un projet qui favorise le réduction des consommations d'énergie dans le secteur de l'immobilier tertiaire")
            
        if st.button("Réglementaion=Décret Tertiaire"):
                st.write('''Le décret tertiaire est un dispositif qui a pour objectif de diminuer la consommation énergétique du secteur tertiaire français de 60% à l’horizon 2050,par rapport 2010''')
                st.write('''Entré en vigueur le 1er octobre 2019, il précise les modalités d’application de l’article 175 de la loi ÉLAN (Évolution du Logement, de l’Aménagement et du Numérique).''')
                st.write('''Le Decrét tertiaire se décline en deux volets qui sont :''')
                st.write(''' 1.Transmission des données de consommation''')
                st.write(''' 2.Réduction des consommations énergétiques''')
            
        if  st.button("Accélérateur de la transition écologique=Décret Bacs"):
                st.write('''Decret tertiaire entré en vigueur le 1er Octobre 2019''')
                st.write(''' Decret Bacs entré en vigueur le 1er Octobre 2019''')         
                st.write('''Le decret Bacs pour buiding Automation & Control Systems determine les moyens permettant d'atteindre les objectifs de reduction de consomation fixées par le decret tertiaire''')
                st.write('''Cette norme impose de mettre en place un système d'automatisation et de controle des batiments,d'ici le 1er janvier 2025 à minima. ''')
                st.write('''Elle concerne tous les batiments tertiaires non résidentiels,pour lesquels le système de chauffage ou de climatisation,combiné ou non à un système de ventilation,a une puissance nominale supérieure à 290kw.''')
                st.write('''Pour les installations d'une puissance nominale supérieure à 70kw ,cette exigence devra etre respectée d'ici le 1er Janvier 2027. ''')
                
        if st.button("Label Consommation énergétique=Evaluation de la performance énergétique d'un batiment en exploitation"):
                st.write('''La certification BREEAM in-Use lancée en 2009 par le BRE(Building Reasearch Establishment), est une méthode internationale d'évaluation de la performance environnementale d'un batiment en exploitation''') 
                st.write('''Périmètre d'évaluation Breeam In-Use:''')
                st.write('''Dans sa version 6.0.0(mai 2020) propose d'évaluer un batiment selon 2 axes distincts,appelés<< Parts>>,qu'il est possible d'évaluer seuls ou conjointement''' )
                
        if st.button('Fournisseur des solutions de gestion énergétique et IOT'):
                st.write('''Bien que nombreuses à ce jour dans un immense marché immobilier,les solutions de comptage des consommations énergétiques en temps réel connues sur le marché par Didier GAMASSA sont: ''')  
                st.write('''Solutions Citron.io / Solutions IqsPot.fr /Solutions Advizeo.io''') 
                st.write('''Solutions GTB/GTC,Gestion centralisée des équipements techniques du batiment: Chauffage,Ventilation,Climatisation,Désenfumage,Ascenceurs,Portails ,....''')
                st.write('''Les principaux fabricants de GTB/GTC sont :ABB,WIT,Schneider Electric,Siemens,Distech Controls,LACROIX Sofrel,Tridium,Wattsense,Wago,Esme Solutions,Sauter,Saia Burgess Controls,Trend,''')                                                                                                                                                           
            
        if st.button('Fournisseurs traditionnels d energie en France'):
               st.write( '''Eau / Veolia ,Suez sont les fournisseurs connus sur le marché français''')
               st.write('''Electricité/Engie reste un fournisseur connue sur le marché de l'électricité''')
               st.write('''Gaz/ GRDF est un fournisseur leader sur le marché Français''')
                                
        if st.button(''' Cout Moyen de L'énergie en France hors abonnement''' ):
               st.write('''_____________________Eau______________________''')
               st.write( ''' Le prix de l'eau varie selon les territoires.Cependant le prix moyen de l'eau en France est de 4.34 €/mètre cube taxes comprises''')
               st.write(''' Le ratio est de 4 litres/m² de bureaux.''')
               st.write('''___________________Electricité_________________''')
               st.write('''Prix du Kwh de l'electricité au 1er Février 2024: ''')
               st.write('''0.2516 en option base / 0.27€ en heures pleines /0.2068€ en heures creuses''')
               st.write(''' En France, le prix moyen de l'électricité par m² est de l'ordre de 13 € par m² ''')
               st.write('''____________________Gaz_______________________''')
               st.write('''La consommation moyenne de gaz en m3 des Français est de 1012m3 par an. Chiffre qui peut varier en fonction de l'isolation et du coefficient de conversion du lieu de localisation d'un Building  ''')
               st.write('''En supposant que votre Building est bien isolé et le coefficient de conversion du lieu d'activités soit de 11.05(similaire à celui de Paris \n
                        on peut déterminer sa consommation:''' ) 
               st.write(''' Exemple :Pour un logement Index de février 2024-Index de janvier 2024)=7532-7405=127m3''')  
               st.write(''' Consommation de gaz(en m3)x Coefficient de conversion(en kwh/m3)''')
               st.write(''' Consommation de gaz en kwh =127 x 11.05 =1403Kwh ''')
               st.write(''' Consommation de gaz en euros=Consommation de gaz(en Kwh)x Prix du gaz négocié (€/Kwh)''')
               st.write('''Selon une étude le prix du Gaz naturel en Avril 2024 est de 0.0913€/kwh ''')
               st.write('''L'estimation d'une consommation moyenne en chauffage au gaz se refère à un volume de 110kwh au mètre carré et par an ''')
            
        if st.button(''' Fournisseur des sous-compteurs d'énergie(Eau/Electricité/Gaz) et flotte de capteurs IoT'''):
            st.write(''' Toutes les sociétés reconnues dans la gestion énergétique des consommations énergétiques accompagne et conseille les clients dans leur projet Smart Building avec une expertise reconnue sur le marché ''' )
        
        if st.button(''' Surface d'exploitation  soumis au Decret Tertiaire?''' ) :
            st.write('''Toute surface d'exploitation cumélée supérieure ou égale à 1000mètre carré est soumise au Décret Tertiaire''')
            
        if st.button('''Tarif minimum estimatif d'un projet de suivi des consommations électriques avec flotte des capteurs Iot au Mètre carré = 2euro/Mètre'''):
            st.write(''' Une première démarche peut etre réalisée sur un périmètre de 1000 Mètres carrés et se developper par itération = 2000€uros''')
            
           
    elif choice=="Audit Energie + Deploiement Iot":
        st.title('Audit Energétique + Deploiement Iot')
       
    elif  choice=='Solutions Iot + Plan Comptage':
        st.title('Solutions Iot + Plan de Comptage') 
             
    elif choice=="Suivi des KPI Conso(Elec/Gaz/Eau)":
        st.title('Suivi des KPI Conso Energétiques')
        
    elif choice=="Objectifs Réduction Conso Energies":
        st.title('Suivi des objectifs Réduction Conso Energies en cours')
                
    # Récupérer les données de consommation depuis le backend
    elif choice == "Visu Conso Energies(Elec/Gaz/Eau)":
        st.title('Consumption Analysis')
        data= {'Electricity': electricity_daily,'Gas':gas_daily,'Water': water_daily}
          
        visualize_consumption(data)
              
    elif choice == "Bilan Conso Energies(Elec/Gaz/Eau)":
        st.title('Bilan des Consommations Energétiques')
        st.subheader('Scenario probable de Management Energétique sur un site de 70000 mètres carrés de surfaces cumulées')
        
                        
        # Dictionnaire pour les unités de mesure de chaque ressource
        unit_of_measure = {'electricity': 'kWh', 'gas': 'm³', 'water': 'm³'}

        # Calculer la consommation totale de chaque ressource
        

        # Afficher la consommation totale de chaque ressource par an
                
        #Afficher la consommation de l'electricité ,Gaz en KWH et Eau en mètre cube
            
        st.subheader('Conversion des m3 consommés de Gaz en Kwh')
        st.write("***Le PCI moyen en France = Pouvoir Calorifique Inférieur moyen en France est 11.2kwh/m3***")
        
        #Présentation des tarifs moyens  des consommations énéergétiques en France en 2022 et 2023 en €/kwh
        
          
         
        st.subheader("Tarif  moyen national  de l'electricité , Gaz et l'eau en €/kwh en 2023 ")
        unit_costs_2023 = {'electricity_2023': 0.27,'gas_2023': 0.11617,'water_2023': 4.3}
        
        for resource, cost in unit_costs_2023.items():
            st.markdown(f"Le coût unitaire de {resource.replace('_2023', '')} est de : {cost}")
                
                        
        st.subheader("Relevés des consommations annuelles Electricité, Gaz et Eau")
        total_electricity = electricity['Consumption'].sum()
        total_gas = gas['Consumption'].sum()
        total_water = water['Consumption'].sum()
        st.markdown(f"Consommation annuelle d'électricité: {total_electricity}kwh")
        st.markdown (f"Consommation annuelle de gaz: {total_gas}m3")
        st.markdown(f"Consommation annuelle d'eau: {total_water}m3")
        
        # Calcul de la consommation annuelle totale equivalent en Kwh du gaz
        total_electricity = electricity['Consumption'].sum()
        total_gas_kwh = 11.2*gas['Consumption'].sum()
        st.subheader("Relevés des consommations annuelles Electricité , Gaz en (kwh) et l'eau en (m3):")
        st.markdown(f"Consommation annuelle totale d'électricité: {total_electricity}kwh")
        st.markdown (f"Consommation annuelle totale de gaz en Kwh: {total_gas_kwh:.2f}kwh")
        st.markdown(f"Consommation annuelle totale d'eau: {total_water}m3")
        
        st.subheader("Calcul des couts annuelles Electricité , Gaz et Eau en Euros ")
        
        total_cost_2023={'total_electricity':total_electricity*.27,'total_gas':total_gas_kwh*0.11617,'total_water':total_water*4.3}
        
        st.markdown(f"Consommation annuelle totale d'électricité: {total_electricity*.27}€")
        st.markdown (f"Consommation annuelle totale de gaz en Kwh: {total_gas_kwh*0.0913:.2f}€")
        st.markdown(f"Consommation annuelle totale d'eau: {total_water*4.34:.2f}€")
                
        st.markdown(f"<u><h4><b> Le cout annuel des consommations énergétiques du site en 2023 est de: {(total_cost_2023['total_electricity'] + total_cost_2023['total_gas'] + total_cost_2023['total_water']):.2f}€</b></h4></u></span>", unsafe_allow_html=True)
                            
        cout_2023=(total_cost_2023['total_electricity'] + total_cost_2023['total_gas'] + total_cost_2023['total_water'])
                
        
        # Afficher le diagramme circulaire
        st.subheader(" Part des dépenses annuelles par ressource énergétique:")
        plot_pie_chart(total_cost_2023)
    elif choice == "Diagnostic Performance Energétique":
        st.title("Diagnostic Performance Energétique")
        st.markdown('''#### Le DPE : qu’est-ce que c’est ?''') 
        st.markdown('''Le diagnostic de performance énergétique (DPE) a été créé en 2006. Cet outil de mesure sert à renseigner sur la performance énergétique d’un logement ou d’un bâtiment, en évaluant sa consommation d’énergie et son impact en termes d’émission de gaz à effet de serre.
                       Ce document sensibilise propriétaires et locataires quant à la consommation d'énergie et aux émissions de gaz à effet de serre occasionnées par leur logement, notamment dans une perspective de travaux de rénovation.                                                                                                              ''')
        st.markdown('''##### A Savoir ''')
        st.markdown('''Depuis le 1er janvier 2023, un logement situé en France métropolitaine est qualifié d'énergétiquement décent lorsque sa consommation d'énergie (chauffage, éclairage, eau chaude, ventilation, refroidissement...) est inférieure à 450 kWh/m2 d’énergie finale par mètre carré de surface habitable et par an.

                        Les logements dont la consommation d'énergie dépasse cette valeur ne peuvent plus être proposés à la location. Cette interdiction des biens les plus énergivores sur le marché locatif concernera à terme :

                        les logements classés G à compter de 2025,
                        les logements classés F à compter de 2028,
                        les logements classés E à compter de 2034.''')
        st.markdown(''' Evaluons le DPE de notre Scenario probable sur un site de 70000 mètres carrés de surfaces de bureaux cumulées ''') 
        Surface = 70000
        Conso_total=7694414 
        Critère_DPE=109.92
        
        st.markdown(f"Surface du site===> {Surface}m2")
        st.markdown (f"Consommation totale annuelle de gaz +Electricité en Kwh===> {Conso_total}kwh")
        st.markdown(f" <u><h4><b>Le Critère DPE = Conso_Total_An/Surface_Site=====>{Critère_DPE}kwh/m2 </b></h4></u>", unsafe_allow_html=True)
        st.markdown(''' ##### Le Critère DPE calculé étant inférieur à 450kwh/m2 ,le site est énergétiquement décent ''')
        
    elif choice == "Bilan GES(Gaz à effet de serre)":
        st.title("Empreinte carbone du site sur le climat liée aux consommations d'énergie")
        st.markdown('''#### Facteur d'émission CO2 pour l'electricité''')
        st.markdown(''' On estime  pour l'electricité le facteur d'émission de 85eqCO2/Kwh  ''' )
        st.markdown(''' On estime  pour le gaz naturel le facteur d'émission de 0.198eqCO2/Kwh  ''' )
        total_electricity = electricity['Consumption'].sum()
        total_gas_kwh = 11.2*gas['Consumption'].sum()
        st.markdown(f"L'équivalent CO2 lié au consommation annuelle  d'électricité: {total_electricity*85:.2f}kgCO2eq")
        st.markdown (f"L'équivalent CO2 lié au consommation annuelle totale de gaz en Kwh: {total_gas_kwh*0.198:.2f}kgCO2eq")
        total_co2_eq_2023={'total_electricity_Co2eq':total_electricity*85,'total_gas_CO2eq':total_gas_kwh*0.11617}
        st.subheader(" Part des émissions annuelles equivalent de CO2 par ressource énergétique:")
        plot_pie_chart(total_co2_eq_2023)
        st.markdown (f" ##### L'équivalent annuel des émissions de CO2 lié au consommation totale de Gaz et Electricité: {(total_electricity*85+total_gas_kwh*0.198):.2f}kgCO2eq")
        st.markdown(" ##### Selon notre scenario probable ,nous avons donc évaluer l'empreinte carbone sur le climat liée aux consommations d'énergie d'un site de 70000 mètres carrés de surfaces de bureaux cumulés")
        st.markdown (f"<u><h2><b>{(total_electricity*85+total_gas_kwh*0.198):.3f}kgCO2eq=={0.001*(total_electricity*85+total_gas_kwh*0.198):.3f}TCO2eq =={0.000001*(total_electricity*85+total_gas_kwh*0.198):.3f}MTCO2eq </b></h2></u>", unsafe_allow_html=True)                                                           
        st.markdown(''' #### A titre comparatif :### ''')
        st.markdown(''' Danone France =====> 25.689MtCO2eq en 2023 ''')
        st.markdown(''' SFR France =====> 0.39 MtCO2eq en 2023 ''')
        st.markdown(''' Officiellement Orange déclare globalement  8,472MtCO2eq en 2023 méthode incluant l'electricité produite par le groupe''')
        url10="https://wearegreen.io/bilan-carbone/orange"
        st.markdown(f'<a href="{url10}" target="_blank">{"Cliquez ici pour visiter"+"www.bilan-carbone/orange"}</a>', unsafe_allow_html=True)
    elif choice == " Axes d'amélioration identifiés":    
        #Ce site est il equipé d'une GTB,
        st.title("Axes d'amélioration identifiés")
        st.markdown('''### Le site est il équipé d'une GTB?''')
        st.markdown('''###### Le site est équipé dune GTB de Classe C avec des performances énergétiques standards''')
        st.markdown('''######  La GTC est utilisé  en mode supervision de niveau 1 et la maitenance est tributaire d'un prestataire''')
        
        st.markdown('''#### Quelle solution d'optimisation de la performance energétique peut etre proposée au site? ### ''')
        st.markdown('''###### Selon une étude menée par le CNRS, consulter sa consommation d'énergie en direct permettrait de réaliser des économies - en moyenne 23% ####''')
        
        st.markdown(''' #### Optimisation de la performance énergétique par intégration d'un système de suivi en temps réel des postes de  consommations energivores en  Electricité,Gaz et Eau. ### ''')
        st.markdown(''' ###### Nombreuses offres  dans l'immense marché de la transition écologique et énergétique : la difference se situera sur la qualité du service et du tarif des prestations #### ''')
        
        st.markdown('''  #### Chiffrage d'un Projet de Deploiement d'une flotte de capteur Iot de suivi en temps réel de la conso énergétique  sur une surface de 70000 mètres carrés #### ''')
        st.markdown(''' ###### Audit + Etude + Deploiement Iot+ 2ans de maintenance offerte = 2€ht/m2 soit 140.000ht €uros de facture à honorer par le propriétaire foncier  afin d' équiper tout le site!Et il faut connaitre le site .C'est pourquoi,la première offre du Cabinet sera adressée au propriétaire foncier et laquelle sera une opportunité de valorisation  de ses biens immobiliers. ''')
        st.markdown(''' #### Estimation des économies à venir à réaliser sur le site  après validation du déploiement des capteurs IOT par le propriétaire foncier ''')
        facture_string = " ####  Facture Consommation Energies_2023 * (0,23) "
        resultat_calcul1 = round(1207156.32 * 0.23,2)
        

        st.markdown(f"{facture_string} ={resultat_calcul1}€")
        st.markdown(''' ##### Grace à cette valorisation des biens,les économies à venir à réaliser sur les dépenses énergétiques du site  seront garanties à un  seuil minimum de 200000Euros ''')
        st.markdown( '''#### Calcul du TRI(Temps de Retour sur Investissement) ''' )
        TRI = "##### 12 mois x Investissement/ Economie réalisée "
        resultat_calcul2=round( 12*140000/257000,2)
        st.markdown(f"{TRI} = {resultat_calcul2} mois")
        st.markdown(''' #### Types de marchés à venir ciblés par le cabinet ''') 
        lien="https://www.google.com/search?sca_esv=a6e40fb14bf67fea&sca_upv=1&sxsrf=ACQVn0-4zt4G--Rj0eI8w8iIYwLMadPF0Q:1712913069008&q=Tour+Blanche+(La+D%C3%A9fense)&stick=H4sIAAAAAAAAAEVUzWvTcBjur7DaZhu0mUOtE2M9WIvQJGvSxMumTjy4OZhFPBma7zZfTZM1HyKKF_HgEA_-AR5ERdGLIh6k6GUWVHTgTQ8eRC8O8aAwUdut-SWH8L553-d5n_eDpEcKY2WlTIRkp-rirQ65e15yML7uNgzJdB1MlDC93n_LkulIPZAuG2Vcw7WwB5CB6clqhdZ6IDNwBMpjnMiusjrZA6MDbpLwbT1khpCmO11pezBNZYLIZkjcjWxWJnwI50mSbfbAplCbNmzaJdpRIs0pkIxqcwQkEG0ZEle4akSG655b5aFn4C0V6iRlDW8KMYPaZx4fRAheoKoBKwvDHiibMfwwJhEI0YYwRuPgdBSuQg8DFFvpMBGf4LS4ZtWAlacJpQIzBYalcdi8R6gdA46rwzGx7RJQuTLtEVQc0WCHpNmiKTkWZ3eiHnjaseNxMXwrFuq1YHmBDZtwqYzQVOFIPNGkKIGPfJniHd8VwmGuwqgcFcWUoOrpqqrF1Vwj3mfbI0w_PgIW7lNWDQ0OOWBkRxyComuFWmgyVGyd_Qy6ydHst9-fJvJPkjfuv_oAHiaR7LxlOZIeLEl63ZXEmoWeQlLHTbfhBuhYHkG2bppm2DxWQMYXN_bvmfwzcQaU0MzHdw_ujUhfTuSu-oe-6qtXfpDbka2Cptn2TbvVya69XZtCVwEyelpya9aCJTbkAH0K0McAySxIBi-1nUUZPYAgxyxdlwS3YZnorvwOZLIswA9lfrmhiw1TcQrnyXPP3t98kzqbS_SfpWunZ_PFUg5JzVlGvWHmTl7YuLjya32mNIGka3XfMi0jyL3-_m9v5u_6TGFfpo-Z_bmyPjNAX3o0daS7E2DbigliQBbenuuWEkub3QqKWumC5OXnd16k0mmQTZDJdOJwspgME2O3RvI1a7mNHdXrpqBKWHG-js29vLv5Azh4PQX-A93NR5AyBAAA&sa=X&lei=rfoYZr0b46aR1Q-_44CQDA#ip=1"
        texte_lien=" Cliquez ici pour découvrir tous les batiments energivores de la défense et susceptible de cumuler plus de 70000mètres carrés de surface de bureaux en altitude "  
        st.markdown(f"[{texte_lien}]({lien})")            

       
    elif choice=="Info + contacts utiles sites":
        st.title('Info + contacts utiles sites')
        st.markdown(''' ##### Qu'est ce qu'un Bilan Carbone?''')
        st.markdown('''En somme, c'est une méthodologie de quantification des émissions de gaz à effet de serre, destinée aux entreprises et créée en 2014. On parle aussi de Bilan Carbone. 
                        Plus concrètement, c’est un calcul qui prend la forme d’une addition. 
                        Mais, quel est le but ? Mesurer la globalité des émissions GES (directes ou indirectes) pour tous les flux physiques d’une organisation sans lesquels le fonctionnement de celle-ci ne serait pas possible. C'est-à-dire, qu'on fait un cumul de l’ensemble de ces données pour connaître le bilan global de l’entreprise.
                        À partir de ce résultat, on peut alors établir une feuille de route (ou plan de transition) des actions à mettre en place afin de réduire son impact et de limiter le réchauffement climatique.                                                                                                                                                   ''')
        st.markdown(''' ##### Comment mesurer le Bilan Carbone® de son entreprise ? ''')
        st.markdown(''' L’équation du Bilan Carbone:Nous l’avons évoqué, tout repose sur une méthode, un calcul. 
>                       émissions de CO2 = quantité consommée x facteur d'émission. 
                        La démarche consiste donc à collecter les données que l'on associe à un facteur d émission permettant de calculer son équivalent carbone.''')
        st.markdown(''' ##### Base d'empreinte  ''')
        st.markdown('''La Base Empreinte® est une base de données publique pilotée par l’ADEME (Agence de l'environnement et de la maîtrise de l'énergie) et gérée par un comité de gouvernance composé de divers acteurs publics et privés (Ministères, Organismes techniques, Associations, MEDEF…). 
                       Elle rassemble ce qui était précédemment appelé Base Carbone® et Base IMPACTS®.
                       Ainsi, elle répertorie de la manière la plus exhaustive possible une liste de facteurs d’émissions de CO2e. À ce jour, presque 10 000 facteurs sont déjà référencés. ''')
        st.markdown(''' ##### Facteur d émission ''')   
        st.markdown('''Mais, en fait, à quoi correspondent les facteurs d’émission ? Un facteur d'émission est un coefficient permettant de convertir les données d'activité en émissions de GES. Une activité en impact. C'est donc le taux d'émission moyen d'une source donnée, par rapport aux activités reliées. 
                        L’entreprise peut alors utiliser ces données en référence et réaliser efficacement sa comptabilité carbone. Les données listées repose sur 6 catégories :
                        Emissions directes de GES (énergie, process et émissions fugitives, UTCF)
                        Emissions indirectes associées à l’énergie (équivalent scope 2)
                        Emissions indirectes associées aux transports (marchandises, personnes)
                        Emissions indirectes associées aux produits achetés (matières et biens, services)
                        Emissions indirectes associées aux produits vendus (traitement des déchets)
                        Les autres émissions indirectes (équivalent scope 3) ''')
        st.markdown(''' ##### Le Bilan Carbone est il obligatoire pour tout le monde ''')
        st.markdown('''Les conditions d’obligations 
                        Le Bilan Carbone® n'est pas obligatoire. Seul le BEGES (bilan de gaz à effet de serre) est obligatoire dans 5 cas : 
                        Les services de l’État,
                        Les collectivités territoriales de plus de 50 000 habitants,
                        Les établissements publics et autres personnes morales de droit public de plus 250 agents,
                        Les personnes morales de droit privé employant plus de 500 personnes en métropole,
                        Les personnes morales de droit privé employant plus de 250 personnes en outre-mer.   
                        🖐 Bon à savoir : L'obligation du BEGES ne concerne à ce jour uniquement les scopes 1 et 2 (les émissions directes et les émissions indirectes liées à l’énergie) alors que le Bilan Carbone® englobe les 3 scopes d'émissions.''')
        st.markdown(''' ##### Où publier son bilan GES ?''')
        st.markdown(''' Très simple. En effet, l’ADEME a mis en place une plateforme nationale permettant de publier en quelques clics son bilan d'émission de gaz à effet et serre. Pour pouvoir procéder, voici les étapes : 
                        Créer un compte sur le site dédié. 
                        Télécharger le fameux Bilan Carbone® 
                        Ajouter également un “plan de transition pour réduire leurs émissions de gaz à effet de serre” (on parlait avant de “plan d'actions"). Ce document doit présenter de manière précise les objectifs définis par l’entreprise en matière de réduction des émissions, les moyens engagés, les actions envisagées, les actions déjà mises en place, les étapes intermédiaires.
                        Indiquer le volume global de réduction de GES pour les émissions directes et indirectes.                                                                                        ''')
        st.markdown(''' ##### Est-il possible de comparer son Bilan Carbone® à celui d’autres entreprises ? ''') 
        st.markdown(''' La Base Empreinte référence déjà 5039 bilans GES publiés sur la base de données de l’ADEME. On y retrouve notamment des bilans GES de : 
                        Grands groupes (Yoplait, We Are Social, RAJA, etc…)
                        Institutions (Département Seine-et-Marne, Préfecture de Gironde, etc…)
                        Écoles et organismes de formation  (IESEG, etc…) 
                        et bien d’autres organisations encore
                        ✋ Attention: Un Bilan Carbone® peut être comparé à celui d’une autre entreprise, mais il s’agit d’un exercice délicat. En effet, les différences de périmètres, d’hypothèses retenus, de données disponibles et même de conditions pour l’activité de l’entreprise influent sur le résultat d'un bilan et rendent la comparaison parfois hasardeuse.''')       
    
        st.markdown('''##### Quelles aides et financements pour des projets de transition ?)                                                                                                                                                  ###''')
        st.markdown(''' Pour vous aider dans la démarche et le cadrage de votre budget, nous avons synthétisé toutes les données existantes pour créer un simulateur clé en main. En effet, ce dernier vous permet de voir en quelques minutes les aides publiques vous êtes éligible pour financer vos projets de transition écologique. ''')
        st.markdown(''' 👉 Bon à savoir : L'aide du Tremplin pour la transition écologique permet la prise en charge du Bilan Carbone® complet à 80%, dans la limite de 5000€. On parle de diagnostique “complet” parce qu’il englobe les 3 Scopes et contient un plan d’action précis.                                                          ''')
        st.markdown('''#### Facteur d'émission CO2 pour l'electricité''')
        st.markdown('''Selon Olivier PAPIN, Ingénieur INSA – Energie et Environnement,le contenu carbone de l'électricité varie à chaque instant de la journée, selon la demande mais également les modes de production disponibles. Si la valeur moyenne annuelle de production d'électricité en France est faible, elle varie toutefois parfois brutalement dans la journée.
                        Il nous semble intéressant d'avoir en tête ces éléments pour comprendre que la production d'électricité n'est pas chose aisée car la demande est volatile et a fortiori le contenu carbone aussi.
                        Nous proposons donc une première approche « simpliste » où le contenu carbone n'est pas associé par usage car cette approche se heurte à une réalité très concrète que le contenu carbone varie à chaque minute et que les électrons du réseau ne sont pas dissociables.
                        Chaque consommateur se voit impacter le contenu carbone réel de la production de l'ensemble de l'électricité, sans chercher à savoir à quel consommateur on attribue les moyens de productions les plus émetteurs.
                        Chaque mode de production se voit impacter ses émissions propres, et pas celles d'un autre mode de production, qu'on lui attribue, ou pas, suivant l'état de la demande.
                        Chaque utilisateur ayant ensuite la responsabilité de réduire ses émissions pour contribuer à la réduction des émissions de gaz à effet de serre globales.
                        On estime alors pour l'electricité le facteur d'émission suivantr=85geqCO2/Kwh     ''')                       # Définition de l'URL et du texte du lien
        url1="https://www.statistiques.developpement-durable.gouv.fr/edition-numerique/chiffres-cles-du-climat/18-la-tarification-du-carbone-dans"
        url2 = "https://www.ademe.fr/"
        url3 = "https://www.ecologie.gouv.fr/"
        url4="https://www.notre-environnement.gouv.fr/themes/climat/les-emissions-de-gaz-a-effet-de-serre-et-l-empreinte-carbone-ressources/article/les-emissions-des-gaz-a-effet-de-serre-du-secteur-tertiaire#:~:text=R%C3%A9partition%20des%20GES%20du%20secteur,de%20l'eau%20chaude%20sanitaire."
        url5="https://www.apur.org/sites/default/files/documents/246.pdf"
        url6="https://www.economie.gouv.fr/cedef/bilan-carbone-entreprise"
        url7="https://mission-transition-ecologique.beta.gouv.fr/"
        url8="https://www.mcdonalds.fr/nos-emissions-de-gaz-effet-de-serre"
        url9="https://orki.green/bilan-carbone-reglementaire"
                    # Utilisation de st.markdown avec une syntaxe HTML pour créer le lien
        st.markdown(f'<a href="{url1}" target="_blank">{"Cliquez ici pour visiter"+"www.statistiques.developpement-durable"}</a>', unsafe_allow_html=True)
        st.markdown(f'<a href="{url2}" target="_blank">{"Cliquez ici pour visiter"+"www.ademe.fr/"}</a>', unsafe_allow_html=True)
        st.markdown(f'<a href="{url3}" target="_blank">{"Cliquez ici pour visiter"+"www.ecologie.gouv.fr/"}</a>', unsafe_allow_html=True)
        st.markdown(f'<a href="{url4}" target="_blank">{"Cliquez ici pour visiter"+"www.notre-environnement.gouv.fr/"}</a>', unsafe_allow_html=True)
        st.markdown(f'<a href="{url5}" target="_blank">{"Cliquez ici pour visiter"+"www.apur.org/"}</a>', unsafe_allow_html=True)
        st.markdown(f'<a href="{url6}" target="_blank">{"Cliquez ici pour visiter"+"www.bilan-carbone-entreprise.org/"}</a>', unsafe_allow_html=True)
        st.markdown(f'<a href="{url7}" target="_blank">{"Cliquez ici pour visiter"+"www.mission-transition-ecologique.org/"}</a>', unsafe_allow_html=True)
        st.markdown(f'<a href="{url8}" target="_blank">{"Cliquez ici pour visiter"+"www.mcdonalds-transition-ecologique.org/"}</a>', unsafe_allow_html=True)                       
        st.markdown(f'<a href="{url9}" target="_blank">{"Cliquez ici pour visiter"+"www.orki green bilan.org/"}</a>', unsafe_allow_html=True)                       












if __name__ == '__main__':
    main()
   
                           

