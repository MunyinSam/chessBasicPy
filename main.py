import pygame

pygame.init()
WIDTH = 1000
HEIGHT = 900
screen = pygame.display.set_mode([WIDTH,HEIGHT] , pygame.FULLSCREEN)
pygame.display.set_caption('Two Player pygame Chess')
font = pygame.font.Font('freesansbold.ttf', 20)
big_font = pygame.font.Font('freesansbold.ttf', 50)
timer = pygame.time.Clock()
fps = 60

# game variables and images
white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                 'pawn','pawn','pawn','pawn','pawn','pawn','pawn','pawn']
white_locations = [(0,0), (1,0), (2,0), (3,0), (4,0), (5,0),(6,0),(7,0),
                   (0,1), (1,1), (2,1), (3,1), (4,1), (5,1),(6,1),(7,1),]


black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                 'pawn','pawn','pawn','pawn','pawn','pawn','pawn','pawn']
black_locations = [(0,7), (1,7), (2,7), (3,7), (4,7), (5,7),(6,7),(7,7),
                   (0,6), (1,6), (2,6), (3,6), (4,6), (5,6),(6,6),(7,6),]

captured_pieces_white = []
captured_pieces_black = []

# 0 - white turn, no selection: 1-whites turn piece selected: 2- black turn no selection, 3 - black turn piece selected
turn_step = 0
selection = 100
valid_moves = []

# load in game piece images 
black_queen = pygame.image.load('assets/images/black queen.png')
black_queen = pygame.transform.scale(black_queen, (80, 80)) #file to use in original square
black_queen_small = pygame.transform.scale(black_queen, (45, 45)) #side small ver
black_king = pygame.image.load('assets/images/black king.png')
black_king = pygame.transform.scale(black_king, (80, 80))
black_king_small = pygame.transform.scale(black_king, (45, 45))
black_rook = pygame.image.load('assets/images/black rook.png')
black_rook = pygame.transform.scale(black_rook, (80, 80))
black_rook_small = pygame.transform.scale(black_rook, (45, 45))
black_bishop = pygame.image.load('assets/images/black bishop.png')
black_bishop = pygame.transform.scale(black_bishop, (80, 80))
black_bishop_small = pygame.transform.scale(black_bishop, (45, 45))
black_knight = pygame.image.load('assets/images/black knight.png')
black_knight = pygame.transform.scale(black_knight, (80, 80))
black_knight_small = pygame.transform.scale(black_knight, (45, 45))
black_pawn = pygame.image.load('assets/images/black pawn.png')
black_pawn = pygame.transform.scale(black_pawn, (65, 65))
black_pawn_small = pygame.transform.scale(black_pawn, (45, 45))
white_queen = pygame.image.load('assets/images/white queen.png')
white_queen = pygame.transform.scale(white_queen, (80, 80))
white_queen_small = pygame.transform.scale(white_queen, (45, 45))
white_king = pygame.image.load('assets/images/white king.png')
white_king = pygame.transform.scale(white_king, (80, 80))
white_king_small = pygame.transform.scale(white_king, (45, 45))
white_rook = pygame.image.load('assets/images/white rook.png')
white_rook = pygame.transform.scale(white_rook, (80, 80))
white_rook_small = pygame.transform.scale(white_rook, (45, 45))
white_bishop = pygame.image.load('assets/images/white bishop.png')
white_bishop = pygame.transform.scale(white_bishop, (80, 80))
white_bishop_small = pygame.transform.scale(white_bishop, (45, 45))
white_knight = pygame.image.load('assets/images/white knight.png')
white_knight = pygame.transform.scale(white_knight, (80, 80))
white_knight_small = pygame.transform.scale(white_knight, (45, 45))
white_pawn = pygame.image.load('assets/images/white pawn.png')
white_pawn = pygame.transform.scale(white_pawn, (65, 65))
white_pawn_small = pygame.transform.scale(white_pawn, (45, 45))

white_images = [white_pawn, white_queen, white_king, white_knight, white_rook, white_bishop]
small_white_images = [white_pawn_small, white_queen_small, white_king_small, white_knight_small,
                       white_rook_small, white_bishop_small]
black_images = [black_pawn, black_queen, black_king, black_knight, black_rook, black_bishop]
small_black_images = [black_pawn_small, black_queen_small, black_king_small, black_knight_small,
                       black_rook_small, black_bishop_small]
piece_list = ["pawn", "queen", "king", "knight", "rook", "bishop"]
#check variable/ flashing counter


# draw main game board
def draw_board():
    for i in range(32):
        column = i % 4 # 0 1 2 3 
        row = i // 4 
        if row % 2 == 0:
            pygame.draw.rect(screen, 'light gray', [600 - (column * 200), row * 100, 100, 100])
        else:
            pygame.draw.rect(screen, 'light grey', [700 - (column * 200), row * 100, 100, 100])
        pygame.draw.rect(screen, 'gray', [0, 800, WIDTH, 100])
        pygame.draw.rect(screen, 'gold', [0, 800, WIDTH, 100], 5)
        pygame.draw.rect(screen, 'gold', [ 800, 0, 200, HEIGHT], 5)

        status_text = ['White: Select a Piece to Move!', 'White: Select a Destination!',
                       'Black: Select a Piece to Move!', 'Black: Select a Destination!']
        screen.blit(big_font.render(status_text[turn_step], True, 'black'), (20,820)) # font.render = 3 args
        
        
        # draw like a border
        for i in range(9):
            pygame.draw.line(screen, 'black', (0, 100 * i), (800, 100 * i), 2) #thickness 2 on y axis
            pygame.draw.line(screen, 'black', (100 * i, 0), (100 * i , 800), 2) # x axis

# function to check legal moves
def check_options():
    pass

# draw pieces on board
def draw_pieces():
    
    for i in range(len(white_pieces)):
        index = piece_list.index(white_pieces[i])
        if white_pieces[i] == 'pawn':
            screen.blit(white_pawn, (white_locations[i][0] * 100 + 22, white_locations[i][1] * 100 + 30)) 
            #if your changing the screen size needs to change
        else: #print things that isnt a pawn
            screen.blit(white_images[index], (white_locations[i][0] * 100 + 10, white_locations[i][1] * 100 + 10))

        if turn_step < 2:
            if selection == i:
                pygame.draw.rect(screen, 'red', [white_locations[i][0] * 100 + 1, white_locations[i][1] * 100 + 1,
                                                 100 , 100], 2) 


# selection for pieces
    for i in range(len(black_pieces)):
        index = piece_list.index(black_pieces[i])
        if black_pieces[i] == 'pawn':
            screen.blit(black_pawn, (black_locations[i][0] * 100 + 22, black_locations[i][1] * 100 + 30)) 
            #if your changing the screen size needs to change
        else: #print things that isnt a pawn
            screen.blit(black_images[index], (black_locations[i][0] * 100 + 10, black_locations[i][1] * 100 + 10)) 
        
        if turn_step >= 2:
            if selection == i:
                pygame.draw.rect(screen, 'blue', [black_locations[i][0] * 100 + 1, black_locations[i][1] * 100 + 1,
                                                 100 , 100], 2) 


#main gameloop
run = True
while run:
    timer.tick(fps)
    screen.fill('dark grey')
    draw_board()
    draw_pieces()
    
    for event in pygame.event.get(): # getting all input
        if event.type == pygame.QUIT: # prebuilt pygame
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # left click
            x_coord = event.pos[0] // 100 #each grid is 100 wide and floor division will round down
            y_coord = event.pos[1] // 100
            clicks_coords = (x_coord, y_coord)

            if turn_step <= 1: #like turn_step<2
                if clicks_coords in white_locations:
                    selection = white_locations.index(clicks_coords)
                    if turn_step == 0:
                        turn_step = 1
                if clicks_coords in valid_moves and selection != 100: # a square that we are allowed to move
                    white_locations[selection] = clicks_coords

                    if clicks_coords in black_locations: #white takes black
                        black_piece = black_locations.index(clicks_coords) # checking the black piece with this coords
                        captured_pieces_white.append(black_pieces[black_piece])
                        black_pieces.pop(black_piece)
                        black_locations.pop(black_piece)

                    black_options = check_options(black_pieces, black_locations, 'black')
                    white_options = check_options(white_pieces, white_locations, 'white')

                    turn_step = 2
                    selection = 100
                    valid_moves = [] # re calculate

            if turn_step > 1: #like turn_step<2
                if clicks_coords in black_locations:
                    selection = black_locations.index(clicks_coords)
                    if turn_step == 2:
                        turn_step = 3
                if clicks_coords in valid_moves and selection != 100: # a square that we are allowed to move
                    black_locations[selection] = clicks_coords

                    if clicks_coords in white_locations: # takes
                        white_piece = white_locations.index(clicks_coords) # checking the black piece with this coords
                        captured_pieces_black.append(white_pieces[white_piece])
                        white_pieces.pop(white_piece)
                        white_locations.pop(white_piece)

                    black_options = check_options(black_pieces, black_locations, 'black')
                    white_options = check_options(white_pieces, white_locations, 'white')

                    turn_step = 0
                    selection = 100
                    valid_moves = [] # re calculate
        
    pygame.display.flip()
pygame.quit()