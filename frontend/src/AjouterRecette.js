import React, { useState } from "react";
import axios from "axios";

const AjouterRecette = ({ onRecetteAjoutee }) => {
  const [titre, setTitre] = useState("");
  const [ingredients, setIngredients] = useState("");
  const [instructions, setInstructions] = useState("");
  const [imageUrl, setImageUrl] = useState("");

  const ajouterRecette = () => {
    axios.post("http://127.0.0.1:5000/recettes/favoris/ajouter", {
      titre,
      ingredients,
      instructions,
      image_url: imageUrl
    })
      .then(response => {
        alert(response.data.message);
        setTitre("");
        setIngredients("");
        setInstructions("");
        setImageUrl("");
        onRecetteAjoutee();
      })
      .catch(error => console.error(error));
  };

  return (
    <div>
      <h2>Ajouter une recette favorite</h2>
      <input
        type="text"
        placeholder="Titre"
        value={titre}
        onChange={(e) => setTitre(e.target.value)}
      />
      <input
        type="text"
        placeholder="Ingrédients"
        value={ingredients}
        onChange={(e) => setIngredients(e.target.value)}
      />
      <textarea
        placeholder="Instructions"
        value={instructions}
        onChange={(e) => setInstructions(e.target.value)}
      />
      <input
        type="text"
        placeholder="URL de l'image"
        value={imageUrl}
        onChange={(e) => setImageUrl(e.target.value)}
      />
      <button onClick={ajouterRecette}>Ajouter</button>
    </div>
  );
};

export default AjouterRecette;