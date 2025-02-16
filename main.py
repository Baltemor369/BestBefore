import streamlit as st
import pandas as pd
import io

# Fonction pour créer un fichier CSV
def create_db_file():
    # Créer un DataFrame vide avec des colonnes prédéfinies
    df = pd.DataFrame(columns=["ID", "Ref", "Produit", "Family", "Date de Péremption", "Quantity"])
    
    # Convertir le DataFrame en fichier CSV en mémoire
    buffer = io.BytesIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)
    
    return buffer

# Fonction pour ajouter un élément au DataFrame
def add_element_to_data(data, ref, product, family, date_peremption, quantity):
    # Trouver le prochain ID disponible
    next_id = data['ID'].max() + 1 if not data.empty else 1

    # Créer un nouveau DataFrame pour l'élément à ajouter
    new_data = pd.DataFrame({
        "ID": [next_id],
        "Ref": [ref],
        "Produit": [product],
        "Family": [family],
        "Date de Péremption": [date_peremption],
        "Quantity": [quantity]
    })

    # Ajouter l'élément au DataFrame existant
    updated_data = pd.concat([data, new_data], ignore_index=True)
    return updated_data

# Fonction pour enregistrer les données dans le fichier CSV téléversé
def save_data_to_file(data, file):
    buffer = io.BytesIO()
    data.to_csv(buffer, index=False)
    buffer.seek(0)
    file.write(buffer.read())

if 'add_form' not in st.session_state:
    st.session_state.add_form = False

# Interface Streamlit
st.title("Best Before")

# Bouton pour créer le fichier CSV
buffer = create_db_file()
st.download_button(
    label="Créer un fichier de BDD",
    data=buffer,
    file_name="save.csv",
    mime="text/csv"
)

uploaded_file = st.file_uploader("Choisissez un fichier CSV", type=["csv"])

if uploaded_file is not None:
    # Lire le fichier téléversé en tant que DataFrame
    data = pd.read_csv(uploaded_file)

    if st.button("Ajouter un produit"):
        st.session_state.add_form = not st.session_state.add_form
    
    if st.session_state.add_form:
        # Formulaire pour ajouter un produit
        with st.form(key='add_product_form'):
            ref = st.text_input("Référence")
            product = st.text_input("Désignation")
            family = st.text_input("Famille", value=None)
            date_peremption = st.date_input("Date de Péremption", value=None)
            quantity = st.number_input("Quantité", min_value=0, value=0)
            
            submit_button = st.form_submit_button(label="Ajouter le produit")
            
            if submit_button:
                data = add_element_to_data(data, ref, product, family, date_peremption, quantity)
                st.success("Produit ajouté avec succès !")
                save_data_to_file(data, uploaded_file)

    # Afficher le tableau dans Streamlit
    st.dataframe(data, use_container_width=True)
