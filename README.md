# Recipe App Script

## Overview

A user runs this script in their terminal. From the terminal, they can conduct the following actions by entering the relevant number or word:

1. Create a new recipe
2. View all recipes
3. Search for a recipe by ingredient
4. Update an existing Recipe
5. Delete a Recipe\
   Type 'quit' to exit the program.

## Data Structures

Each recipe is represented as a dictionary. Here's an example of what each recipe's dictionary looks like:

```
  recipe = {
    "name": "Recipe Name",
    "cooking_time": 30,  # in minutes
    "ingredients": ["Ingredient1", "Ingredient2", ...]
}

```

This data structure is used throughout the application for creating, editing, searching, and deleting recipes. It enables efficient and intuitive handling of recipe data, ensuring a seamless user experience.

Why a Dictionary?

- Clarity and Readability: Each element in the recipe is associated with a clear, descriptive key. This makes it easy for users (and other developers) to understand what each part of the recipe represents without needing additional documentation or comments.
- Flexibility and Scalability: The dictionary structure allows for easy modification and expansion. New fields can be added to the recipe format (such as 'servings', 'nutrition facts', or 'category') without disrupting existing data or requiring major structural changes.
- Direct Access: The dictionary format allows for direct access to any part of the recipe using its key. This is particularly useful for features like editing a specific part of a recipe or displaying detailed information.

Recipes are then represented in the all_recipes list.

Why a List?

- Sequential Storage: Recipes are stored in the order they are added. This sequential nature makes it intuitive to traverse, add, or remove recipes.

- Flexibility in Modification: Lists in Python are dynamic, allowing recipes to be added, removed, or modified easily. This is particularly useful for a recipe management application where the number of recipes can vary over time.

- Direct Access by Index: Each recipe can be accessed directly by its index in the list. This is useful for displaying a specific recipe or editing a recipe at a particular position.

- Compatibility with Iterative Operations: Lists are ideal for operations that require iteration, such as displaying all recipes or applying a function to each recipe (e.g., searching or filtering recipes based on certain criteria).

## Setup and Installation

### Virtual Environment

- If you haven't already, set up a virtual environment named `<name-of-environment>` for this project.

### Requirements File

- A `requirements.txt` file is included, which lists all the necessary Python packages.
- To install these packages, activate your virtual environment and run:
  ```
  pip install -r requirements.txt
  ```

### Database Setup

- This project uses a MySQL database running locally. Ensure MySQL is installed on your system.
- Create a new MySQL database and user or ensure you have the credentials for an existing database and user.

For example, to create a new database and a user with full privileges on that database, you can use the following commands in your MySQL client:

```
CREATE DATABASE my_database;
CREATE USER 'cf-python'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON my_database.* TO 'cf-python'@'localhost';
FLUSH PRIVILEGES;
```

Update the database connection string in the script if necessary. The default is set to:

```
mysql://cf-python:password@localhost/my_database
```

## Running the Script

1. **Activate the Virtual Environment**:

   ```bash
   source path/to/<name-of-environment>/bin/activate  # For Unix-like systems
   path	o\<name-of-environment>\Scriptsctivate     # For Windows
   ```

2. **Run the Script**:

   ```bash
   python recipe_app.py
   ```

3. **Follow the Prompts**
