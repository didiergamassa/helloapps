import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

import datetime
st.set_option('deprecation.showPyplotGlobalUse', False)

# Replace with your Heroku app URL

# Adresse du backend Flask
BACKEND_URL="https://backendener-8840ad7ad582.herokuapp.com"

# Récupérer les données de consommation depuis le backend
def get_consumption_data(resource):
    response = requests.get(f"{BACKEND_URL}/{resource}")
    return response.json()

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
    menu = ['Introduction','Environnement_d_un_Projet Smart Building','Visu Audit Energie + Deploiement Iot','Visu Solutions Iot + Plan Comptage','Visu Conso Energies(Elec/Gaz/Eau)',"Bilan Conso Energies(Elec/Gaz/Eau)"," Axes d'amélioration identifiées",'Visu Suivi des KPI Conso(Elec/Gaz/Eau)','Visu objectifs Réduction Conso Energies','Info + contacts utiles sites']
    choice=st.sidebar.selectbox("Menu",menu)
    if choice=="Introduction":
       st.markdown(''' ## Idée d'un projet de Conseil en Data , Environnement , Energie et Maintenance en faveur de la transition écologique en France ! ''') 
       st.markdown(''' ######  1.En 2000, j’ai pris connaissance du traité du protocole de Kyoto qui interpellait le monde à agir contre les effets des gaz à effet de serre. J’étais étudiant en cours du Soir et du Samedi en BTS de Froid Energie et Environnement. ''')
       st.markdown(''' ######  2.En 2015, j’’entendais parler pour la première fois des changements climatiques et des dégâts causés par l’industrie du Pétrole dans le golfe de Guinée en Afrique par le feu Docteur Alain Pensé GAMASSA, médecin généraliste du Congo. Avant sa mort, il me donna mandat de le représenter à la Conférence du Climat COP 23 à Bonn au milieu de 15000 participants venus de tous les pays du monde afin de réfléchir sur les pistes susceptibles de trouver les meilleures solutions d’adaptation de notre planète aux phénomènes des changements Climatiques.''')                                                                                                                                           
       st.markdown(''' ######  3.En 2017, après la COP 23 de Bonn en Allemagne,je suis devenu un adepte de la protection de notre planète contre les dégats causés par les emissions des gaz à effet de serre depuis la révolution industrielle .''')                                                                                                                                                        
       st.markdown(''' ######  3.En 2019, je suis Chef de Projet Informatique formé à l'Institut Poly Informatique de Paris ''') 
       st.markdown(''' ######  4.En 2023, Je suis Data Scientist (Data Analyst) et évoluant actuellement vers les compétences de Développeur Full Stack par apprentissage continu chez OpenClassRooms  ''')
       st.markdown(''' ######  5.En 2023, au titre de mes responsabilités en Maintenance et Déploiement des Solutions IOT chez IqSpOT, Je me suis retrouvé au cœur du management de l’énergie par les technologies numériques.  ''')
       st.markdown(''' ######  6.En 2023 au titre de mes responsabilités en Maintenance et Energie chez Sodexo, je pilote une équipe de 10 techniciens chargés de la maintenance des infrastructures énergétiques de pointe composé de divers systèmes de réfrigération et de chauffage en faveur du confort des employés du campus technologique du groupe des télécommunications Orange à Chatillon. Oui pour qu’il y ait productivité sur un site tertiaire, il faut qu’il y ait confort au dixième de degré près; mais à quels prix ? C’est aux prix d’émissions des gaz à effet de serre produits par la surconsommation énergétique dont tous les sites tertiaires de France et du monde sont en partie responsables . D’où le décret BACS en France qui exige désormais des mesures de réduction de la consommation énergétique dans le secteur de l’immobilier tertiaire Français.''')                                                                                                                                                                
       st.markdown(''' ######  7. En 2024, mes expériences professionnelles et mes convictions idéologiques en matière de protection de notre environnement m’interpellent sérieusement sur un projet de creation un Cabinet de conseil et d'Audit dans les domaines de la Data,l’Environnement,la Maintenance et de l’Energie.Aujourd'hui la Data est au coeur de la décision et sans Data ,pas de conseils ni d'Audits!Alors ,mes multiples compétences m'exigent de mettre ce projet sur pied et  prendre le train de la transition écologique comme souhaité par mon mentor Scientifique en l'occurence du feu  Docteur Alain Pensé GAMASSA!!!''')
       st.markdown(''' ######  8. En 2024, Qui suis je? Je suis Landry Didier GAMASSA,je me définis comme un Chef Projet Senior Assistant au Management de la maintenance et du cycle de vie des ouvrages technologiques dans tout secteur industriel . Je milite pour une technologie respectueuse de l'environnement et au service du bien etre de l'humanité ''')

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
            st.write(''' Une première démarche peut etre réalisée sur un périmètre de 1000 Mètre carré et se developper par itération = 2000€uros''')
            
           
    elif choice=="Visu Audit Energie + Deploiement Iot":
        st.title('Visu Audit Energétique + Deploiement Iot')
       
    elif  choice=='Visu Solutions Iot + Plan Comptage':
        st.title('Visu Solutions Iot + Plan de Comptage') 
             
    elif choice=="Visu Suivi des KPI Conso(Elec/Gaz/Eau)":
        st.title('Suivi des KPI Conso Energétiques')
        
    elif choice=="Visu objectifs Réduction Conso Energies":
        st.title('Suivi des objectifs Réduction Conso Energies en cours')
    
    elif choice=="Info + contacts utiles sites":
        st.title('Visu info + contacts utiles sites')
        
    # Récupérer les données de consommation depuis le backend
    elif choice == "Visu Conso Energies(Elec/Gaz/Eau)":
        st.title('Consumption Analysis')
        
        response = requests.get("https://backendener-8840ad7ad582.herokuapp.com/daily_consumption_data")
        data = response.json()
           
        visualize_consumption(data)
              
    elif choice == "Bilan Conso Energies(Elec/Gaz/Eau)":
        st.title('Bilan des Consommations Energétiques et Equivalent Co2 émis par le site')
        st.subheader('Scenario sur un site de 70000 mètre carré de surfaces cumulées')
      
        # Récupérer les données de consommation depuis le backend
        consumption_data = {resource: get_consumption_data(resource) for resource in ['electricity', 'gas', 'water']}
                    
        # Dictionnaire pour les unités de mesure de chaque ressource
        unit_of_measure = {'electricity': 'kWh', 'gas': 'm³', 'water': 'm³'}

        # Calculer la consommation totale de chaque ressource
        total_consumption = {resource: sum(item['Consumption'] for item in data) for resource, data in consumption_data.items()}

        # Afficher la consommation totale de chaque ressource par an
        st.subheader('Consommation totale de chaque ressource par an:')
        for resource, consumption in total_consumption.items():
            st.write(f"{resource.capitalize()}: {consumption} {unit_of_measure[resource]}")
        
        #Afficher la consommation de l'electricité ,Gaz en KWH et Eau en mètre cube
            
        st.subheader('Consommation totale des ressources Electricité / Gaz en Kwh et Eau en mètre cube par an')
        st.write("***Le PCI moyen en France = Pouvoir Calorifique Inférieur moyen en France est 11.2kwh/m3***")
        for resource, consumption in total_consumption.items():
            if resource=='gas':
                consumption =consumption*11.2
                unit_of_measure[resource]='Kwh'
            else:
                pass
            st.write(f"{resource.capitalize()}: {consumption} {unit_of_measure[resource]}")
        
        #Présentation des tarifs unitaires des consommations énéergétiques en France
        st.write("Tarifs unitaires moyen de l énergie en France")
        st.write(unit_costs)
            
        # Calculer le coût total de la consommation pour chaque ressource
        total_cost = {resource: sum(item['Consumption'] * unit_costs[resource] for item in data) for resource, data in consumption_data.items()}
        
        # Afficher le coût total de la consommation pour chaque ressource en euros avec deux chiffres après la virgule
        st.subheader('Coût total de la consommation par ressource:')
        for resource, cost in total_cost.items():
          st.write(f"{resource.capitalize()}: {cost:.2f} euros")
                
        # Calculer la somme des coûts de chaque ressource en euros
        total_energy_cost = sum(total_cost.values())

        # Afficher la dépense énergétique annuelle
        st.markdown(f"### Dépense énergétique annuelle: {total_energy_cost:.2f} euros")

        # Afficher le diagramme circulaire
        st.subheader("Répartition des parts de consommation annuelle des ressources énergétiques:")
        plot_pie_chart(total_cost)
    elif choice == " Axes d'amélioration identifiées":    
        #Ce site est il equipé d'une GTB,
        st.markdown('''### Le site est il équipé d'une GTB?''')
        st.markdown('''###### Le site est équipé dune GTB de Classe C avec des performances énergétiques standards''')
        st.markdown('''######  La GTC est utilisé  en mode supervision de niveau 1 et la maitenance est tributaire d'un prestataire''')
        
        st.markdown('''#### Quelle solution d'optimisation de la performance energétique peut etre proposée au site? ### ''')
        st.markdown('''###### Selon une étude menée par le CNRS, consulter sa consommation d'énergie en direct permettrait de réaliser des économies - en moyenne 23% ####''')
        
        st.markdown(''' #### Optimisation de la performance énergétique par intégration d'un système de suivi en temps réel des consommations Electricité,Gaz et Eau. ### ''')
        st.markdown(''' ###### Nombreux fournisseurs dans l'immense marché de la transition écologique et énergétique : la difference se situera sur la qualité du service et du tarif des prestations #### ''')
        
        st.markdown('''  #### Chiffrage d'un Projet de Deploiement d'une flotte de capteur Iot de suivi en temps réel de la conso énergétique  sur une surface de 70000 mètre carré #### ''')
        st.markdown(''' ###### Audit + Etude + Deploiement Iot = 1€ht/m2 soit 70000.00ht €uros de facture à honorer afin d' équiper tout le site #### ''')

    
                           

if __name__ == '__main__':
    main()
