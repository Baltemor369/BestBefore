# BestBefore

a web app to manage expiration dates of products for a shop.

## Requirements

* [Python 3.12.3](https://www.python.org/downloads/release/python-3123/)

## Installation

1. download the project
2. extract it
3. run the script "run.bat"
    it will automatically install all requirements and launch the app.

## Features

Very simple to use : 
- to add a product with the button "ajouter un produit", a little form will appear.
- to delete a product, select rows (by the id) in the multi choice box, then click on "supprimer la sélection"
- to modify the product, select rows (by the id) in the multi choice box, then click on "modifier la sélection". you can modify selection one product by one.
- Filter the dataFrame by the name, the reference, or the provider
- rows have different colors depending on the expiration date ( red : less than 1 month left, orange : less than 2 month, green : more than 2 month).
- moreover, products whose the date is one month past are automatically removed.
- finally, the web app is accessible on local network from any device connected. Check the url you get when you launch the app.

## Tech

Interface : Streamlit

## Contribution

All suggestions for improving the project are welcome.

@[Baltemor369](https://github.com/Baltemor369)
@[nixiz0](https://github.com/nixiz0)