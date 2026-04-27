import numpy as np

def pivot(tableau, row, col):
    new_tableau = tableau.copy()
    new_tableau[row] /= new_tableau[row][col]

    for r in range(len(new_tableau)):
        if r != row:
            new_tableau[r] = new_tableau[r] - new_tableau[row]*new_tableau[r][col]
    
    return new_tableau


#test
# if __name__ == "__main__":
#     tableau = np.array([[2, 1, 1, 10], [1, 2, 1, 15], [1, 1, 2, 20]], dtype=float)
#     tableau = pivot(tableau, 1, 1)

#     print(tableau)