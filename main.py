import pygame, math, copy, os

pygame.init()

WIN_WIDTH = 800
WIN_HEIGHT = 800
ICON_IMG = pygame.image.load(os.path.join("imgs","cross.png"))
CROSS_IMG = pygame.transform.scale(pygame.image.load(os.path.join("imgs","cross.png")), (150, 150))
NOUGHT_IMG = pygame.transform.scale(pygame.image.load(os.path.join("imgs","nought.png")), (150, 150))
PLAYERS = {1 : CROSS_IMG, -1 : NOUGHT_IMG}
GRID_IMG = pygame.transform.scale(pygame.image.load(os.path.join("imgs","grid.png")), (600, 600))
FONT = pygame.font.SysFont("georgia", 50)

class Board:
    def __init__(self, board = [0, 0, 0, 0, 0, 0, 0, 0, 0]):
        self.board = board

    def makeMove(self, pos, player):
        if self.board[pos] == 0:
            self.board[pos] = player
            return True
        else:
            return False

    def getMove(self, pos, player):
        new_board = copy.copy(self.board)
        new_board[pos] = player
        return new_board
        
    def checkWin(self, player, score = 3):
        for i in range(3):
            if sum(self.board[i * 3:(i * 3) + 3]) == score * player:
                return True
            if sum([ self.board[x] for x in range(i, i + 7, 3) ]) == score * player:
                return True
        if sum([ self.board[x] for x in range(0, 9, 4) ]) == score * player:
            return True
        if sum([ self.board[x] for x in range(2, 7, 2) ]) == score * player:
            return True

    def calculateScore(self):
        score = 0
        if self.checkWin(1):
            score += 5
        if self.checkWin(-1):
            score -= 5
        if self.checkWin(1, 2):
            score += 1
        if self.checkWin(-1, 2):
            score -= 1
        return score
        
    def generateBoards(self, player):
        boards = []
        for pos in range(9):
            if self.board[pos] == 0:
                boards.append(((pos, player), Board(self.getMove(pos, player))))
        return boards

    def getEmpty(self):
        n = 0
        for value in self.board:
            if value != 0:
                n += 1
        return 9 - n

    def displayBoard(self, win):
        positions = [ (x, y) for y in range(3) for x in range(3) ]
        for i, pos in [ (i, positions[i]) for i in range(9)]:
            if self.board[i] != 0:
                win.blit(PLAYERS[self.board[i]], (pos[0] * 200 + 25, pos[1] * 200 + 25))

def minimax(board, depth, alpha, beta, maximizingPlayer):
    if depth == 0 or board.checkWin(-1) or board.checkWin(1):
        return board.calculateScore(), (0, 0)
    if maximizingPlayer:
        value = -math.inf
        bestMove = None
        for move, result in board.generateBoards(1):
            old_value = value
            value = max(value, minimax(result, depth - 1, alpha, beta, False)[0])
            if old_value != value:
                bestMove = move
            alpha = max(alpha, value)
            if alpha >= beta:
                break
    else:
        value = math.inf
        bestMove = None
        for move, result in board.generateBoards(-1):
            old_value = value
            value = min(value, minimax(result, depth - 1, alpha, beta, True)[0])
            if old_value != value:
                bestMove = move
            beta = min(beta, value)
            if beta <= alpha:
                break
    return value, bestMove

def drawGame(screen, win, board, won, winner):
    win.blit(GRID_IMG, (0, 0))
    board.displayBoard(win)
    screen.fill([255, 255, 255])
    screen.blit(win, (100, 100))
    if won:
        win_text = FONT.render(winner, 1, (0, 0, 0))
        restart_text = FONT.render("Press 'R' to restart.", 1, (0, 0, 0))
        screen.blit(win_text, (400 - (win_text.get_width() // 2), 10))
        screen.blit(restart_text, (400 - (restart_text.get_width() // 2), 800 - 30 - restart_text.get_height()))
    pygame.display.update()

pygame.display.set_caption("Noughts & Crosses")
pygame.display.set_icon(ICON_IMG)
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
win = pygame.Surface((600, 600))

clock = pygame.time.Clock()

b = Board()

turn = 1
winner = 0
player = 1

run = True
playing = True

while run:
    clock.tick(60)

    if b.checkWin(player) and playing:
        winner = "Player wins!"
        playing = False
    if b.checkWin(-player) and playing:
        winner = "Computer wins!"
        playing = False
    if b.getEmpty() == 0 and playing:
        winner = "Draw!"
        playing = False

    if turn == -player:
        b.makeMove(minimax(b, b.getEmpty(), -math.inf, math.inf, -player == 1)[1][0], -player)
        turn = player

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN and turn == player and playing:
            if event.button == 1:
                positions = [ (x, y) for y in range(3) for x in range(3) ]
                pos = pygame.mouse.get_pos()
                pos = (pos[0] - 100) // 200, (pos[1] - 100) // 200
                if pos[0] >= 0 and pos[0] <= 2 and pos[1] >= 0 and pos[1] <= 2:
                    if b.makeMove(positions.index(pos), player):
                        turn = -player
        elif event.type == pygame.KEYDOWN and not playing:
            if event.key == pygame.K_r:
                player = -player
                turn = player
                if player == 1:
                    b = Board([0, 0, 0, 0, 0, 0, 0, 0, 0])
                else:
                    b = Board([1, 0, 0, 0, 0, 0, 0, 0, 0])
                playing = True
            
    drawGame(screen, win, b, not playing, winner)