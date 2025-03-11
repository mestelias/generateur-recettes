import axios from "axios";

const RecettesFavorites = ({ recettes, onRecetteSupprimee }) => {
  const supprimerRecette = (id) => {
    axios.delete(`http://127.0.0.1:5000/recettes/favoris/supprimer/${id}`)
      .then(() => {
        onRecetteSupprimee();
      })
      .catch(error => console.error(error));
  };

  return (
    <div>
      <h2>Mes recettes favorites</h2>
      {recettes.length === 0 ? (
        <p>Aucune recette favorite pour le moment.</p>
      ) : (
        <ul>
          {recettes.map(recette => (
            <li key={recette.id}>
              <h3>{recette.titre}</h3>
              <img src={recette.image_url} alt={recette.titre} width="200" />
              <p>{recette.ingredients}</p>
              <p>{recette.instructions}</p>
              <button onClick={() => supprimerRecette(recette.id)}>Supprimer</button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default RecettesFavorites;