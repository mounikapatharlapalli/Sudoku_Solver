from tkinter import *
from tkinter import messagebox

root = Tk()
root.geometry('450x500')
root.title("Sudoku Solver")
root.configure(bg='#f0f0f0')

# Sudoku solver class
class SudokuSolver():

    def __init__(self):
        self.setZero()
        
    # Set the empty cells to 0 (i.e. the cells you have not filled in)
    def setZero(self):
        for i in range(9):
            for j in range(9):
                if filledBoard[i][j].get() not in ['1','2','3','4','5','6','7','8','9']:
                    filledBoard[i][j].set('0')

    # Solve using backtracking    
    def solve(self):
        # Find next empty cell
        findEmpty = self.emptyCell()
        
        if not findEmpty:
            return True   
        else:
            row, column = findEmpty
        
        for i in range(1, 10):
            if self.isValid(i, (row, column)):
                filledBoard[row][column].set(str(i))

                if self.solve():
                    return True

                filledBoard[row][column].set('0')
        
        return False

    # Check row, column and subgrid(3x3 square) to see if number can be placed in cell          
    def isValid(self, num, pos):
        # Check Row
        for i in range(9):
            if filledBoard[pos[0]][i].get() == str(num):
                return False
        # Check Column 
        for i in range(9):
            if filledBoard[i][pos[1]].get() == str(num):
                return False

        # Check Sub Grid
        row = pos[0] // 3 
        column = pos[1] // 3 

        for i in range(row * 3, (row * 3) + 3):
            for j in range(column * 3, (column * 3) + 3):
                if filledBoard[i][j].get() == str(num):
                    return False 
        return True

    # Find empty cells, defined as cells filled with a zero
    def emptyCell(self):
        for row in range(9):
            for column in range(9):
                if filledBoard[row][column].get() == '0':
                    return (row, column)
        return None

# GUI class
class Interface():
    def __init__(self, window):
        self.window = window

        font = ('Arial', 20)
        button_font = ('Arial', 15)
        cell_color = '#ffffff'
        alt_cell_color = '#d3d3d3'
        button_color = '#007acc'
        button_text_color = '#ffffff'

        # Create solve and clear button and link them to Solve and Clear methods
        solve = Button(window, text='Solve', command=self.Solve, font=button_font, bg=button_color, fg=button_text_color)
        solve.grid(column=3, row=20, pady=20)
        clear = Button(window, text='Clear', command=self.Clear, font=button_font, bg=button_color, fg=button_text_color)
        clear.grid(column=5, row=20, pady=20)

        # Initialize empty 2D list
        self.board = []
        for row in range(9):
            self.board += [["", "", "", "", "", "", "", "", ""]]

        for row in range(9):
            for col in range(9):
                # Change color of cells depending on position in grid
                if (row < 3 or row > 5) and (col < 3 or col > 5):
                    color = cell_color
                elif (row >= 3 and row < 6) and (col >= 3 and col < 6):
                    color = cell_color
                else:
                    color = alt_cell_color
                
                # Make each cell of grid an entry box and store each user entry into the filledBoard 2D list
                self.board[row][col] = Entry(window, width=2, font=font, bg=color, cursor='arrow', borderwidth=2,
                                             highlightcolor='yellow', highlightthickness=0, highlightbackground='black', 
                                             textvariable=filledBoard[row][col])
                self.board[row][col].bind('<FocusIn>', self.gridChecker)
                self.board[row][col].bind('<Motion>', self.gridChecker)                        
                self.board[row][col].grid(row=row, column=col, padx=5, pady=5)

    # Function to check if user enters a value which is not an int between 1 and 9 (valid numbers in Sudoku game).
    # If entry is not valid, clear value
    def gridChecker(self, event):
        for row in range(9):
            for col in range(9):
                if filledBoard[row][col].get() not in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '']:
                    filledBoard[row][col].set('')

    # Call Sudoku solver class (called by solve button)
    def Solve(self):
        if self.isValidInput():
            solver = SudokuSolver()
            if not solver.solve():
                messagebox.showerror("Error", "No solution exists!")
        else:
            messagebox.showerror("Error", "Invalid input! Check for duplicate numbers or incorrect entries.")

    # Function to clear board (called by clear button) 
    def Clear(self):
        for row in range(9):
            for col in range(9):
                filledBoard[row][col].set('')

    # Validate the input board before solving
    def isValidInput(self):
        for i in range(9):
            row_check = set()
            col_check = set()
            for j in range(9):
                # Check rows and columns for duplicates
                if filledBoard[i][j].get() in row_check and filledBoard[i][j].get() != '0' and filledBoard[i][j].get() != '':
                    return False
                if filledBoard[j][i].get() in col_check and filledBoard[j][i].get() != '0' and filledBoard[j][i].get() != '':
                    return False
                if filledBoard[i][j].get() != '0' and filledBoard[i][j].get() != '':
                    row_check.add(filledBoard[i][j].get())
                if filledBoard[j][i].get() != '0' and filledBoard[j][i].get() != '':
                    col_check.add(filledBoard[j][i].get())

        # Check 3x3 subgrids for duplicates
        for i in range(3):
            for j in range(3):
                subgrid_check = set()
                for row in range(i * 3, (i + 1) * 3):
                    for col in range(j * 3, (j + 1) * 3):
                        if filledBoard[row][col].get() in subgrid_check and filledBoard[row][col].get() != '0' and filledBoard[row][col].get() != '':
                            return False
                        if filledBoard[row][col].get() != '0' and filledBoard[row][col].get() != '':
                            subgrid_check.add(filledBoard[row][col].get())

        return True

# Global 2D list which saves the values the user enters on the GUI
# Each value in the 2D list is set as a StringVar(), a class in Tkinter
# which allows you to save values users enter into the Entry widget
filledBoard = []
for row in range(9): 
    filledBoard += [["", "", "", "", "", "", "", "", ""]]
for row in range(9):
    for col in range(9):
        filledBoard[row][col] = StringVar(root)    

# Main Loop
Interface(root)
root.mainloop()
