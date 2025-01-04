import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QGridLayout, 
                             QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
                             QDialog, QMessageBox, QLineEdit, QListWidget, QListWidgetItem,
                             QCheckBox)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QPalette, QColor
from sudoku import SudokuGame
from sudoku_solver import SudokuSolver
import numpy as np
from datetime import datetime

class SudokuCell(QPushButton):
    def __init__(self, row, col):
        super().__init__()
        self.row = row
        self.col = col
        self.value = 0
        self.is_original = False
        self.setFixedSize(60, 60)
        self.setFont(QFont('Arial', 20))
        self.setStyleSheet("""
            QPushButton {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)

    def set_value(self, value, is_original=False):
        self.value = value
        self.is_original = is_original
        self.setText(str(value) if value != 0 else "")
        if is_original:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #f0f0f0;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                    color: #2c3e50;
                    font-weight: bold;
                }
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    background-color: white;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                    color: #3498db;
                }
                QPushButton:hover {
                    background-color: #f0f0f0;
                }
            """)

    def set_hint(self):
        self.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                border: 1px solid #27ae60;
                border-radius: 5px;
                color: white;
                font-weight: bold;
            }
        """)

class SudokuGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.game = SudokuGame()
        self.solver = None
        self.selected_cell = None
        self.player_name = "Player1"  # Default player name
        self.cells = []
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Sudoku Game')
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
        """)

        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # Add player name input
        player_layout = QHBoxLayout()
        player_label = QLabel("Player Name:")
        self.player_name_input = QLineEdit(self.player_name)
        self.player_name_input.textChanged.connect(self.update_player_name)
        player_layout.addWidget(player_label)
        player_layout.addWidget(self.player_name_input)
        main_layout.addLayout(player_layout)

        # Add statistics button
        stats_btn = QPushButton("View Statistics")
        stats_btn.clicked.connect(self.show_statistics)
        player_layout.addWidget(stats_btn)

        # Create title
        title = QLabel('Modern Sudoku with AI')
        title.setFont(QFont('Arial', 24))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet('color: #2c3e50;')
        main_layout.addWidget(title)

        # Add controls
        controls_layout = QHBoxLayout()

        self.difficulty_selector = QComboBox()
        self.difficulty_selector.addItems(['Easy', 'Medium', 'Hard'])
        self.difficulty_selector.setStyleSheet("""
            QComboBox {
                padding: 5px;
                border: 2px solid #3498db;
                border-radius: 5px;
                background: white;
                min-width: 100px;
                font-size: 14px;
            }
        """)
        controls_layout.addWidget(self.difficulty_selector)

        new_game_btn = QPushButton('New Game')
        new_game_btn.setStyleSheet("""
            QPushButton {
                padding: 8px 15px;
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        new_game_btn.clicked.connect(self.start_new_game)
        controls_layout.addWidget(new_game_btn)

        main_layout.addLayout(controls_layout)

        # Add AI controls
        ai_controls = QHBoxLayout()

        hint_btn = QPushButton('Get Hint')
        hint_btn.setStyleSheet("""
            QPushButton {
                padding: 8px 15px;
                background-color: #2ecc71;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        hint_btn.clicked.connect(self.get_hint)
        ai_controls.addWidget(hint_btn)

        solve_btn = QPushButton('Solve with AI')
        solve_btn.setStyleSheet("""
            QPushButton {
                padding: 8px 15px;
                background-color: #9b59b6;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
        """)
        solve_btn.clicked.connect(self.solve_with_ai)
        ai_controls.addWidget(solve_btn)

        verify_btn = QPushButton('Verify Solution')
        verify_btn.setStyleSheet("""
            QPushButton {
                padding: 8px 15px;
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        verify_btn.clicked.connect(self.verify_solution)
        ai_controls.addWidget(verify_btn)

        self.show_steps = QCheckBox('Show Solution Steps')
        self.show_steps.setChecked(True)
        self.show_steps.setStyleSheet("""
            QCheckBox {
                color: #2c3e50;
                font-size: 14px;
            }
        """)
        ai_controls.addWidget(self.show_steps)

        main_layout.addLayout(ai_controls)

        # Add Save/Load buttons
        save_load_layout = QHBoxLayout()
        
        save_btn = QPushButton('Save Game')
        save_btn.setStyleSheet("""
            QPushButton {
                padding: 8px 15px;
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #219a52;
            }
        """)
        save_btn.clicked.connect(self.save_game)
        save_load_layout.addWidget(save_btn)
        
        load_btn = QPushButton('Load Game')
        load_btn.setStyleSheet("""
            QPushButton {
                padding: 8px 15px;
                background-color: #2980b9;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2472a4;
            }
        """)
        load_btn.clicked.connect(self.load_game)
        save_load_layout.addWidget(load_btn)
        
        main_layout.addLayout(save_load_layout)

        # Create grid for Sudoku board
        grid_widget = QWidget()
        grid_widget.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        grid_layout = QGridLayout(grid_widget)
        grid_layout.setSpacing(2)

        # Create cells
        for i in range(9):
            row_cells = []
            for j in range(9):
                cell = SudokuCell(i, j)
                cell.clicked.connect(lambda checked, row=i, col=j: self.cell_clicked(row, col))
                grid_layout.addWidget(cell, i, j)
                row_cells.append(cell)
            self.cells.append(row_cells)

        # Add thick borders for 3x3 boxes
        for i in range(9):
            for j in range(9):
                cell = self.cells[i][j]
                style = cell.styleSheet().replace("}", "")
                if i % 3 == 0 and i != 0:
                    style += "border-top: 2px solid #2c3e50;"
                if j % 3 == 0 and j != 0:
                    style += "border-left: 2px solid #2c3e50;"
                style += "}"
                cell.setStyleSheet(style)

        main_layout.addWidget(grid_widget)

        # Add number buttons
        numbers_layout = QHBoxLayout()
        for num in range(1, 10):
            num_btn = QPushButton(str(num))
            num_btn.setFixedSize(40, 40)
            num_btn.setStyleSheet("""
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    border: none;
                    border-radius: 20px;
                    font-size: 16px;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
            """)
            num_btn.clicked.connect(lambda checked, x=num: self.number_clicked(x))
            numbers_layout.addWidget(num_btn)

        clear_btn = QPushButton('Clear')
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        clear_btn.clicked.connect(lambda: self.number_clicked(0))
        numbers_layout.addWidget(clear_btn)

        main_layout.addLayout(numbers_layout)

        # Set window size and position
        self.setFixedSize(main_layout.sizeHint())
        self.center_window()

        # Start a new game
        self.start_new_game()

    def center_window(self):
        screen = QApplication.primaryScreen().geometry()
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) // 2,
            (screen.height() - size.height()) // 2
        )

    def update_player_name(self):
        """Update the current player name."""
        self.player_name = self.player_name_input.text()

    def show_statistics(self):
        """Show player statistics dialog."""
        if not self.solver:
            return

        stats = self.solver.get_player_statistics(self.player_name)

        stats_dialog = QDialog(self)
        stats_dialog.setWindowTitle(f'Statistics for {self.player_name}')
        stats_dialog.setMinimumWidth(400)

        layout = QVBoxLayout()

        # Add statistics information
        total_label = QLabel(f"Total Puzzles Solved: {stats['total_puzzles_solved']}")
        layout.addWidget(total_label)

        # Add difficulty breakdown
        diff_label = QLabel("Puzzles by Difficulty:")
        layout.addWidget(diff_label)

        for diff, count in stats['puzzles_by_difficulty'].items():
            layout.addWidget(QLabel(f"  {diff.title()}: {count}"))

        # Add recent games
        recent_label = QLabel("\nRecent Games:")
        layout.addWidget(recent_label)

        history = self.solver.get_puzzle_history(player_name=self.player_name)[:5]
        for game in history:
            game_label = QLabel(f"  {game['timestamp'][:19]} - {game['difficulty'].title()}")
            layout.addWidget(game_label)

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(stats_dialog.accept)
        layout.addWidget(close_btn)

        stats_dialog.setLayout(layout)
        stats_dialog.exec()
        
    def start_new_game(self):
        difficulty = self.difficulty_selector.currentText().lower()
        puzzle = self.game.new_game(difficulty)
        self.solver = SudokuSolver(self.game.current_puzzle)

        # Update UI
        for i in range(9):
            for j in range(9):
                value = puzzle[i][j]
                self.cells[i][j].set_value(value, value != 0)

    def cell_clicked(self, row, col):
        if not self.cells[row][col].is_original:
            self.selected_cell = (row, col)
            # Reset all cell styles
            for i in range(9):
                for j in range(9):
                    if not self.cells[i][j].is_original:
                        self.cells[i][j].setStyleSheet(self.cells[i][j].styleSheet().replace("border: 2px solid #3498db !important;", ""))
            # Highlight selected cell
            self.cells[row][col].setStyleSheet(self.cells[row][col].styleSheet().replace("}", """
                border: 2px solid #3498db !important;
            }"""))

    def number_clicked(self, number):
        if self.selected_cell:
            row, col = self.selected_cell
            valid, message = self.solver.check_move(row, col, number)
            if valid:
                self.game.current_puzzle[row][col] = number
                self.cells[row][col].set_value(number)

                # Check if the puzzle is complete
                is_valid, errors = self.solver.validate_solution()
                if is_valid:
                    if np.all(self.game.current_puzzle != 0):
                        # Save the completed puzzle
                        self.solver.save_puzzle_state(
                            puzzle_type="player_solution",
                            player_name=self.player_name,
                            difficulty=self.difficulty_selector.currentText().lower()
                        )
                        QMessageBox.information(self, 'Congratulations!', 
                                             'You have completed the puzzle successfully!')
                elif np.all(self.game.current_puzzle != 0):
                    error_message = "The puzzle is complete but contains errors:\n\n" + "\n".join(errors)
                    QMessageBox.warning(self, 'Invalid Solution', error_message)
            else:
                QMessageBox.warning(self, 'Invalid Move', message)

    def get_hint(self):
        hint = self.solver.get_hint()
        if hint:
            row, col, value, message = hint
            # Reset previous hints visual style
            for i in range(9):
                for j in range(9):
                    if not self.cells[i][j].is_original:
                        self.cells[i][j].setStyleSheet(self.cells[i][j].styleSheet().replace("background-color: #2ecc71;", "background-color: white;"))
            # Highlight the hint cell
            self.cells[row][col].set_hint()
            QMessageBox.information(self, 'Hint', message)
        else:
            remaining_empty = sum(1 for i in range(9) for j in range(9) 
                                if self.game.current_puzzle[i][j] == 0)
            if remaining_empty > 0:
                QMessageBox.information(self, 'Hint', 
                    'All available hints have been used! Try solving the remaining cells yourself or use "Solve with AI".')
            else:
                QMessageBox.information(self, 'Hint', 'The puzzle is already complete!')

    def solve_with_ai(self):
        if self.show_steps.isChecked():
            success, steps = self.solver.solve()
            if success:
                # Save the AI solution
                self.solver.save_puzzle_state(
                    puzzle_type="ai_solution",
                    player_name="AI",
                    difficulty=self.difficulty_selector.currentText().lower()
                )

                # Create step-by-step dialog
                step_dialog = QDialog(self)
                step_dialog.setWindowTitle('Solution Steps')
                step_dialog.setMinimumWidth(400)

                layout = QVBoxLayout()

                # Create a list widget for steps
                step_list = QListWidget()
                for step in steps:
                    step_list.addItem(step)
                layout.addWidget(step_list)

                # Add control buttons
                button_layout = QHBoxLayout()

                # Previous step button
                prev_btn = QPushButton('Previous')
                prev_btn.setEnabled(False)

                # Next step button
                next_btn = QPushButton('Next')
                if len(steps) <= 1:
                    next_btn.setEnabled(False)

                # Apply all button
                apply_btn = QPushButton('Apply All')

                current_step = [0]  # Using list to modify in closure
                solution = self.solver.grid.copy()
                original_state = self.game.current_puzzle.copy()

                def apply_step(step_idx):
                    # Reset to original state
                    self.game.current_puzzle = original_state.copy()
                    # Apply steps up to current
                    for i in range(step_idx + 1):
                        step = steps[i]
                        if "at row" in step and "column" in step:
                            # Parse step text to get row, column and value
                            try:
                                parts = step.split()
                                value = int(parts[parts.index("single") + 1] if "single" in step else parts[parts.index("Trying") + 1])
                                row = int(parts[parts.index("row") + 1].rstrip(',')) - 1
                                col = int(parts[parts.index("column") + 1]) - 1
                                self.game.current_puzzle[row][col] = value
                                self.cells[row][col].set_value(value)
                            except:
                                pass

                    # Update button states
                    prev_btn.setEnabled(step_idx > 0)
                    next_btn.setEnabled(step_idx < len(steps) - 1)

                    # Highlight current step
                    step_list.setCurrentRow(step_idx)

                def next_step():
                    if current_step[0] < len(steps) - 1:
                        current_step[0] += 1
                        apply_step(current_step[0])

                def prev_step():
                    if current_step[0] > 0:
                        current_step[0] -= 1
                        apply_step(current_step[0])

                def apply_all():
                    self.game.current_puzzle = solution.copy()
                    for i in range(9):
                        for j in range(9):
                            if original_state[i][j] == 0:
                                self.cells[i][j].set_value(solution[i][j])
                    step_dialog.accept()

                prev_btn.clicked.connect(prev_step)
                next_btn.clicked.connect(next_step)
                apply_btn.clicked.connect(apply_all)

                button_layout.addWidget(prev_btn)
                button_layout.addWidget(next_btn)
                button_layout.addWidget(apply_btn)

                layout.addLayout(button_layout)

                step_dialog.setLayout(layout)

                # Show the dialog
                step_dialog.exec()
            else:
                QMessageBox.critical(self, 'Error', 'Could not solve the puzzle!')
        else:
            # Solve without showing steps
            success, _ = self.solver.solve()
            if success:
                solution = self.solver.grid
                for i in range(9):
                    for j in range(9):
                        if self.game.current_puzzle[i][j] == 0:
                            self.game.current_puzzle[i][j] = solution[i][j]
                            self.cells[i][j].set_value(solution[i][j])
            else:
                QMessageBox.critical(self, 'Error', 'Could not solve the puzzle!')

    def verify_solution(self):
        """Add a new method to manually verify the current solution"""
        is_valid, errors = self.solver.validate_solution()
        if is_valid:
            QMessageBox.information(self, 'Verification Result', 
                                 'The current solution is valid!')
        else:
            error_message = "The current solution contains the following errors:\n\n" + "\n".join(errors)
            QMessageBox.warning(self, 'Verification Result', error_message)

    def save_game(self):
        """Save current game state."""
        if not self.solver:
            return
            
        # Create save game dialog
        save_dialog = QDialog(self)
        save_dialog.setWindowTitle('Save Game')
        save_dialog.setMinimumWidth(300)
        
        layout = QVBoxLayout()
        
        # Add save name input
        name_layout = QHBoxLayout()
        name_label = QLabel("Save Name:")
        name_input = QLineEdit()
        name_layout.addWidget(name_label)
        name_layout.addWidget(name_input)
        layout.addLayout(name_layout)
        
        # Add save button
        save_btn = QPushButton("Save")
        
        def do_save():
            save_name = name_input.text() or None
            saved_name = self.solver.save_game_state(self.player_name, save_name)
            QMessageBox.information(self, 'Success', f'Game saved as "{saved_name}"')
            save_dialog.accept()
            
        save_btn.clicked.connect(do_save)
        layout.addWidget(save_btn)
        
        save_dialog.setLayout(layout)
        save_dialog.exec()
        
    def load_game(self):
        """Load a saved game state."""
        if not self.solver:
            return
            
        saves = self.solver.get_saved_games(self.player_name)
        if not saves:
            QMessageBox.information(self, 'No Saves', 'No saved games found')
            return
            
        # Create load game dialog
        load_dialog = QDialog(self)
        load_dialog.setWindowTitle('Load Game')
        load_dialog.setMinimumWidth(400)
        
        layout = QVBoxLayout()
        
        # Add saves list
        saves_list = QListWidget()
        for save in saves:
            item_text = (f"{save['name']} - {save['timestamp'][:19]} - "
                        f"{save['difficulty'].title()} - "
                        f"{save['progress']:.1f}% Complete")
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, save['name'])
            saves_list.addItem(item)
            
        layout.addWidget(saves_list)
        
        button_layout = QHBoxLayout()
        
        # Add load button
        load_btn = QPushButton("Load")
        load_btn.setEnabled(False)
        
        def do_load():
            selected = saves_list.currentItem()
            if selected:
                save_name = selected.data(Qt.UserRole)
                if self.solver.load_game_state(self.player_name, save_name):
                    # Update UI with loaded state
                    for i in range(9):
                        for j in range(9):
                            value = self.solver.grid[i][j]
                            is_original = self.solver.original_grid[i][j] != 0
                            self.cells[i][j].set_value(value, is_original)
                    self.game.current_puzzle = self.solver.grid.copy()
                    QMessageBox.information(self, 'Success', 'Game loaded successfully')
                    load_dialog.accept()
                else:
                    QMessageBox.warning(self, 'Error', 'Failed to load game')
                    
        load_btn.clicked.connect(do_load)
        button_layout.addWidget(load_btn)
        
        # Add delete button
        delete_btn = QPushButton("Delete")
        delete_btn.setEnabled(False)
        
        def do_delete():
            selected = saves_list.currentItem()
            if selected:
                save_name = selected.data(Qt.UserRole)
                if QMessageBox.question(self, 'Confirm Delete', 
                                     f'Delete save "{save_name}"?') == QMessageBox.Yes:
                    if self.solver.delete_saved_game(self.player_name, save_name):
                        saves_list.takeItem(saves_list.row(selected))
                        if saves_list.count() == 0:
                            load_dialog.accept()
                    else:
                        QMessageBox.warning(self, 'Error', 'Failed to delete save')
                        
        delete_btn.clicked.connect(do_delete)
        button_layout.addWidget(delete_btn)
        
        def selection_changed():
            has_selection = bool(saves_list.currentItem())
            load_btn.setEnabled(has_selection)
            delete_btn.setEnabled(has_selection)
            
        saves_list.itemSelectionChanged.connect(selection_changed)
        
        layout.addLayout(button_layout)
        load_dialog.setLayout(layout)
        load_dialog.exec()
        
def main():
    app = QApplication(sys.argv)

    # Set application style
    app.setStyle('Fusion')

    window = SudokuGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
