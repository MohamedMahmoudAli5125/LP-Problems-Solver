import numpy as np

def pivot(tableau, row, col):
    new_tableau = tableau.copy()
    new_tableau[row] /= new_tableau[row][col]

    for r in range(len(new_tableau)):
        if r != row:
            new_tableau[r] = new_tableau[r] - new_tableau[row]*new_tableau[r][col]
    
    return new_tableau