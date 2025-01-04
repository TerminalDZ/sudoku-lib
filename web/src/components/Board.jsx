import React from 'react';
import './Board.css';

const Board = ({ puzzle, onCellChange, disabled, hintCell, originalPuzzle, showingSolution }) => {
  const handleChange = (row, col, value) => {
    if (disabled) return;
    const numValue = value === '' ? 0 : parseInt(value, 10);
    if (isNaN(numValue) || numValue < 0 || numValue > 9) return;
    onCellChange(row, col, numValue);
  };

  const isSolvedCell = (row, col) => {
    if (!showingSolution || !originalPuzzle) return false;
    return originalPuzzle[row][col] === 0 && puzzle[row][col] !== 0;
  };

  return (
    <div className={`sudoku-board ${disabled ? 'disabled' : ''}`}>
      {puzzle.map((row, rowIndex) => (
        <div key={rowIndex} className="board-row">
          {row.map((cell, colIndex) => (
            <input
              key={`${rowIndex}-${colIndex}`}
              type="number"
              min="1"
              max="9"
              value={cell === 0 ? '' : cell}
              onChange={(e) => handleChange(rowIndex, colIndex, e.target.value)}
              className={`board-cell 
                ${(rowIndex + 1) % 3 === 0 ? 'border-bottom' : ''} 
                ${(colIndex + 1) % 3 === 0 ? 'border-right' : ''}
                ${hintCell && hintCell.row === rowIndex && hintCell.column === colIndex ? 'hint-cell' : ''}
                ${isSolvedCell(rowIndex, colIndex) ? 'solved-cell' : ''}
                ${originalPuzzle && originalPuzzle[rowIndex][colIndex] !== 0 ? 'original-cell' : ''}`}
              disabled={disabled}
            />
          ))}
        </div>
      ))}
    </div>
  );
};

export default Board;
