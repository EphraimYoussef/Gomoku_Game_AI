import math
import random


emptyCell = 0
PLAYER = 1
miniMaxAI = 2
AlphaBetaAI = 3


class Gomoku:
    def __init__(self, boardSize):
        self.boardSize = boardSize
        self.board = [[emptyCell for _ in range(boardSize)] for _ in range(boardSize)]
        self.winCondition = 5

    def printBoard(self):
        print("   " + "|".join(f"{i:2}" for i in range(self.boardSize)))
        print("---" + "+".join(["--"] * self.boardSize))
        for idx, row in enumerate(self.board):
            rowStr = "|".join(self.cellSymbol(cell) for cell in row)
            print(f"{idx:2} |{rowStr}")

    def cellSymbol(self, cell):
        if cell == emptyCell:
            return " ."
        elif cell == PLAYER:
            return " X"
        elif cell == miniMaxAI:
            return " M"
        elif cell == AlphaBetaAI:
            return " A"

    def isValidMove(self, row, col):
        return 0 <= row < self.boardSize and 0 <= col < self.boardSize and self.board[row][col] == emptyCell

    def makeMove(self, row, col, player):
        if self.isValidMove(row, col):
            self.board[row][col] = player
            return True
        return False
    def randomFreeCellIndex(self):
        count = self.freeCellsCounter()
        if count == 0:
            return None
        return random.randrange(count)

    def checkWinner(self, player):
        for row in range(self.boardSize):
            for col in range(self.boardSize):
                if any(self.checkLine(row, col, dr, dc, player) for dr, dc in ((1, 0), (0, 1), (1, 1), (1, -1))):
                    return True
        return False

    def checkLine(self, row, col, dr, dc, player):
        for i in range(self.winCondition):
            r, c = row + dr * i, col + dc * i
            if not (0 <= r < self.boardSize and 0 <= c < self.boardSize and self.board[r][c] == player):
                return False
        return True

    def getValidMoves(self):
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),          (0, 1),
                      (1, -1), (1, 0), (1, 1)]
        valid_moves = set()

        for r in range(self.boardSize):
            for c in range(self.boardSize):
                if self.board[r][c] != emptyCell:
                    for dr, dc in directions:
                        nr, nc = r + dr, c + dc
                        if self.isValidMove(nr, nc):
                            valid_moves.add((nr, nc))

        if not valid_moves:
            return [(r, c) for r in range(self.boardSize)
                    for c in range(self.boardSize)
                    if self.isValidMove(r, c)]

        return list(valid_moves)

    def freeCellsCounter(self):
        return len(self.getValidMoves())

    def isDraw(self):
        if self.freeCellsCounter() > 1:
            return False
        return not (self.checkWinner(PLAYER) or self.checkWinner(miniMaxAI) or self.checkWinner(AlphaBetaAI))

    def evaluate(self, maximizingPlayer):

        weights = {1: 10, 2: 100, 3: 1000, 4: 10000}
        score = 0
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        opponents = {PLAYER, miniMaxAI, AlphaBetaAI} - {maximizingPlayer}

        for dr, dc in directions:
            for row in range(self.boardSize):
                for col in range(self.boardSize):
                    cntMax, cntOpp = 0, 0
                    for i in range(self.winCondition): # checking 5s in a row
                        r, c = row + dr * i, col + dc * i
                        if not (0 <= r < self.boardSize and 0 <= c < self.boardSize):
                            break
                        cell = self.board[r][c]
                        if cell == maximizingPlayer:
                            cntMax += 1
                        elif cell in opponents:
                            cntOpp += 1
                        else:
                            if cntMax > 0 and cntOpp == 0:
                                score += weights.get(cntMax, 0)
                            elif cntOpp > 0 and cntMax == 0:
                                score -= weights.get(cntOpp, 0)
        return score

    def minimax(self, depth, isMaximizing, depthLimit ,currrentPLayer =PLAYER):

        if self.checkWinner(miniMaxAI):
            return math.inf, None
        if self.checkWinner(currrentPLayer):
            return -math.inf, None
        if depth == depthLimit :
            return self.evaluate(miniMaxAI), None

        moves = self.getValidMoves()

        bestMove = moves[self.randomFreeCellIndex()]
        if isMaximizing:
            maxEval = -math.inf
            for move in moves:
                self.makeMove(*move, miniMaxAI)
                evalScore, _ = self.minimax(depth + 1, False, depthLimit)
                self.board[move[0]][move[1]] = emptyCell
                if evalScore > maxEval:
                    maxEval, bestMove = evalScore, move
            return maxEval, bestMove
        else:
            minEval = math.inf
            for move in moves:
                self.makeMove(*move, PLAYER)
                evalScore, _ = self.minimax(depth + 1, True, depthLimit)
                self.board[move[0]][move[1]] = emptyCell
                if evalScore < minEval:
                    minEval, bestMove = evalScore, move
            return minEval, bestMove

    def alphaBeta(self, depth, isMaximizing, alpha=-math.inf, beta=math.inf):

        if self.checkWinner(AlphaBetaAI):
            return math.inf, None
        if self.checkWinner(miniMaxAI):
            return -math.inf, None
        if depth == 0:
            return self.evaluate(AlphaBetaAI), None

        moves = self.getValidMoves()

        bestMove = moves[self.randomFreeCellIndex()]
        if isMaximizing:
            maxEval = -math.inf
            for move in moves:
                self.makeMove(*move, AlphaBetaAI)
                evalScore, _ = self.alphaBeta(depth - 1, False, alpha, beta)
                self.board[move[0]][move[1]] = emptyCell
                if evalScore > maxEval:
                    maxEval, bestMove = evalScore, move
                alpha = max(alpha, evalScore)
                if beta <= alpha:
                    break
            return maxEval, bestMove
        else:
            minEval = math.inf
            for move in moves:
                self.makeMove(*move, miniMaxAI)
                evalScore, _ = self.alphaBeta(depth - 1, True, alpha, beta)
                self.board[move[0]][move[1]] = emptyCell
                if evalScore < minEval:
                    minEval, bestMove = evalScore, move
                beta = min(beta, evalScore)
                if beta <= alpha:
                    break
            return minEval, bestMove
def main():
    print("Welcome to Gomoku! Connect five in a row to win.")
    while True:
        try:
            size = int(input("Enter board size (>=5): "))
            if size < 5:
                print("Board size must be at least 5.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter an integer.")

    game = Gomoku(size)

    # game mode
    while True:
        try:
            mode = int(input("Select mode: \n1 - Human vs Minimax AI\n2 - Minimax AI vs AlphaBeta AI: "))
            if mode not in (1, 2):
                print("Please select 1 or 2.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter 1 or 2.")

    # AI depth inputs
    while True:
        try:
            depthLimit = int(input("Enter depth limit for Minimax AI (>=1): "))
            if depthLimit < 1:
                print("Depth must be at least 1.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter an integer.")

    while True:
        try:
            abDepth = int(input("Enter depth limit for AlphaBeta AI (>=1): "))
            if abDepth < 1:
                print("Depth must be at least 1.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter an integer.")

    game.printBoard()

    while True:
        if mode == 1:
            while True:
                try:
                    move = input("Enter your move as 'row,col': ")
                    r, c = map(int, move.split(','))
                    if game.makeMove(r, c, PLAYER):
                        break
                    else:
                        print("Invalid move. Cell occupied or out of range.")
                except Exception:
                    print("Invalid format. Use row,col.")
            game.printBoard()
            if game.checkWinner(PLAYER):
                print("Congratulations, you win!")
                break
            if game.isDraw():
                print("Game is a draw.")
                break

            print("Minimax AI is thinking...")
            _, move = game.minimax(0, True, depthLimit )
            if move is None:
                print("No moves left—game over.")
                break
            game.makeMove(*move, miniMaxAI)
            print(f"Minimax AI played at: {move}")
            game.printBoard()
            if game.checkWinner(miniMaxAI):
                print("Minimax AI wins!")
                break
            if game.isDraw():
                print("Game is a draw.")
                break

        else:
            print("Minimax AI's turn...")
            _, move = game.minimax(0, True, depthLimit ,AlphaBetaAI)
            game.makeMove(*move, miniMaxAI)
            print(f"Minimax AI played at: {move}")
            game.printBoard()
            if game.checkWinner(miniMaxAI):
                print("Minimax AI wins!")
                break
            if game.isDraw():
                print("Game is a draw.")
                break

            print("AlphaBeta AI's turn...")
            _, move = game.alphaBeta(abDepth, True)

            game.makeMove(*move, AlphaBetaAI)
            print(f"AlphaBeta AI played at: {move}")
            game.printBoard()
            if game.checkWinner(AlphaBetaAI):
                print("AlphaBeta AI wins!")
                break
            if game.isDraw():
                print("Game is a draw.")
                break


if __name__ == "__main__":
   main()