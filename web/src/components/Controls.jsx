import React from 'react';
import './Controls.css';

const Controls = ({ 
  onNewGame, 
  onSolve, 
  onHint, 
  onValidate, 
  difficulty, 
  setDifficulty,
  disabled,
  onShowSteps,
  hasSolution
}) => {
  return (
    <div className="controls">
      <div className="difficulty-controls">
        <select 
          value={difficulty} 
          onChange={(e) => setDifficulty(e.target.value)}
          disabled={disabled}
        >
          <option value="easy">Easy</option>
          <option value="medium">Medium</option>
          <option value="hard">Hard</option>
        </select>
        <button 
          onClick={onNewGame}
          disabled={disabled}
          className="new-game-btn"
        >
          New Game
        </button>
      </div>
      
      <div className="game-controls">
        <button 
          onClick={onSolve}
          disabled={disabled}
          className="solve-btn"
        >
          Solve
        </button>
        <button 
          onClick={onHint}
          disabled={disabled}
          className="hint-btn"
        >
          Hint
        </button>
        <button 
          onClick={onValidate}
          disabled={disabled}
          className="validate-btn"
        >
          Validate
        </button>
        {hasSolution && (
          <button 
            onClick={onShowSteps}
            disabled={disabled}
            className="steps-btn"
          >
            <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor" className="steps-icon">
              <path d="M3 4h18v2H3V4zm0 7h18v2H3v-2zm0 7h18v2H3v-2z"/>
            </svg>
            Solution Steps
          </button>
        )}
      </div>
    </div>
  );
};

export default Controls;
