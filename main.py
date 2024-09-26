import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, timedelta

# Nom du fichier CSV
CSV_FILE = 'products.csv'
DB_NAME = 'fournisseurs.db'

# Connection à la BDD
conn = sqlite3.connect(DB_NAME)
c = conn.cursor()
# Create table fournisseurs
c.execute('''
    CREATE TABLE IF NOT EXISTS fournisseurs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        code TEXT NOT NULL
    )
''')
conn.commit()

# Fonction pour sauvegarder un fournisseur dans la base de données
def save_in_fournisseur(nom,code):
    # Connection à la BDD
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('INSERT INTO fournisseurs (nom,code) VALUES (?,?)', (nom,code))
    conn.commit()

# Fonction pour sauvegarder un fournisseur dans la base de données
def save_out_fournisseur(nom):
    # Connection à la BDD
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM fournisseurs WHERE nom = ?", (new_fournisseur,))
    conn.commit()

# Fonction pour charger la liste des fournisseurs depuis la base de données
def load_fournisseur():
    # Connection à la BDD
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT nom,code FROM fournisseurs')
    rows = c.fetchall()
    return [row for row in rows]

def get_code(name):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # get from the database the element where nom = name
    c.execute('SELECT code FROM fournisseurs WHERE nom=?', (name,))
    rows = c.fetchall()
    return rows[0][0] if rows else None

# Fonction pour charger les produits depuis le fichier CSV
def load_products():
    try:
        return pd.read_csv(CSV_FILE)
    except FileNotFoundError:
        return pd.DataFrame(columns=['Nom', 'Référence', 'Fournisseur', 'Date', 'Quantité'])

# Fonction pour sauvegarder les produits dans le fichier CSV
def save_products():
    st.session_state.products.to_csv(CSV_FILE, index=False)

# Fonction pour supprimer les produits qui dépassé de 1 mois
def remove_expired_products():
    today = datetime.now().date()
    st.session_state.products = st.session_state.products[pd.to_datetime(st.session_state.products['Date']).dt.date > today - timedelta(days=30)]
    save_products()

# Fonction pour mettre en capitalize les fournisseur dans la BDD
def capitalize_fournisseurs():
    st.session_state.products['Fournisseur'] = st.session_state.products['Fournisseur'].apply(lambda x: x.capitalize() if isinstance(x, str) else x)
    save_products()

# Fonction pour mettre en maj toutes les ref dans la BDD
def maj_ref():
    st.session_state.products['Référence'] = st.session_state.products['Référence'].apply(lambda x: x.upper() if isinstance(x, str) else x)
    save_products()

# Fonction de rappel pour ajouter un nouveau fournisseur
def add_fournisseur():
    new_fournisseur = st.session_state.new_fournisseur.capitalize()
    code_fournisseur = st.session_state.code_fournisseur.upper()

    # check input aren't empty
    if new_fournisseur and code_fournisseur:
        # Check if the new_fournisseur doesn't already exist in the list
        names = [name for name, code in st.session_state.fournisseur_list]
        if new_fournisseur not in names:
            # Add the new_fournisseur to the list and save it in the database
            st.session_state.fournisseur_list.append((new_fournisseur,code_fournisseur))
            save_in_fournisseur(new_fournisseur, code_fournisseur)
            st.success(f'Fournisseur "{new_fournisseur}" ajouté avec succès!')
            # Clear the session state
            st.session_state.new_fournisseur = ''
            st.session_state.code_fournisseur = ''
        else :
            st.warning(f'Le fournisseur "{new_fournisseur}" existe déjà.')
    else:
        st.error('Veuillez entrer un nom et un code de fournisseur valide.')

# Fonction de suppression d'un fournisseur
def del_fournisseur():
    new_fournisseur = st.session_state.new_fournisseur.capitalize()
    if new_fournisseur:
        if new_fournisseur in st.session_state.fournisseur_list:
            # Delete the fournisseur from the database
            save_out_fournisseur(new_fournisseur)
            
            # Delete new_fournisseur from st.session_state.fournisseur_list
            st.session_state.fournisseur_list.remove(new_fournisseur)
            st.success(f'Fournisseur "{new_fournisseur}" supprimé avec succès!')
            st.session_state.new_fournisseur = ''
        else:
            st.warning(f'Le fournisseur "{new_fournisseur}" n\'existe pas.')
    else:
        st.error('Veuillez entrer un nom de fournisseur valide.')
        
# Initialisation de la base de données (DataFrame)
if 'products' not in st.session_state:
    st.session_state.products = load_products()

remove_expired_products()
capitalize_fournisseurs()
maj_ref()

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
if 'temp_nom' not in st.session_state:
    st.session_state.temp_nom = ''
if 'temp_reference' not in st.session_state:
    st.session_state.temp_reference = ''
if 'temp_fournisseur' not in st.session_state:
    st.session_state.temp_fournisseur = ''
if 'temp_date' not in st.session_state:
    st.session_state.temp_date = datetime.now().date()
if 'temp_quantite' not in st.session_state:
    st.session_state.temp_quantite = 0
if 'fournisseur_list' not in st.session_state:
    st.session_state.fournisseur_list = load_fournisseur()
if 'new_fournisseur' not in st.session_state:
    st.session_state.new_fournisseur = ''


# Fonction pour ajouter un produit
def add_product():
    # Vérifier si un produit avec cette date existe déjà
    resultat = st.session_state.products.loc[st.session_state.products['Référence'] == st.session_state.reference and st.session_state.products['Date'] == st.session_state.date]
    if not resultat.empty:
        st.warning("Ce produit existe déjà dans la liste.")
        return
    
    # Vérifier si les champs sont remplis
    if not (st.session_state.nom and st.session_state.reference and st.session_state.fournisseur and st.session_state.date and st.session_state.quantite):
        st.warning("Veuillez remplir tous les champs pour ajouter un produit.")
        return
    
    # Création d'un DataFrame avec les nouvelles informations du produit
    new_product = pd.DataFrame({
        'Nom': [st.session_state.nom],
        'Référence': [st.session_state.reference],
        'Fournisseur': [st.session_state.fournisseur],
        'Date': [st.session_state.date],
        'Quantité': [st.session_state.quantite]
    })
    
    # Ajout du produit au DataFrame de produits existants
    st.session_state.products = pd.concat([st.session_state.products, new_product], ignore_index=True)

    save_products()
    st.success("Product successfully")
    st.session_state.show_form = False
    
    # Sauvegarde temporaire des informations du produit
    st.session_state.temp_nom = st.session_state.nom
    st.session_state.temp_reference = st.session_state.reference
    st.session_state.temp_fournisseur = st.session_state.fournisseur
    st.session_state.temp_date = st.session_state.date
    st.session_state.temp_quantite = st.session_state.quantite

# Fonction pour supprimer des produits sélectionnés
def delete_products():
    selected_indices = st.session_state.selected_rows
    st.session_state.products.drop(selected_indices, inplace=True)
    st.session_state.products.reset_index(drop=True, inplace=True)
    save_products()
    st.session_state.selected_rows = []

# Fonction pour modifier un produit
def modify_product():
    # Vérifier si un produit avec cette date existe déjà
    resultat = st.session_state.products.loc[st.session_state.products['Référence'] == st.session_state.reference and st.session_state.products['Date'] == st.session_state.date]
    if not resultat.empty:
        st.warning("Ce produit existe déjà dans la liste.")
        return
    
    # Vérifier si les champs sont remplis
    if not (st.session_state.nom and st.session_state.reference and st.session_state.fournisseur and st.session_state.date and st.session_state.quantite):
        st.warning("Veuillez remplir tous les champs pour ajouter un produit.")
        return
    
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
    st.session_state.reference = st.session_state.products.at[index, 'Référence']
    st.session_state.fournisseur = st.session_state.products.at[index, 'Fournisseur']
    st.session_state.date = pd.to_datetime(st.session_state.products.at[index, 'Date']).date()
    st.session_state.quantite = st.session_state.products.at[index, 'Quantité']
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

def update_ref():
    # insérer le code du fournisseur dans la reference
    st.session_state.reference = get_code(st.session_state.fournisseur)

# Interface utilisateur
st.title('Gestion des Périmés')

# Disposition en colonnes
col1, col2 = st.columns([2, 4])

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
        # Remplir le formulaire avec les informations temporaires
        st.session_state.nom = st.session_state.temp_nom
        st.session_state.reference = st.session_state.temp_reference
        st.session_state.fournisseur = st.session_state.temp_fournisseur
        st.session_state.date = st.session_state.temp_date
        st.session_state.quantite = st.session_state.temp_quantite

    # Formulaire pour ajouter ou modifier un produit
    if st.session_state.show_form:
        if st.session_state.edit_mode:
            st.text_input('Nom', key='nom', on_change=lambda: st.session_state.update({'nom': st.session_state.nom.lower()}))
            st.session_state.fournisseur = st.selectbox('Fournisseur', [x[0] for x in st.session_state.fournisseur_list])
            st.text_input('Référence', key='reference', on_change=lambda: st.session_state.update({'reference': st.session_state.reference.upper().replace(' ','')}))
            st.date_input('Date', key='date')
            st.number_input('Quantité', min_value=0, key='quantite')
            st.button('Enregistrer', on_click=modify_product)
        else:
            st.text_input('Nom', key='nom', on_change=lambda: st.session_state.update({'nom': st.session_state.nom.lower()}))
            st.session_state.fournisseur = st.selectbox('Fournisseur', [x[0] for x in st.session_state.fournisseur_list])
            st.text_input('Référence', key='reference', on_change=lambda: st.session_state.update({'reference': st.session_state.reference.upper().replace(' ','')}))
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

    # Input pour saisir un nouveau fournisseur
    new_fournisseur = st.text_input('Nouveau Fournisseur', key='new_fournisseur')
    
    # Input pour saisir le code fournisseur associé
    code_fournisseur = st.text_input('Code Fournisseur', key='code_fournisseur')

    # Bouton pour ajouter le nouveau fournisseur à la liste
    st.button('Ajouter Fournisseur', on_click=add_fournisseur)
    
    # Bouton pour ajouter le nouveau fournisseur à la liste
    st.button('Supprimer Fournisseur', on_click=del_fournisseur)