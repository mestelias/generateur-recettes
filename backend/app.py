from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Charger les variables d'environnement
load_dotenv()

# Initialiser Flask
app = Flask(__name__)
CORS(app)  # Autoriser les requêtes CORS

# Configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialiser SQLAlchemy
db = SQLAlchemy(app)

# Clé API Spoonacular
SPOONACULAR_API_KEY = os.getenv("SPOONACULAR_API_KEY")

# Route de test
@app.route("/")
def home():
    return "Bienvenue sur le générateur de recettes !"

# Route pour récupérer des recettes
@app.route("/recettes", methods=["GET"])
def get_recettes():
    ingredients = request.args.get("ingredients")
    if not ingredients:
        return jsonify({"error": "Veuillez fournir des ingrédients"}), 400

    url = f"https://api.spoonacular.com/recipes/findByIngredients"
    params = {
        "ingredients": ingredients,
        "apiKey": SPOONACULAR_API_KEY,
        "number": 5
    }
    response = requests.get(url, params=params)

    if response.status_code != 200:
        return jsonify({"error": "Erreur lors de la récupération des recettes"}), 500

    return jsonify(response.json())

# Route pour rajouter une recette favorite
@app.route("/recettes/favoris/ajouter", methods=["POST"])
def ajouter_recette_favorite():
    data = request.json
    nouvelle_recette = RecetteFavorite(
        titre=data.get("titre"),
        ingredients=data.get("ingredients"),
        instructions=data.get("instructions"),
        image_url=data.get("image_url")
    )
    db.session.add(nouvelle_recette)
    db.session.commit()
    return jsonify({"message": "Recette ajoutée aux favoris !"}), 201

# Route pour supprimer une recette favorite
@app.route("/recettes/favoris/supprimer/<int:id>", methods=["DELETE"])
def supprimer_recette_favorite(id):
    recette = RecetteFavorite.query.get_or_404(id)
    db.session.delete(recette)
    db.session.commit()
    return jsonify({"message": "Recette supprimée des favoris !"}), 200

# Route pour consulter les recettes favorites
@app.route("/recettes/favoris", methods=["GET"])
def consulter_recettes_favorites():
    recettes = RecetteFavorite.query.all()
    return jsonify([{
        "id": recette.id,
        "titre": recette.titre,
        "ingredients": recette.ingredients,
        "instructions": recette.instructions,
        "image_url": recette.image_url
    } for recette in recettes]), 200

# Modèle SQLAlchemy
class RecetteFavorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(200), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(500))

    def __repr__(self):
        return f"<RecetteFavorite {self.titre}>"

if __name__ == "__main__":
    app.run(debug=True)