# Party Hire Store Program User Guide

## Introduction

Welcome to the Party Hire Store Program! This software is designed to help manage inventory and hire items for a party hire store. With this program, you can add, update, and delete items from the inventory, as well as track party hires and returns.

## System Requirements

- Operating System: Windows, macOS, or Linux
- Python 3.6 or higher installed

## Installation

1. Download the 'party_hire_store.py' file.
2. Ensure you have Python and VS Code installed on your system.
3. Open the file and run.

## Installation (without VS code)
1. Download the 'party_hire_store.py' file.
2. Ensure you have Python and VS Code installed on your system.
3. Open a terminal or command prompt.
4. Navigate to the directory where the 'party_hire_store.py' file is located.
5. Run the following command to start the program:
   
   ```
   python party_hire_store.py
   ```

## Getting Started

Upon starting the Party Hire Store Program, you will see the main window with two tabs: 'Menu' and 'Items'.

### Menu Tab

- In this tab, you can add and update party hire records.
- Fill in the 'Full Name', 'Receipt Number', 'Item', and 'Quantity' fields to add a new party hire record.
- Click the 'Add' button to add the record to the inventory.
- To update an existing record, select it from the data table on the right, make the necessary changes in the input fields, and click the 'Update' button.

### Items Tab

- In this tab, you can manage the item types available for hire.
- Enter the name of the new item type in the 'Item Name' field and click the 'Add' button to add it to the list of available items.
- To remove an item type, select it from the list on the right and click the 'Remove' button.

### Data Table

- The data table displays the current inventory of party hire items.
- Click on the column headers to sort the data in ascending or descending order.
- To select an item from the table, click on it.

### Navigation Buttons

- The '<' and '>' buttons in the bottom section allow you to navigate between selected items in the data table.

### Search

- Use the search bar in the top section to find specific items quickly.
- Enter a keyword or item name in the search bar and press the 'Search' button.
- To clear the search results and display the full inventory, click the 'Clear Search' button.

### Deleting Items

- To delete one or more selected items from the inventory, first select the item(s) in the data table.
- Press the 'Delete' button to remove the selected items permanently.

### Copying Data

- Right-click on an item in the data table to access a context menu.
- Choose the 'Copy' option to copy the selected item's data to the clipboard.
- This feature can be useful for exporting data to other applications or documents.

## Return Items

1. Select an item from the data table that you wish to return.
2. Click the 'Return' button to initiate the return process.
3. A dialog box will prompt you to enter the quantity of the item to be returned.
4. If the entered quantity is valid (positive integer), the program will update the item's quantity in the inventory.

## Tips

- Ensure that all required fields are filled before adding or updating records.
- The 'Quantity' field must be a positive integer between 1 and 500.
- The 'Receipt Number' field must be a positive integer.
- 'Full Name' should only contain alphabetical characters.
- To return an item, make sure to enter the correct quantity to avoid errors.
- Regularly save your data or create backups to avoid data loss.
