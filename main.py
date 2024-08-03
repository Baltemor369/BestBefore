import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Nom du fichier CSV
CSV_FILE = 'products.csv'

# Fonction pour charger les produits depuis le fichier CSV
def load_products():
    try:
        return pd.read_csv(CSV_FILE)
    except FileNotFoundError:
        return pd.DataFrame(columns=['Nom', 'Référence', 'Fournisseur', 'Date', 'Quantité'])

# Fonction pour sauvegarder les produits dans le fichier CSV
def save_products():
    st.session_state.products.to_csv(CSV_FILE, index=False)

def remove_expired_products():
    today = datetime.now().date()
    st.session_state.products = st.session_state.products[pd.to_datetime(st.session_state.products['Date']).dt.date > today - timedelta(days=30)]
    save_products()

# Initialisation de la base de données (DataFrame)
if 'products' not in st.session_state:
    st.session_state.products = load_products()

remove_expired_products()

# Initialisation des variables de session
if 'nom' not in st.session_state:
    st.session_state.nom = ''
if 'reference' not in st.session_state:
    st.session_state.reference = ''
if 'fournisseur' not in st.session_state:
    st.session_state.fournisseur = ''
if 'date' not in st.session_state:
    st.session_state.date = datetime.now().date()
if 'quantite' not in st.session_state:
    st.session_state.quantite = 0
if 'selected_rows' not in st.session_state:
    st.session_state.selected_rows = []
if 'show_form' not in st.session_state:
    st.session_state.show_form = False
if 'edit_mode' not in st.session_state:
    st.session_state.edit_mode = False
if 'current_index' not in st.session_state:
    st.session_state.current_index = 0
if 'search_query' not in st.session_state:
    st.session_state.search_query = ''
if 'search_attribute' not in st.session_state:
    st.session_state.search_attribute = 'Nom'

# Fonction pour ajouter un produit
def add_product():
    new_product = pd.DataFrame({
        'Nom': [st.session_state.nom],
        'Référence': [st.session_state.reference],
        'Fournisseur': [st.session_state.fournisseur],
        'Date': [st.session_state.date],
        'Quantité': [st.session_state.quantite]
    })
    st.session_state.products = pd.concat([st.session_state.products, new_product], ignore_index=True)
    save_products()
    st.session_state.show_form = False

# Fonction pour supprimer des produits sélectionnés
def delete_products():
    selected_indices = st.session_state.selected_rows
    st.session_state.products.drop(selected_indices, inplace=True)
    st.session_state.products.reset_index(drop=True, inplace=True)
    save_products()
    st.session_state.selected_rows = []

# Fonction pour modifier un produit
def modify_product():
    index = st.session_state.selected_rows[st.session_state.current_index]
    st.session_state.products.at[index, 'Nom'] = st.session_state.nom
    st.session_state.products.at[index, 'Référence'] = st.session_state.reference
    st.session_state.products.at[index, 'Fournisseur'] = st.session_state.fournisseur
    st.session_state.products.at[index, 'Date'] = st.session_state.date
    st.session_state.products.at[index, 'Quantité'] = st.session_state.quantite
    save_products()
    st.session_state.current_index += 1
    if st.session_state.current_index < len(st.session_state.selected_rows):
        fill_form()
    else:
        st.session_state.show_form = False
        st.session_state.edit_mode = False
        st.session_state.current_index = 0
        st.session_state.selected_rows = []

# Fonction pour remplir le formulaire avec les informations du produit sélectionné
def fill_form():
    index = st.session_state.selected_rows[st.session_state.current_index]
    st.session_state.nom = st.session_state.products.at[index, 'Nom']
    st.session_state.reference = st.session_state.products.at(index, 'Référence')
    st.session_state.fournisseur = st.session_state.products.at(index, 'Fournisseur')
    st.session_state.date = pd.to_datetime(st.session_state.products.at(index, 'Date')).date()
    st.session_state.quantite = st.session_state.products.at(index, 'Quantité')
    st.session_state.show_form = True
    st.session_state.edit_mode = True

# Fonction pour colorer les lignes en fonction de la date
def color_rows(row):
    today = datetime.now().date()
    date = pd.to_datetime(row['Date']).date()
    if date <= today + timedelta(days=30):
        return ['background-color: red'] * len(row)
    elif date <= today + timedelta(days=60):
        return ['background-color: orange'] * len(row)
    else:
        return ['background-color: green'] * len(row)

# Interface utilisateur
st.title('Gestion des Périmés')

# Disposition en colonnes
col1, col2 = st.columns([2, 3])

with col2:
    # Liste déroulante pour sélectionner l'attribut de recherche
    st.session_state.search_attribute = st.selectbox('Rechercher par', ['Nom', 'Référence', 'Fournisseur'])

    # Barre de recherche
    st.session_state.search_query = st.text_input('Rechercher')

    # Filtrage des produits en fonction de la recherche
    filtered_products = st.session_state.products[st.session_state.products[st.session_state.search_attribute].str.contains(st.session_state.search_query, case=False, na=False)]
    
    # Affichage de la liste des produits filtrés avec coloration
    st.dataframe(filtered_products.style.apply(color_rows, axis=1))

with col1:

    # Bouton pour afficher le formulaire d'ajout
    if st.button('Ajouter un produit'):
        st.session_state.show_form = not st.session_state.show_form
        st.session_state.edit_mode = False

    # Formulaire pour ajouter ou modifier un produit
    if st.session_state.show_form:
        if st.session_state.edit_mode:
            st.text_input('Nom', key='nom')
            st.text_input('Référence', key='reference')
            st.text_input('Fournisseur', key='fournisseur')
            st.date_input('Date', key='date')
            st.number_input('Quantité', min_value=0, key='quantite')
            st.button('Enregistrer', on_click=modify_product)
        else:
            st.text_input('Nom', key='nom')
            st.text_input('Référence', key='reference')
            st.text_input('Fournisseur', key='fournisseur')
            st.date_input('Date', key='date')
            st.number_input('Quantité', min_value=0, key='quantite')
            st.button('Enregistrer', on_click=add_product)

    # Bouton pour supprimer des produits sélectionnés
    st.button('Supprimer la sélection', on_click=delete_products)

    # Sélection des lignes parmi les produits filtrés
    filtered_indices = filtered_products.index
    selected_filtered_rows = st.multiselect('Sélectionner les lignes', filtered_indices)
    st.session_state.selected_rows = selected_filtered_rows

    # Modification d'un produit sélectionné
    if st.session_state.selected_rows:
        st.button('Modifier la sélection', on_click=fill_form)
