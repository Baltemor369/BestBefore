# Documentation

BestBefore is a simple tool that allows for the management of product expiration dates.

## Requirements

* [Python 3.12.3](https://www.python.org/downloads/release/python-3123/)
  
## Installation

1. Download the application (in zip format)
2. Extract the contents into a folder of your choice
3. Run the “run.bat” script

## Warning

Windows might consider the application dangerous because it is not certified. In this case, in the error message, select the “More info” option, then click “Run anyway”.

## Usage
On the left, you can register a product by clicking the “Add a product” button. A form will appear asking for: name, supplier, reference, date, and quantity.

**Name**  
Product name

**Supplier**  
Product supplier. A form, located at the bottom of the input column, allows you to add a supplier with its supplier code. This code is automatically added to “Reference” when the supplier is selected.

**Reference**  
Unique product reference. Allows product identification, depends on the supplier code.

**Date Product**  
expiration date. Allows specific coloring in the product table: 
- green = expires in more than 2 months
- orange = expires in more than 1 month
- red = expires in less than 1 month. 
Products that have been expired for more than 1 month are automatically deleted.

**Quantity**  
Number of products expiring on this date.

Once all the information is entered, click “Save” to save the product in the database.  
If the form is open and you want to close it, simply click the “Add a product” button again.  
Additionally, after saving a product, its information is retained to be automatically filled in the next product addition form.

On the left, you have an object selector “Select rows”, which allows you to select the rows of the table that interest you by their ID (first column). Once the selection is made, you can either delete or modify them. The latter will open the addition form with the information of the first selected product. Modify the values you want and click “Save”. If all your entries are correct, you will automatically move on to modifying the next selected product.

To register suppliers with their code, the small “New Supplier” form asks for a name and a code. Enter them and click “Add Supplier”. It will be added to the list of suppliers and can be selected in the new product addition form.  
To delete a supplier, enter only the name and click “Delete Supplier”.

Above the table, you have a search bar that allows you to find products by their name, reference, or supplier. Simply select the parameter you want to search by and enter your value.

## Technology

* Interface: Streamlit 
* Database: sqlite3, pandas

## Contribution

Any suggestions for improvement are welcome.

@[Baltemor369](https://github.com/Baltemor369)  
@[nixiz0](https://github.com/nixiz0)