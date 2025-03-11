import React, { useState, useEffect } from "react";
import axios from "axios";
import AjouterRecette from "./AjouterRecette";
import RecettesFavorites from "./RecettesFavorites";

function App() {
  const [recettes, setRecettes] = useState([]);

  // Charger les recettes favorites au montage du composant
  useEffect(() => {
    chargerRecettes();
  }, []);

  const chargerRecettes = () => {
    axios.get("http://127.0.0.1:5000/recettes/favoris")
      .then(response => setRecettes(response.data))
      .catch(error => console.error(error));
  };

  return (
    <div className="App">
      <h1>Générateur de recettes</h1>
      <AjouterRecette onRecetteAjoutee={chargerRecettes} />
      <RecettesFavorites recettes={recettes} onRecetteSupprimee={chargerRecettes} />
    </div>
  );
}

export default App;