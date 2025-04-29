import React from 'react';

const Flashcard = ({ frontText, backText }) => {
  return (
    <div className="flashcard">
      <h3>{frontText}</h3>
      <p>{backText}</p>
    </div>
  );
};

export default Flashcard;
