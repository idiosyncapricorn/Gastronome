import json
import os
import random

INGREDIENTS_FILE = 'ingredients.json'

def get_ingredients():
    """
    Load ingredients from a JSON file or return a default set if the file doesn't exist.
    """
    if os.path.exists(INGREDIENTS_FILE):
        with open(INGREDIENTS_FILE, 'r') as file:
            return json.load(file)
    else:
        # Default ingredients
        return {
            "chocolate": {"sweet": 5, "salty": 1, "sour": 1, "bitter": 2, "umami": 1},
            "bacon": {"sweet": 2, "salty": 5, "sour": 1, "bitter": 1, "umami": 4},
            "lemon": {"sweet": 1, "salty": 1, "sour": 5, "bitter": 2, "umami": 1},
            "cheese": {"sweet": 2, "salty": 4, "sour": 1, "bitter": 2, "umami": 5},
            "tomato": {"sweet": 3, "salty": 2, "sour": 3, "bitter": 1, "umami": 4},
            "soy sauce": {"sweet": 1, "salty": 5, "sour": 2, "bitter": 1, "umami": 5},
            "apple": {"sweet": 4, "salty": 1, "sour": 3, "bitter": 1, "umami": 1},
            "spinach": {"sweet": 1, "salty": 1, "sour": 2, "bitter": 3, "umami": 2},
            "mushroom": {"sweet": 1, "salty": 1, "sour": 1, "bitter": 2, "umami": 5},
            "honey": {"sweet": 5, "salty": 1, "sour": 1, "bitter": 1, "umami": 1},
        }

def nutritional_to_umami(nutritional_facts):
    """
    Map nutritional facts to umami levels on a scale of 1-5.
    """
    umami_profile = {
        "sweet": min(5, max(1, nutritional_facts.get("sugar", 0) // 5)),
        "salty": min(5, max(1, nutritional_facts.get("sodium", 0) // 100)),
        "sour": min(5, max(1, nutritional_facts.get("acidity", 0) // 10)),
        "bitter": min(5, max(1, nutritional_facts.get("bitterness", 0) // 2)),
        "umami": min(5, max(1, nutritional_facts.get("glutamate", 0) // 10)),
    }
    return umami_profile

def add_ingredient(ingredients, name, nutritional_facts):
    """
    Add a new ingredient with its umami profile generated from nutritional facts.
    """
    umami_profile = nutritional_to_umami(nutritional_facts)
    ingredients[name] = umami_profile
    save_ingredients(ingredients)

def save_ingredients(ingredients):
    """
    Save the ingredients dictionary to a JSON file.
    """
    with open(INGREDIENTS_FILE, 'w') as file:
        json.dump(ingredients, file, indent=4)

def user_input_ingredient():
    """
    Allow user to input a new ingredient and its nutritional facts.
    """
    name = input("Enter the name of the ingredient: ").strip()
    
    sugar = int(input("Enter sugar content (grams): ").strip())
    sodium = int(input("Enter sodium content (mg): ").strip())
    acidity = int(input("Enter acidity (percentage): ").strip())
    bitterness = int(input("Enter bitterness (arbitrary scale): ").strip())
    glutamate = int(input("Enter glutamate content (mg): ").strip())
    
    nutritional_facts = {
        "sugar": sugar,
        "sodium": sodium,
        "acidity": acidity,
        "bitterness": bitterness,
        "glutamate": glutamate
    }
    
    return name, nutritional_facts

def display_ingredients(ingredients):
    """
    Display the ingredients and their umami profiles.
    """
    print("\nCurrent Ingredients:")
    for ingredient, profile in ingredients.items():
        print(f"{ingredient}: {profile}")

def suggest_use(profile):
    """
    Suggest a use case based on the flavor profile.
    """
    total_sweet = profile["sweet"]
    total_sour = profile["sour"]
    total_salty = profile["salty"]
    total_bitter = profile["bitter"]

    if total_sweet > max(total_sour, total_salty, total_bitter):
        return "Dessert"
    elif total_sour > max(total_sweet, total_salty, total_bitter):
        return "Lunch"
    elif total_sweet > 2 * total_sour and total_sweet > total_salty and total_sweet > total_bitter:
        return "Breakfast"
    else:
        return "Dinner"

def combine_ingredients(ingredients, num_ingredients=2):
    """
    Combine a random selection of ingredients and calculate the combined flavor profile.
    """
    if num_ingredients > len(ingredients):
        raise ValueError("Number of ingredients requested exceeds the number of available ingredients.")

    selected = random.sample(list(ingredients.keys()), num_ingredients)
    combined_profile = {"sweet": 0, "salty": 0, "sour": 0, "bitter": 0, "umami": 0}

    valid_ingredients = {key: value for key, value in ingredients.items() if key not in ["Combinations"]}

    for ingredient in selected:
        if ingredient not in valid_ingredients:
            print(f"Warning: '{ingredient}' is not a valid ingredient.")
            continue

        ingredient_profile = valid_ingredients[ingredient]
        
        for flavor in combined_profile:
            combined_profile[flavor] += ingredient_profile.get(flavor, 0)

    # Sort umami flavors by strength (value)
    sorted_profile = dict(sorted(combined_profile.items(), key=lambda item: item[1], reverse=True))
    
    # Suggestion based on the combined profile
    suggestion = suggest_use(combined_profile)
    
    return selected, sorted_profile, suggestion


def suggest_alterations(ingredients, original_selected):
    """
    Suggest two random alterations to the combination.
    """
    all_ingredients = list(ingredients.keys())
    # Ensure the alterations are not among the original selected ingredients
    possible_alternations = [i for i in all_ingredients if i not in original_selected]
    
    if len(possible_alternations) < 2:
        print("Not enough ingredients to suggest alterations.")
        return []
    
    suggestions = random.sample(possible_alternations, 2)
    return suggestions
def save_combination(ingredients, combination_name, selected_ingredients, combined_profile):
    """
    Save the combination to the 'Combinations' section of the JSON file.
    """
    if 'Combinations' not in ingredients:
        ingredients['Combinations'] = {}
    
    ingredients['Combinations'][combination_name] = {
        "ingredients": selected_ingredients,
        "profile": combined_profile
    }
    save_ingredients(ingredients)
    print(f"Combination '{combination_name}' saved successfully.")

def make_custom_suggestion(ingredients):
    """
    Allow user to make their own suggestion by inputting their chosen ingredients.
    """
    print("Enter your suggested ingredients (separated by commas):")
    user_input = input().strip()
    suggested_ingredients = [ingredient.strip() for ingredient in user_input.split(',')]
    
    invalid_ingredients = [ingredient for ingredient in suggested_ingredients if ingredient not in ingredients]
    if invalid_ingredients:
        print(f"Invalid ingredients: {', '.join(invalid_ingredients)}. Please check your input.")
        return
    
    combined_profile = {"sweet": 0, "salty": 0, "sour": 0, "bitter": 0, "umami": 0}
    
    for ingredient in suggested_ingredients:
        for flavor in combined_profile:
            combined_profile[flavor] += ingredients[ingredient][flavor]
    
    print("Custom Suggestion - Combined Flavor Profile:")
    for flavor, value in combined_profile.items():
        print(f"  {flavor.capitalize()}: {value}")
    
   

def control_center():
    """
    Control center to choose between adding a new ingredient, getting suggestions, making custom suggestions, or exiting.
    """
    ingredients = get_ingredients()

    while True:
        print("\nControl Center")
        print("1. Add New Ingredient")
        print("2. Get Ingredient Suggestions")
        print("3. Make Custom Suggestion")
        print("4. Display All Ingredients")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            name, nutritional_facts = user_input_ingredient()
            add_ingredient(ingredients, name, nutritional_facts)
            print(f"Ingredient '{name}' added successfully.")
        elif choice == "2":
            num_ingredients = int(input("Enter the number of ingredients to combine: ").strip())
            try:
                selected_ingredients, sorted_profile, suggestion = combine_ingredients(ingredients, num_ingredients)
                print("Selected Ingredients:", selected_ingredients)
                print("Combined Flavor Profile:")
                for flavor, value in sorted_profile.items():
                    print(f"  {flavor.capitalize()}: {value}")
                print(f"Suggested Use: {suggestion}")

                # Ask if the user wants to save the combination
                save_choice = input("Do you want to save this combination? (yes/no): ").strip().lower()
                if save_choice == "yes":
                    save_combination(selected_ingredients, sorted_profile)
                    print("Combination saved successfully.")
            except ValueError as e:
                print(e)
        elif choice == "3":
            make_custom_suggestion(ingredients)
        elif choice == "4":
            display_ingredients(ingredients)
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")


def control_center():
    """
    Control center to choose between adding a new ingredient, getting suggestions, making custom suggestions, or exiting.
    """
    ingredients = get_ingredients()

    while True:
        print("\nControl Center")
        print("1. Add New Ingredient")
        print("2. Get Ingredient Suggestions")
        print("3. Make Custom Suggestion")
        print("4. Display All Ingredients")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            name, nutritional_facts = user_input_ingredient()
            add_ingredient(ingredients, name, nutritional_facts)
            print(f"Ingredient '{name}' added successfully.")
        elif choice == "2":
            num_ingredients = int(input("Enter the number of ingredients to combine: ").strip())
            try:
                selected_ingredients, sorted_profile, suggestion = combine_ingredients(ingredients, num_ingredients)
                print("Selected Ingredients:", selected_ingredients)
                print("Combined Flavor Profile:")
                for flavor, value in sorted_profile.items():
                    print(f"  {flavor.capitalize()}: {value}")
                print(f"Suggested Use: {suggestion}")

                # Ask if the user wants to save the combination
                save_choice = input("Do you want to save this combination? (yes/no): ").strip().lower()
                if save_choice == "yes":
                    save_combination(selected_ingredients, sorted_profile)
                    print("Combination saved successfully.")
            except ValueError as e:
                print(e)
        elif choice == "3":
            make_custom_suggestion(ingredients)
        elif choice == "4":
            display_ingredients(ingredients)
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

def save_combination(ingredients, profile):
    """
    Save the combination to the 'Combinations' category in the JSON file.
    """
    file_path = INGREDIENTS_FILE
    
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
    else:
        data = {"Ingredients": {}, "Combinations": {}}
    
    combination_name = f"Combination_{len(data.get('Combinations', {})) + 1}"
    data.setdefault("Combinations", {})[combination_name] = {
        "ingredients": ingredients,  # List the ingredients used
        "profile": profile
    }
    
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)



if __name__ == "__main__":
    control_center()