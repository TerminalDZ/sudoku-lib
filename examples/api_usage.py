"""
Example usage of the Sudoku API
"""

import requests
import json

# API base URL (assuming local development server)
BASE_URL = "http://localhost:8000"

def print_grid(grid):
    """Pretty print a Sudoku grid"""
    for row in grid:
        print(" ".join(str(x) if x != 0 else "." for x in row))

def main():
    # Get a new puzzle
    response = requests.get(f"{BASE_URL}/puzzle/medium")
    data = response.json()
    puzzle = data["puzzle"]
    
    print("New Puzzle:")
    print_grid(puzzle)
    print("\n")
    
    # Get a hint
    hint_response = requests.post(f"{BASE_URL}/hint", json={"puzzle": puzzle})
    hint = hint_response.json()
    print(f"Hint: {hint['message']}")
    print(f"Position: ({hint['row']}, {hint['col']})")
    print(f"Value: {hint['value']}")
    print("\n")
    
    # Solve the puzzle
    solve_response = requests.post(f"{BASE_URL}/solve", json={"puzzle": puzzle})
    solution = solve_response.json()
    
    print("Solution:")
    print_grid(solution["solution"])
    print("\n")
    
    # Validate the solution
    validate_response = requests.post(
        f"{BASE_URL}/validate",
        json={"puzzle": solution["solution"]}
    )
    validation = validate_response.json()
    
    print("Validation:")
    print(f"Valid: {validation['is_valid']}")
    if not validation['is_valid']:
        print("Errors:")
        for error in validation['errors']:
            print(f"- {error}")

if __name__ == "__main__":
    main()
