# Documentation 

BestBefore un outil simple qui permet une gestion des dates de péremption des produits.

## Requirements

* [Python 3.12.3](https://www.python.org/downloads/release/python-3123/)

## Installation

1. Télécharger l'application (en zip)
2. Extraire le contenu dans un dossier de votre choix
3. Lancer le script "run.bat" 

## Attention

Il possible que Windows considère l'application comme dangeureux car il n'y pas de certification. Dans ce cas, dans le message d'erreur, sélectionnez l'option "informations complémentaire", ensuite il faut cliquer sur "executer quand même"

## Utilisation

Sur la gauche vous pouvez enregistrez un produit en cliquant sur le bouton "Ajouter un produits", un formulaire apparait qui demande : nom, fournisseur, référence, un date et un quantité.

**Nom** 
Nom du produit

**Fournisseur**
Fournisseur du produit. Un formulaire, situé en dernière dans la colonne des saisies, permet d'ajouter un fournisseur avec son code fournisseur. Ce code est ajouté automatiquement à "Référence" lors que le fournisseur est sélectionné.

**Référence**
Référence unique du produit. permet l'identification du produit, dépend du code fournisseur.

**Date**
La date de péremption du produit. permet une coloration spécifique dans la tableau des produits : vert = périmé dans + de 2 mois, orange = prérimé dans + d'un mois, rouge = périmé dans - d'un mois. les périmés qui sont périmés depuis + d'un mois sont supprimés automatiquement.

**Quantité**
Nombre de produits qui périme à cette date.

Une fois toutes les informations saisies, cliquez sur "Enregistrer" pour enregistrer le produit dans la base de données.

Si le formulaire est ouvert et que vous souhaitez le fermer, il suffit de recliquer sur le bouton "Ajoter un produit".

De plus, après avoir enregistrer un produit, ses informations sont conservées pour être automatiquement remises dans le prochain formulaire d'ajout de produit.


Sur la gauche vous avec un sélecteur d'objets "Sélectionner les lignes", il permet de sélectionner les lignes du tableau qui vous intéressent grâce à leur ID (première colonne). Une fois la sélection faite, vous pouvez ou les supprimer ou les modifier, ce dernier va ouvrir le formulaire d'ajout avec les informations du premier produit sélectionné, modifier les valeurs que vous souhaitez et cliquez sur "Enregistrer", si toutes vos saisies sont bonne, vous passerez automatiquement à la modification du prochain produit de la sélection.


Pour enregistrer des fournisseurs avec leur code, le petit formulaire "Nouveau Fournisseur" demande un nom et un code. Renseignez les puis cliquez sur "Ajouter Fournisseur", il sera ajouté à la liste des fournisseurs et pourra être sélectionné dans le formulaire d'ajout un nouveau produit.

Pour supprimer un fournisseurs, saisissez uniquement le nom puis cliquez sur "Supprimer Fournisseur".


Au dessus du tableau, vous avez une bar de recherche qui permet de trouver des produits par leur nom, leur ref ou leur fournisseur. Sélectionnez simplement avec quel paramètre vous souhaitez chercher et entrez votre valeur.

## Technologie

Interface : Streamlit
DBB : sqlite3, pandas

# Contribution

Toute suggestion d'amélioration est la bienvenue.

@[Baltemor369](https://github.com/Baltemor369)

@[nixiz0](https://github.com/nixiz0)