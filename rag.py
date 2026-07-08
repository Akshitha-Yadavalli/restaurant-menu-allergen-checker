import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ALLERGEN_FILE = os.path.join(BASE_DIR, "knowledge", "allergens.txt")
DISH_FILE = os.path.join(BASE_DIR, "knowledge", "dishes.txt")


def load_allergens():

    database = {}

    with open(ALLERGEN_FILE, "r", encoding="utf-8") as file:

        text = file.read()

    blocks = text.split("--------------------------------")

    for block in blocks:

        lines = [i.strip() for i in block.split("\n") if i.strip()]

        if len(lines) == 0:
            continue

        allergy = lines[0].replace(":", "").lower()

        database[allergy] = []

        for ingredient in lines[1:]:

            database[allergy].append(ingredient.lower())

    return database


def load_dishes():

    dishes = {}

    with open(DISH_FILE, "r", encoding="utf-8") as file:

        text = file.read()

    blocks = text.split("------------------------")

    for block in blocks:

        lines = [i.strip() for i in block.split("\n") if i.strip()]

        if len(lines) < 3:
            continue

        dish_name = lines[0].lower()

        ingredients = []

        for ingredient in lines[2:]:

            ingredients.append(ingredient.lower())

        dishes[dish_name] = ingredients

    return dishes


def analyze_menu(menu, allergies):

    allergen_db = load_allergens()
    dish_db = load_dishes()

    allergy_list = [a.strip().lower() for a in allergies.split(",")]

    menu_items = [m.strip() for m in menu.split("\n") if m.strip()]

    results = []

    for dish in menu_items:

        dish_lower = dish.lower()

        ingredients = dish_db.get(dish_lower, [])

        found = []

        matched_ingredients = []

        for allergy in allergy_list:

            if allergy not in allergen_db:
                continue

            allergen_ingredients = allergen_db[allergy]

            for ingredient in ingredients:

                if ingredient in allergen_ingredients:

                    if allergy.title() not in found:
                        found.append(allergy.title())

                    if ingredient not in matched_ingredients:
                        matched_ingredients.append(ingredient)

        if len(found) > 1:
            risk = "High"

        elif len(found) == 1:
            risk = "Medium"

        else:
            risk = "Low"

        if found:

            suggestion = "Choose another dish or ask the restaurant to remove these ingredients."

            results.append({

                "dish": dish,

                "status": "Risky",

                "risk": risk,

                "ingredients": ", ".join(ingredients),

                "matched": ", ".join(matched_ingredients),

                "allergens": ", ".join(found),

                "suggestion": suggestion

            })

        else:

            results.append({

                "dish": dish,

                "status": "Safe",

                "risk": "Low",

                "ingredients": ", ".join(ingredients),

                "matched": "-",

                "allergens": "-",

                "suggestion": "Safe to consume."

            })

    return results