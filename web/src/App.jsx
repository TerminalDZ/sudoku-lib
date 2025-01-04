import React, { useState, useEffect, useCallback } from 'react';
import Board from './components/Board';
import Controls from './components/Controls';
import Modal from './components/Modal';
import './App.css';

const API_URL = 'http://localhost:8000';

// Common fetch options for all API calls
const fetchOptions = {
  mode: 'cors',
  credentials: 'include',
  headers: {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
  }
};

function App() {
  const [puzzle, setPuzzle] = useState(Array(9).fill().map(() => Array(9).fill(0)));
  const [originalPuzzle, setOriginalPuzzle] = useState(null);
  const [difficulty, setDifficulty] = useState('medium');
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [hintCell, setHintCell] = useState(null);
  const [solutionSteps, setSolutionSteps] = useState([]);
  const [showingSolution, setShowingSolution] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const fetchNewPuzzle = useCallback(async () => {
    try {
      setLoading(true);
      setMessage('');
      setHintCell(null);
      setSolutionSteps([]);
      setShowingSolution(false);
      setIsModalOpen(false);
      
      const response = await fetch(`${API_URL}/puzzle/${difficulty}`, {
        ...fetchOptions,
        method: 'GET'
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Failed to fetch puzzle');
      }
      
      const data = await response.json();
      if (!data.puzzle) {
        throw new Error('Invalid puzzle data received');
      }
      
      setPuzzle(data.puzzle);
      setOriginalPuzzle(JSON.parse(JSON.stringify(data.puzzle)));
    } catch (error) {
      console.error('Error:', error);
      setMessage(error.message || 'Error loading puzzle. Please try again.');
    } finally {
      setLoading(false);
    }
  }, [difficulty]);

  const handleCellChange = (row, col, value) => {
    // Don't allow changes to original puzzle numbers
    if (originalPuzzle && originalPuzzle[row][col] !== 0) {
      return;
    }
    
    const newPuzzle = puzzle.map((r, i) =>
      r.map((c, j) => (i === row && j === col ? value : c))
    );
    setPuzzle(newPuzzle);
    setMessage('');
    setHintCell(null);
    setSolutionSteps([]);
    setShowingSolution(false);
  };

  const handleSolve = async () => {
    try {
      setLoading(true);
      setHintCell(null);
      setSolutionSteps([]);
      setIsModalOpen(false);
      const response = await fetch(`${API_URL}/solve`, {
        ...fetchOptions,
        method: 'POST',
        body: JSON.stringify({ puzzle: puzzle })
      });
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Failed to solve puzzle');
      }
      
      const data = await response.json();
      //console data 
      
      if (data.solution) {
        setPuzzle(data.solution);
        setSolutionSteps(data.steps || []);
        setShowingSolution(true);
        setMessage('✨ Puzzle solved successfully!');
        setIsModalOpen(true);
      } else {
        setMessage('Could not find a solution. Please check the puzzle.');
      }
    } catch (error) {
      setMessage(error.message || 'Error solving puzzle. Please try again.');
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleHint = async () => {
    try {
      setLoading(true);
      setHintCell(null);
      const response = await fetch(`${API_URL}/hint`, {
        ...fetchOptions,
        method: 'POST',
        body: JSON.stringify({ puzzle: puzzle })
      });
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || 'No hint available');
      }
      
      const data = await response.json();
      if (data.row !== undefined && data.col !== undefined && data.value !== undefined) {
        setHintCell({ row: data.row, column: data.col });
        setMessage(`💡 ${data.message}`);
      } else {
        setMessage('No hint available for the current state.');
      }
    } catch (error) {
      setMessage(error.message || 'Error getting hint. Please try again.');
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleValidate = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_URL}/validate`, {
        ...fetchOptions,
        method: 'POST',
        body: JSON.stringify({ puzzle })
      });
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Failed to validate solution');
      }
      
      const { is_valid = false, errors = [] } = await response.json() || {};
      setMessage(is_valid 
        ? '✅ The solution is valid!' 
        : `❌ ${errors.join(', ') || 'Invalid solution'}`
      );
    } catch (error) {
      setMessage(error.message || 'Error validating solution. Please try again.');
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleShowSteps = () => {
    setIsModalOpen(true);
  };

  useEffect(() => {
    fetchNewPuzzle();
  }, [fetchNewPuzzle]);

  return (
    <div className="app">
      <header>
        <h1>Sudoku IBA</h1>
        <p className="subtitle">Professional Sudoku Game with AI Solver</p>
      </header>

      <main>
        <Controls
          onNewGame={fetchNewPuzzle}
          onSolve={handleSolve}
          onHint={handleHint}
          onValidate={handleValidate}
          difficulty={difficulty}
          setDifficulty={setDifficulty}
          disabled={loading}
          onShowSteps={handleShowSteps}
          hasSolution={solutionSteps.length > 0}
        />

        <Board 
          puzzle={puzzle} 
          onCellChange={handleCellChange} 
          disabled={loading}
          hintCell={hintCell}
          originalPuzzle={originalPuzzle}
          showingSolution={showingSolution}
        />

        {message && (
          <div className={`message ${
            message.includes('✅') ? 'success' : 
            message.includes('❌') ? 'error' : 
            message.includes('💡') ? 'hint' :
            message.includes('✨') ? 'solution' :
            'info'
          }`}>
            {message}
          </div>
        )}

        {loading && (
          <div className="loading">
            Processing...
          </div>
        )}

        <Modal
          isOpen={isModalOpen}
          onClose={() => setIsModalOpen(false)}
          title="Solution Steps"
        >
          <div className="solution-steps-modal">
            {solutionSteps.map((step, index) => (
              <div key={index} className="step-item">
                <span className="step-number">{index + 1}</span>
                <span className="step-text">{step}</span>
              </div>
            ))}
          </div>
        </Modal>
      </main>

      <footer>
        <p>Made with ❤️ by Idriss Boukmouche</p>
      </footer>
    </div>
  );
}

export default App;
