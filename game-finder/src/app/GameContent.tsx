import React from "react";
import { Image } from 'antd';

const GameContent: React.FC<{ game: any }> = ({ game }) => {
  if (!game) {
    return <div>Wybierz grę z listy.</div>;
  }

  return (
    <div>
      <h1>{game.title}</h1>
      <p>Gatunek: {game.genre}</p>
      <p>Opis: {game.description ? game.description : "Brak opisu"}</p>
      {game.img ? (
        <Image
          width={200}
          src={game.img}
          alt="Obraz gry"
        />
      ) : (
        <p>Brak obrazka</p>
      )}
    </div>
  );
};

export default GameContent;
