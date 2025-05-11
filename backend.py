# Tile class
import random
class Tile:
    def __init__(self):
        self.revealed = False
        self.type = None # Can be 'Path','Wall' or 'Coin'

    def reveal(self):
        if not self.revealed:
            self.type = random.choices(['Path','Wall','Coin'],weights=[0.5,0.25,0.25])[0]
            self.revealed = True
        return self.type

# finding the list of neighbours of the given tile to which we can move
def get_neighbours(row,col,grid):
    directions = [(-1,0),(0,-1),(1,0),(0,1)] # moving up,left,down,right respectively
    neighbours = []
    for dr,dc in directions:
        new_row,new_col = row+dr,col+dc
        if 0 <= new_row < 4 and 0 <= new_col < 4: # ensuring that new rows and colums are within the boundaries of the grid
            neighbours.append((new_row,new_col,grid[new_row][new_col]))
    return neighbours


class Game:
    def __init__(self,grid):
        self.state = "start" # State of the game
        self.grid = grid
        self.stamina = 6
        self.coins = 0

    # using depth first search approach
    def play(self):  
        firstType = self.grid[1][1].reveal() #starting from tile[1][1]

        if firstType != 'Wall':
            queue = [(1,1,self.grid[1][1])]  # store row,col and tile object using stack
            prev = (1,1,self.grid[1][1]) #used to backtrack when we step on a wall

        # Handling the case of first tile being a wall
        else:
            print("the first tile[1][1] is 'Wall'.")
            valid_moves = [(r,c,tile) for r,c,tile in get_neighbours(1,1,self.grid) if tile.reveal() != 'Wall'] # moving to one of its neighbours
            if not valid_moves: 
                print("Surrounded by walls!!") # No valid moves
                return
            queue = [(valid_moves[0][0],valid_moves[0][1],valid_moves[0][2])]

        visited = set() # A set which stores the indices of rows and columns of visited tiles

        while queue and self.state != "end":
            row,col,current = queue.pop()
            print(f"\nmoved to tile[{row}][{col}]")
            current_type = current.reveal() # Revealing the type only when we step on it
            if (row,col) in visited:
                if current.reveal() == 'Wall':
                    continue  # Do not revisit a tile which is a wall
                print("Already revealed")
            else:
                print(f"the tile[{row}][{col}] is {current_type}.")

            if current_type == 'Wall':
                if prev[2].reveal() != 'Wall':
                    self.stamina += 1 # increment the stamina, since backtracking from wall doesn't cost stamina
                    queue.append(prev) # back tracking to previous tile if the current tile is wall
                continue
            
            else:
                if (current_type == 'Coin') and (row,col) not in visited:
                    self.coins += 1 # Collecting the coins
                    print(f"number of coins is {self.coins}")

                if (row == 0 or col == 0 or row == 3 or col == 3) and self.coins >= 2:
                    self.state = "end"  # End the game if the boundary tile is reached with 2 coins
                    print(f"Edge reached!! with coins {self.coins}")
                    break   

                # Update the stamina after every move
                self.stamina -= 1
                if self.stamina == 0:
                    self.state = "end"  # end the game once you run out of stamina
                    print("Game Ended!! Out of stamina")
                    break

                visited.add((row,col))

                # Moving to one of its neigbours using dfs approach
                for r,c,neighbour in get_neighbours(row,col,self.grid):
                    queue.append((r,c,neighbour))
                
                # Updating the previous tile
                prev = (row,col,current) 

# intializing grid
Grid = [[Tile() for i in range(4)] for _ in range(4)]

# Creating a object of class game
game1 = Game(Grid)
game1.play()
