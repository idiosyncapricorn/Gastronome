from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os
import random

app = Flask(__name__)

INGREDIENTS_FILE = 'ingredients.json'

def get_ingredients():
    if os.path.exists(INGREDIENTS_FILE):
        with open(INGREDIENTS_FILE, 'r') as file:
            return json.load(file)
    else:
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

def save_ingredients(ingredients):
    with open(INGREDIENTS_FILE, 'w') as file:
        json.dump(ingredients, file, indent=4)

@app.route('/')
def index():
    ingredients = get_ingredients()
    return render_template('index.html', ingredients=ingredients)

@app.route('/add_ingredient', methods=['POST'])
def add_ingredient():
    ingredients = get_ingredients()
    name = request.form['name']
    nutritional_facts = {
        "sugar": int(request.form['sugar']),
        "sodium": int(request.form['sodium']),
        "acidity": int(request.form['acidity']),
        "bitterness": int(request.form['bitterness']),
        "glutamate": int(request.form['glutamate'])
    }
    ingredients[name] = nutritional_to_umami(nutritional_facts)
    save_ingredients(ingredients)
    return redirect(url_for('index'))

def nutritional_to_umami(nutritional_facts):
    return {
        "sweet": min(5, max(1, nutritional_facts.get("sugar", 0) // 5)),
        "salty": min(5, max(1, nutritional_facts.get("sodium", 0) // 100)),
        "sour": min(5, max(1, nutritional_facts.get("acidity", 0) // 10)),
        "bitter": min(5, max(1, nutritional_facts.get("bitterness", 0) // 2)),
        "umami": min(5, max(1, nutritional_facts.get("glutamate", 0) // 10)),
    }

@app.route('/combine_ingredients', methods=['POST'])
def combine_ingredients():
    ingredients = get_ingredients()
    num_ingredients = int(request.form['num_ingredients'])
    selected, combined_profile, suggestion = combine_random_ingredients(ingredients, num_ingredients)
    return jsonify({
        'selected': selected,
        'combined_profile': combined_profile,
        'suggestion': suggestion
    })

def combine_random_ingredients(ingredients, num_ingredients):
    selected = random.sample(list(ingredients.keys()), num_ingredients)
    combined_profile = {"sweet": 0, "salty": 0, "sour": 0, "bitter": 0, "umami": 0}

    for ingredient in selected:
        for flavor in combined_profile:
            combined_profile[flavor] += ingredients[ingredient].get(flavor, 0)

    suggestion = suggest_use(combined_profile)
    return selected, combined_profile, suggestion

def suggest_use(profile):
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

if __name__ == '__main__':
    app.run(debug=True)
