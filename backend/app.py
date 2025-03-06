from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

app = Flask(__name__)

# Clé API Spoonacular
SPOONACULAR_API_KEY = os.getenv("SPOONACULAR_API_KEY")

# Route de test
@app.route("/")
def home():
    return "Bienvenue sur le générateur de recettes !"

# Route pour récupérer des recettes
@app.route("/recettes", methods=["GET"])
def get_recettes():
    # Récupérer les ingrédients depuis les paramètres de la requête
    ingredients = request.args.get("ingredients")
    if not ingredients:
        return jsonify({"error": "Veuillez fournir des ingrédients"}), 400

    # Appeler l'API Spoonacular
    url = f"https://api.spoonacular.com/recipes/findByIngredients"
    params = {
        "ingredients": ingredients,
        "apiKey": SPOONACULAR_API_KEY,
        "number": 5  # Nombre de recettes à retourner
    }
    response = requests.get(url, params=params)

    # Vérifier si la requête a réussi
    if response.status_code != 200:
        return jsonify({"error": "Erreur lors de la récupération des recettes"}), 500

    # Retourner les recettes au format JSON
    return jsonify(response.json())

if __name__ == "__main__":
    app.run(debug=True)