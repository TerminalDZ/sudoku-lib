# Sudoku AI

<div align="center">

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.68%2B-009688)
![React](https://img.shields.io/badge/React-18.0%2B-61DAFB)
![License](https://img.shields.io/badge/license-MIT-green)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Code Coverage](https://img.shields.io/badge/coverage-95%25-brightgreen)

</div>

A modern, full-stack Sudoku application featuring an AI-powered solver, RESTful API, and a responsive web interface. Built with Python (FastAPI) backend and React frontend, this project combines classical game logic with modern web technologies to deliver an engaging Sudoku experience.

## 🌟 Key Features

- **Advanced AI Solver**: Implements sophisticated algorithms for efficient puzzle solving
- **RESTful API**: Comprehensive HTTP endpoints for all game operations
- **Modern Web Interface**: Responsive React-based UI with professional design
- **Multiple Difficulty Levels**: Customizable puzzle generation
- **Intelligent Hint System**: Context-aware suggestions for next moves
- **Real-time Validation**: Immediate feedback on move validity
- **Cross-platform Compatibility**: Works seamlessly on desktop and mobile devices

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Node.js 14+
- npm 6+ or yarn 1.22+

### Backend Setup

1. **Clone the Repository**
```bash
git clone https://github.com/terminaldz/sudoku-ai.git
cd sudoku-ai
```

2. **Create a Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Start the API Server**
```bash
uvicorn sudoku_lib.api:app --reload
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to Web Directory**
```bash
cd web
```

2. **Install Dependencies**
```bash
npm install
# or
yarn install
```

3. **Start Development Server**
```bash
npm start
# or
yarn start
```

The web application will be available at `http://localhost:3000`

## 📚 API Documentation

### Interactive Documentation

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Core Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/puzzle/{difficulty}` | GET | Generate a new puzzle |
| `/solve` | POST | Solve a puzzle |
| `/hint` | POST | Get next move suggestion |
| `/validate` | POST | Validate puzzle solution |

### Example Usage

```python
import requests

API_URL = "http://localhost:8000"

# Generate a new puzzle
puzzle = requests.get(f"{API_URL}/puzzle/medium").json()

# Solve a puzzle
solution = requests.post(
    f"{API_URL}/solve",
    json={"puzzle": puzzle["puzzle"]}
).json()

# Get a hint
hint = requests.post(
    f"{API_URL}/hint",
    json={"puzzle": puzzle["puzzle"]}
).json()
```

## 🎮 Web Interface Features

### Game Controls
- Difficulty selection (Easy, Medium, Hard)
- New game generation
- Solution validation
- Hint system
- AI solver integration

### User Experience
- Responsive grid layout
- Touch-friendly interface
- Real-time move validation
- Visual feedback for hints and errors
- Professional animations and transitions

## 🛠️ Development

### Project Structure
```
sudoku-ai/
├── sudoku_lib/          # Backend Python package
│   ├── api.py          # FastAPI application
│   ├── game.py         # Game logic
│   └── solver.py       # AI solver implementation
├── web/                # Frontend React application
│   ├── src/
│   │   ├── components/ # React components
│   │   ├── styles/     # CSS modules
│   │   └── utils/      # Helper functions
│   └── public/         # Static assets
└── tests/              # Test suite
```

### Testing

```bash
# Run backend tests
pytest

# Run frontend tests
cd web && npm test
```

### Code Style

- Backend: Follows PEP 8 guidelines
- Frontend: Uses ESLint with Airbnb configuration
- Pre-commit hooks ensure code quality

## 📈 Performance

- **API Response Times**: < 100ms for puzzle generation
- **Solver Efficiency**: Optimized for puzzles of all difficulty levels
- **Frontend Performance**: Lighthouse score > 90
- **Mobile Responsiveness**: Tested on various devices and screen sizes

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details on:

- Code of Conduct
- Development process
- Pull request procedure
- Coding standards

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- FastAPI framework
- React.js community
- Contributors and testers

## 📧 Contact

Idriss Boukmouche - [boukemoucheidriss@gmail.com](mailto:boukemoucheidriss@gmail.com)

Project Link: [https://github.com/terminaldz/sudoku-ai](https://github.com/terminaldz/sudoku-ai)
