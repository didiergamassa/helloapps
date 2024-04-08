import streamlit as st

st.title("Hello guys")

menu = ['Introduction','Environnement_d_un_Projet Smart Building','Visu Audit Energie + Deploiement Iot','Visu Solutions Iot + Plan Comptage','Visu Conso Energies(Elec/Gaz/Eau)',"Bilan Conso Energies(Elec/Gaz/Eau)"," Axes d'amélioration identifiées",'Visu Suivi des KPI Conso(Elec/Gaz/Eau)','Visu objectifs Réduction Conso Energies','Info + contacts utiles sites']
choice=st.sidebar.selectbox("Menu",menu)
   
