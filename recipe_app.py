from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy.types import String, Integer

# Create an engine to the database
engine = create_engine("mysql://cf-python:password@localhost/my_database")
# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Create declarative base
Base = declarative_base()

# Create a class for the recipe table
class Recipe(Base):
    __tablename__ = "final_recipes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    def __repr__(self):
        return "<Recipe ID: " + str(self.id) + "-" + self.name + " Difficulty: " + str(self.difficulty) + " >"
    
    def __str__(self):
        return(f"Recipe Name: {self.name}\n"
            f"\tCooking Time: {self.cooking_time}\n"
            f"\tDifficulty: {self.difficulty}\n"
            f"\tIngredients: {self.ingredients}")
    
    # Calculate difficulty, used in create_recipe()
    def calc_difficulty(self):
        
        num_ingredients = len(self.ingredients.split(','))
        cooking_time = self.cooking_time

        if cooking_time < 10 and num_ingredients < 4:
            self.difficulty = "Easy"
        elif cooking_time < 10 and num_ingredients >= 4:
            self.difficulty = "Medium"
        elif cooking_time >= 10 and num_ingredients < 4:
            self.difficulty = "Intermediate"
        elif cooking_time >= 10 and num_ingredients >= 4:
            self.difficulty = "Hard"

    def return_ingredients_as_list(self):
        # Check if the ingredients string is empty
        if not self.ingredients:
            return []

        # Otherwise, split the string into a list at each ", "
        ingredients_list = self.ingredients.split(", ")
        return ingredients_list

# Create table in the database
Base.metadata.create_all(engine)
        
# Functions used for user choices
# Create recipe
def create_recipe():
    # Ask user for recipe details
    # Recipe name
    while True:
        user_input1 = input("Enter the name of the recipe: ")
        if len(user_input1) <= 50:
            name = user_input1
            break
        else:
            print("Name exceeds character limit. Try again.")
    
    ######## test what happens when exceeds 50 - goes back to menu? Or asks for input again?
    # Recipe cooking time
    while True:
        user_input2 = input("Enter the cooking time in minutes: ")
        if user_input2.isnumeric():
            cooking_time = int(user_input2)
            break
        else:
            print("Please enter a number.")
            
    # Recipe ingredients
    
    # Ask user for the number of ingredients they'd like to add
    while True:
        try:
            n = int(input("How many ingredients would you like to add? "))
            # If n is a positive integer, break out of the loop
            if n > 0:
                break
            else:
                print("Please enter a positive number.")
        except ValueError:
            # If a ValueError is raised (e.g., input is not a number), print an error message
            print("Invalid input. Please enter a numeric value.")

    # Check if character limit is exceeded
    character_limit_exceeded = False
    ingredients = []
    for i in range(n):
        if character_limit_exceeded:
            break  # Exit the outer loop if the character limit has already been exceeded
        # Add a loop to allow re-entry if the ingredient causes an overflow
        while True:  
            ingredient = input(f"Enter ingredient {i+1}: ").title()
            # Check if adding the new ingredient would exceed the 255 characters limit
            if len(", ".join(ingredients + [ingredient])) > 255:
                print("Sorry, you've exceeded the total character limit and cannot add more ingredients.")
                break
            else:
                ingredients.append(ingredient)
                break  # Exit the while loop since the ingredient was successfully added

    ingredients_string = ", ".join(ingredients)

    # Create a new recipe object
    recipe_entry = Recipe(name=name, ingredients=ingredients_string, cooking_time=cooking_time)
    recipe_entry.calc_difficulty()

    # Add the new recipe to the session
    session.add(recipe_entry)
    session.commit()
    print("Recipe added successfully!")

# View recipe
def view_all_recipes():
    # Retrieve all recipes from the database
    recipes = session.query(Recipe).all()

    # Check if there are no entries
    if not recipes:
        print("There aren't any entries in your database.")
        return None  # Exit the function

    # If there are entries, display each recipe
    for recipe in recipes:
        print(recipe)  # This calls the __str__ method of each Recipe instance

# Search recipes
def search_by_ingredients():
    # Check if the table has any entries
    entry_count = session.query(Recipe).count()
    if entry_count == 0:
        print("There aren't any entries in your database.")
        return None  # Exit the function

    # Retrieve only the values from the ingredients column
    recipes = session.query(Recipe).all()

    all_ingredients = []

    # Go through each entry in results
    for recipe in recipes:
        # Split the ingredients into a temporary list
        temp_list = recipe.return_ingredients_as_list()
        
        # Add each ingredient from this list to all_ingredients if it isn't already included
        for ingredient in temp_list:
            if ingredient not in all_ingredients:
                all_ingredients.append(ingredient)

    sorted_ingredients = sorted(all_ingredients)

    # Display numerated list of unique, sorted ingredients
    print("\nIngredients:")
    
    for idx, ingredient in enumerate(sorted_ingredients, 1):
        print(f"{idx}. {ingredient}")

    # Prompt the user for the ingredient to search for
    while True:
        try:
            input_str = input("Enter the number(s) of the ingredient(s) you want to search for, separated by spaces. \n#: ")
            # Split input string on spaces and attempt to convert to zero-based indices
            idx_list = [int(x) - 1 for x in input_str.split()]

            # Check if all indices are within the valid range
            if all(0 <= idx < len(sorted_ingredients) for idx in idx_list):
                # Proceed with ingredient retrieval and recipe search...
                search_ingredients = [sorted_ingredients[idx] for idx in idx_list]
                print(f"You selected: {', '.join(search_ingredients)}")
                # Further processing, like fetching matching recipes
                break  # If valid input was provided, exit the loop
            else:
                print("Invalid selection. Please enter a valid number within the range of ingredients.")
        except ValueError:
            # Catch cases where conversion to int fails, including commas in input
            print("Invalid input. Please enter numbers separated by spaces.")
   
    # Retrieve the ingredients
    search_ingredients = [sorted_ingredients[idx] for idx in idx_list]
    
    print(f"You selected: {', '.join(search_ingredients)}")
    print("\nRecipes that contain these ingredients:")

    conditions = []
    for ingredient in search_ingredients:
        like_term = f"%{ingredient}%"
        conditions.append(Recipe.ingredients.like(like_term))
    
    # Retrieve all recipes from the database using the filter() query with the conditions
    matching_recipes = session.query(Recipe).filter(or_(*conditions)).all()

    # Check if any recipes matched the search criteria
    if not matching_recipes:
        print("No recipes found containing the selected ingredients.")
        return

    # Display these recipes using the __str__ method
    for recipe in matching_recipes:
        print(recipe)

# Edit recipe
def edit_recipe():
    # Check if any entries, exit if none
    entry_count = session.query(Recipe).count()
    if entry_count == 0:
        print("There aren't any entries in your database.")
        return None  # Exit the function
    
    # Retrieve all recipes from the database
    results = session.query(Recipe.id, Recipe.name).all()
    for recipe_id, recipe_name in results:
        print(f"Recipe ID: {recipe_id}, Name: {recipe_name}")

    # Prompt the user for the ID of the recipe to edit
    while True:
        try:
            user_input = int(input("Enter the ID of the recipe you would like to edit: "))
            recipe_to_edit = session.query(Recipe).filter(Recipe.id == user_input).first()
            if recipe_to_edit:
                chosen_ID = user_input
                print("1. Name: ", recipe_to_edit.name)
                print("2. Cooking Time: ", recipe_to_edit.cooking_time)
                print("3. Ingredients: ", recipe_to_edit.ingredients)

                update_success = False  # Flag to indicate a successful update
                
                while True:
                    item_to_edit = (input("Enter the number of the item you'd like to edit: "))
                    if item_to_edit == "1":
                        val_name = input("Enter the new name of the recipe: ")
                        # update the name
                        recipe_to_edit.name = val_name
                        update_success = True
                        session.commit()
                        # return changed name
                        print()
                        print(f"Recipe name updated to '{val_name}'")
                        break
                    elif item_to_edit == "2":
                        new_time = int(input("Enter the new cooking time of the recipe: "))
                        # update the time
                        recipe_to_edit.cooking_time = new_time
                        #recalculate difficulty
                        recipe_to_edit.calc_difficulty()
                        update_success = True
                        session.commit()
                        print(f"Recipe time updated to '{new_time}'")
                        break
                    elif item_to_edit == "3":
                        # Prompt the user for ingredients and store them in a list
                        # Ask user for the number of ingredients they'd like to add
                        while True:
                            try:
                                n = int(input("How many ingredients would you like to add? "))
                                # If n is a positive integer, break out of the loop
                                if n > 0:
                                    break
                                else:
                                    print("Please enter a positive number.")
                            except ValueError:
                                # If a ValueError is raised (e.g., input is not a number), print an error message
                                print("Invalid input. Please enter a numeric value.")

                        # Check if character limit is exceeded
                        character_limit_exceeded = False
                        ingredients = []
                        for i in range(n):
                            if character_limit_exceeded:
                                break  # Exit the outer loop if the character limit has already been exceeded
                            # Add a loop to allow re-entry if the ingredient causes an overflow
                            while True:  
                                ingredient = input(f"Enter ingredient {i+1}: ").title()
                                # Check if adding the new ingredient would exceed the 255 characters limit
                                if len(", ".join(ingredients + [ingredient])) > 255:
                                    print("Sorry, you've exceeded the total character limit and cannot add more ingredients.")
                                    break
                                else:
                                    ingredients.append(ingredient)
                                    break  # Exit the while loop since the ingredient was successfully added

                        ingredients_string = ", ".join(ingredients)

                        # update the ingredients
                        recipe_to_edit.ingredients = ingredients_string
                        # recalculate difficulty
                        recipe_to_edit.calc_difficulty()
                        update_success = True
                        session.commit()
                        print("Recipe updated successfully!")
                        print(f"New recipe details:")
                        print(recipe_to_edit)
                        break
                    else:
                        print("Invalid input. Please enter a valid number.")
                
                if update_success:
                    session.commit()
                    print("Recipe updated successfully!")
                    print(recipe_to_edit)
                    break  # Break out of the outer loop to return to the main menu
            else:
                print("Please enter a valid ID.")
                continue
        except ValueError:
            print("Please enter a valid ID.")

# Delete recipe
def delete_recipe():
    # Check if any entries, exit if none
    entry_count = session.query(Recipe).count()
    if entry_count == 0:
        print("There aren't any entries in your database.")
        return None  # Exit the function
    
    # Retrieve all recipes from the database
    results = session.query(Recipe.id, Recipe.name).all()
    for recipe_id, recipe_name in results:
        print(f"Recipe ID: {recipe_id}, Name: {recipe_name}")

    # Prompt the user for the ID of the recipe to delete
    while True:
        user_input = int(input("Enter the ID of the recipe you would like to delete: "))
        recipe_to_delete = session.query(Recipe).filter(Recipe.id == user_input).first()
        if recipe_to_delete:
            session.delete(recipe_to_delete)
            session.commit()
            print(f"Recipe ID {user_input} has been deleted.")
            break
        else:
            print("Please enter a valid ID.")

# Present main menu to user, user makes a choice and relevant function is executed
def main_menu(engine, session):
    choice = ""
    while choice.lower() != "quit":
        choice = input("""
        Main Menu:
        ====================================
        Pick a choice by entering a number:
        1. Create a new recipe
        2. View all recipes
        3. Search for a recipe by ingredient
        4. Update an existing Recipe
        5. Delete a Recipe
        Type 'quit' to exit the program.
        Your choice: """).strip()

        print()

# Execute function base on choice
        if choice == "1":
            create_recipe()
        elif choice == "2":
            view_all_recipes()
        elif choice == "3":
            search_by_ingredients()
        elif choice == "4":
            edit_recipe()
        elif choice == "5":
            delete_recipe()
        elif choice.lower() == "quit":
            print("Exiting program...")
            if session:
                session.close()
            if engine:
                engine.dispose()
        else:
            print("Invalid choice. Please enter a number from 1 to 4, or type 'quit' to exit.")

main_menu(engine, session)