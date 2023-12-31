import pygame

pygame.init()
WIDTH = 1000
HEIGHT = 900
screen = pygame.display.set_mode([WIDTH,HEIGHT], pygame.RESIZABLE)
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
black_queen = pygame.image.load('assets/images/black_queen.png')
black_queen = pygame.transform.scale(black_queen, (80, 80)) #file to use in original square
black_queen_small = pygame.transform.scale(black_queen, (45, 45)) #side small ver
black_king = pygame.image.load('assets/images/black_king.png')
black_king = pygame.transform.scale(black_king, (80, 80))
black_king_small = pygame.transform.scale(black_king, (45, 45))
black_rook = pygame.image.load('assets/images/black_rook.png')
black_rook = pygame.transform.scale(black_rook, (80, 80))
black_rook_small = pygame.transform.scale(black_rook, (45, 45))
black_bishop = pygame.image.load('assets/images/black_bishop.png')
black_bishop = pygame.transform.scale(black_bishop, (80, 80))
black_bishop_small = pygame.transform.scale(black_bishop, (45, 45))
black_knight = pygame.image.load('assets/images/black_knight.png')
black_knight = pygame.transform.scale(black_knight, (80, 80))
black_knight_small = pygame.transform.scale(black_knight, (45, 45))
black_pawn = pygame.image.load('assets/images/black_pawn.png')
black_pawn = pygame.transform.scale(black_pawn, (65, 65))
black_pawn_small = pygame.transform.scale(black_pawn, (45, 45))
white_queen = pygame.image.load('assets/images/white_queen.png')
white_queen = pygame.transform.scale(white_queen, (80, 80))
white_queen_small = pygame.transform.scale(white_queen, (45, 45))
white_king = pygame.image.load('assets/images/white_king.png')
white_king = pygame.transform.scale(white_king, (80, 80))
white_king_small = pygame.transform.scale(white_king, (45, 45))
white_rook = pygame.image.load('assets/images/white_rook.png')
white_rook = pygame.transform.scale(white_rook, (80, 80))
white_rook_small = pygame.transform.scale(white_rook, (45, 45))
white_bishop = pygame.image.load('assets/images/white_bishop.png')
white_bishop = pygame.transform.scale(white_bishop, (80, 80))
white_bishop_small = pygame.transform.scale(white_bishop, (45, 45))
white_knight = pygame.image.load('assets/images/white_knight.png')
white_knight = pygame.transform.scale(white_knight, (80, 80))
white_knight_small = pygame.transform.scale(white_knight, (45, 45))
white_pawn = pygame.image.load('assets/images/white_pawn.png')
white_pawn = pygame.transform.scale(white_pawn, (65, 65))
white_pawn_small = pygame.transform.scale(white_pawn, (45, 45))

white_images = [white_pawn, white_queen, white_king, white_knight, white_rook, white_bishop]

white_promotions = 'queen'
black_promotions = 'queen'

small_white_images = [white_pawn_small, white_queen_small, white_king_small, white_knight_small,
                       white_rook_small, white_bishop_small]
black_images = [black_pawn, black_queen, black_king, black_knight, black_rook, black_bishop]
small_black_images = [black_pawn_small, black_queen_small, black_king_small, black_knight_small,
                       black_rook_small, black_bishop_small]
piece_list = ["pawn", "queen", "king", "knight", "rook", "bishop"]
#check variable/ flashing counter


# check var / flashing counter

counter = 0     
winner = ''
game_over = False
white_ep = (100, 100)
black_ep = (100, 100)
white_promote = False
black_promote = False
promo_index = 100


# draw main game board
def draw_board():
    for i in range(32):
        column = i % 4 # 0 1 2 3 
        row = i // 4 
        if row % 2 == 0:
            pygame.draw.rect(screen, 'dark green', [600 - (column * 200), row * 100, 100, 100])
        else:
            pygame.draw.rect(screen, 'dark green', [700 - (column * 200), row * 100, 100, 100])
        pygame.draw.rect(screen, 'gray', [0, 800, WIDTH, 100])
        pygame.draw.rect(screen, 'black', [0, 800, WIDTH, 100], 5)
        pygame.draw.rect(screen, 'black', [ 800, 0, 200, HEIGHT], 5)

        status_text = ['White: Select a Piece to Move!', 'White: Select a Destination!',
                       'Black: Select a Piece to Move!', 'Black: Select a Destination!']
        screen.blit(big_font.render(status_text[turn_step], True, 'black'), (20,820)) # font.render = 3 args
        
        
        # draw like a border
        for i in range(9):
            pygame.draw.line(screen, 'black', (0, 100 * i), (800, 100 * i), 2) #thickness 2 on y axis
            pygame.draw.line(screen, 'black', (100 * i, 0), (100 * i , 800), 2) # x axis
        screen.blit(big_font.render('Resign', True, 'black'), (810, 825))

        if white_promote or black_promote:
            pygame.draw.rect(screen, 'gray', [0, 800, WIDTH-200, 100])
            pygame.draw.rect(screen, 'black', [0, 800, WIDTH-200, 100], 5)
            screen.blit(big_font.render('Select piece to promote', True, 'black'), (20,820))

# function to check legal moves
def check_options(pieces, locations, turn):
    moves_list = []
    all_moves_list = []
    for i in range(len(pieces)):
        location = locations[i]
        piece = pieces[i]
        if piece == 'pawn':
            moves_list = check_pawn(location, turn)
        elif piece == 'rook':
            moves_list = check_rook(location, turn)
        elif piece == 'knight':
            moves_list = check_knight(location, turn)
        elif piece == 'bishop':
            moves_list = check_bishop(location, turn)
        elif piece == 'queen':
            moves_list = check_queen(location, turn)
        elif piece == 'king':
            moves_list = check_king(location, turn)
            
        all_moves_list.append(moves_list)

    return all_moves_list

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

# check legal pawn moves
def check_pawn(position, color):
    moves_list = []
    
    if color == 'white':

        
        #(position[0 = x], position[1 = y]) cause we gonna pass in 2 args in pos

        if (position[0], position[1] + 1) not in white_locations and \
                (position[0], position[1] + 1) not in black_locations and position[1] < 7:
            moves_list.append((position[0], position[1] + 1))
        if (position[0], position[1] + 2) not in white_locations and \
                (position[0], position[1] + 2) not in black_locations and position[1] == 1:
            moves_list.append((position[0], position[1] + 2))
        if (position[0] + 1, position[1] + 1) in black_locations:
            moves_list.append((position[0] + 1, position[1] + 1))
        if (position[0] - 1, position[1] + 1) in black_locations:
            moves_list.append((position[0] - 1, position[1] + 1))

        # promote


    else:
        if (position[0], position[1] - 1) not in white_locations and \
                (position[0], position[1] - 1) not in black_locations and position[1] > 0:
            moves_list.append((position[0], position[1] - 1))
        if (position[0], position[1] - 2) not in white_locations and \
                (position[0], position[1] - 2) not in black_locations and position[1] == 6:
            moves_list.append((position[0], position[1] - 2))
        if (position[0] + 1, position[1] - 1) in white_locations:
            moves_list.append((position[0] + 1, position[1] - 1))
        if (position[0] - 1, position[1] - 1) in white_locations:
            moves_list.append((position[0] - 1, position[1] - 1))
    return moves_list
    

# check rook legal moves
def check_rook(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations

    for i in range(4): #check down up right left
        path = True
        chain = 1
        if i == 0:
            x = 0
            y = 1
        elif i == 1:
            x = 0
            y = -1
        elif i == 2:
            x = 1
            y = 0
        else:
            x = -1
            y = 0
        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
            0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7: 
                # first line is checking any direction if we can go or not
                #check if its in between legal space and can move there
                moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves_list

# check knight legal moves
def check_knight(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations

        #move sets for knight
    targets = [(1,2), (1, -2), (2, 1), (2, -1),(-1, 2), (-1, -2), (-2, 1), (-2, -1)]
    for i in range(8):  
        #check the x pos of the target 0 of the index targets[i]
        target = (position[0] + targets[i][0] , position[1] + targets[i][1] )
        # target[0] x axis
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)


    return moves_list

# checks bishop legal moves
def check_bishop(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations

    for i in range(4): #check up-right up-left down-right down-left
        path = True
        chain = 1
        if i == 0:
            x = 1
            y = -1
        elif i == 1:
            x = -1
            y = -1
        elif i == 2:
            x = 1
            y = 1
        else:
            x = -1
            y = 1
        while path: #literally the same as rook
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
            0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7: 
                # first line is checking any direction if we can go or not
                #check if its in between legal space and can move there
                moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False

    
    return moves_list
    
# checks queen legal moves
def check_queen(position, color):
    moves_list = check_bishop(position, color)
    second_list = check_rook(position, color)
    for i in range(len(second_list)):
        moves_list.append(second_list[i])

 
    
    # u can return second list but it wont give u any bishop move cause theres no var that except seocnd list
    return moves_list

# checks king legal moves
def check_king(position, color):
    
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations

    # 8 square available
    targets = [(1,0), (1, 1), (1, -1), (-1, 0),(-1, 1), (-1, -1), (0, 1), (0, -1)]
    for i in range(8):  
        #check the x pos of the target 0 of the index targets[i]
        target = (position[0] + targets[i][0] , position[1] + targets[i][1] )
        # target[0] x axis
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)

    return moves_list

# check for valid moves for just selected piece
def check_valid_moves():
    if turn_step < 2:
        options_list = white_options
    else:
        options_list = black_options
    valid_options = options_list[selection]
    return valid_options


# draw valid moves on screen
def draw_valid(moves):
    if turn_step < 2:
        color = 'red'
    else:
        color = 'blue'
    for i in range(len(moves)):

        if turn_step < 2:

            pygame.draw.rect(screen, 'red', [moves[i][0] * 100 + 1, 
                                                            moves[i][1] * 100 + 1, 100, 100], 7)
        #pygame.draw.circle(screen, color, (moves[i][0] * 100 + 50, moves[i][1] * 100 + 50), 5)

        else:
            pygame.draw.rect(screen, 'blue', [moves[i][0] * 100 + 1, 
                                                            moves[i][1] * 100 + 1, 100, 100], 7)



# draw captured pieces on the side of the screen
def draw_captured():
    for i in range(len(captured_pieces_white)):
        captured_piece = captured_pieces_white[i]
        index = piece_list.index(captured_piece)
        screen.blit(small_black_images[index], (825, 5 + 50*i))

    for i in range(len(captured_pieces_black)):
        captured_piece = captured_pieces_black[i]
        index = piece_list.index(captured_piece)
        screen.blit(small_white_images[index], (925, 5 + 50*i))

# draw a flashing square around the king
def draw_check():

    if turn_step < 2:
        if 'king' in white_pieces:

            king_index = white_pieces.index('king')
            king_location = white_locations[king_index]
            for i in range(len(black_options)): #all of the black pieces and the current move
                if king_location in black_options[i]:
                    if counter < 15:  # itll flutter red cause counter
                        pygame.draw.rect(screen, 'dark red', [white_locations[king_index][0] * 100 + 1, 
                                                            white_locations[king_index][1] * 100 + 1, 100, 100], 5)


    else:
        if 'king' in black_pieces:

            king_index = black_pieces.index('king')
            king_location = black_locations[king_index]
            for i in range(len(white_options)): #all of the black pieces and the current move
                if king_location in white_options[i]:
                    if counter < 15:
                        pygame.draw.rect(screen, 'dark blue', [black_locations[king_index][0] * 100 + 1, 
                                                            black_locations[king_index][1] * 100 + 1, 100, 100], 5)



def draw_game_over():
    pygame.draw.rect(screen, 'black', [200, 200, 400, 70])
    screen.blit(font.render(f'{winner} won the game!', True, 'white'), (210, 210))
    screen.blit(font.render(f'Press ENTER to Restart!', True, 'white'), (210, 240))

def check_promotion():
    pawn_indexes = []
    white_promotion = False
    black_promotion = False
    promote_index = 100
    for i in range(len(white_pieces)):
        if white_pieces[i] == 'pawn':
            pawn_indexes.append(i)
    for i in range(len(pawn_indexes)):
        if white_locations[pawn_indexes[i]][1] == 7:
            white_promotion = True
            promote_index = pawn_indexes[i]
    pawn_indexes = []
    for i in range(len(black_pieces)):
        if black_pieces[i] == 'pawn':
            pawn_indexes.append(i)
    for i in range(len(pawn_indexes)):
        if black_locations[pawn_indexes[i]][1] == 0:
            black_promotion = True
            promote_index = pawn_indexes[i]
    return white_promotion, black_promotion, promote_index



def draw_promotion(): # draw the promotion option screen
   # pygame.draw.rect(screen, 'dark gray', [800, 0, 200, 420]) # draw a rect on top of the score board
    if white_promote:
        color = 'white'
        
        piece = white_promotions
        index = piece_list.index(piece)
            #screen.blit(white_images[index], (860, 5 + 100 * i))

    elif black_promote:
        color = 'black'
        
        piece = black_promotions
        index = piece_list.index(piece)
            #screen.blit(black_images[index], (860, 5 + 100 * i))
    #pygame.draw.rect(screen, color, [800, 0, 200, 420], 6)


def check_promo_select():
    mouse_pos = pygame.mouse.get_pos()
    left_click = pygame.mouse.get_pressed()[0]
    x_pos = mouse_pos[0] // 100 #cause our square is 100 wide
    y_pos = mouse_pos[1] // 100
    if white_promote and y_pos >7:
        white_pieces[promo_index] = white_pieces[4]
        print("Yes")
    elif black_promote and y_pos <7:
        black_pieces[promo_index] = black_pieces[4]


#main gameloop
black_options = check_options(black_pieces, black_locations, 'black')
white_options = check_options(white_pieces, white_locations, 'white')
run = True
while run:
    timer.tick(fps)

    if counter < 30:
        counter += 1
    else:
        counter = 0
    
    screen.fill('light yellow')
    draw_board()
    draw_pieces()
    draw_captured()
    draw_check()
    if not game_over:
        white_promote, black_promote, promo_index = check_promotion()
        if white_promote or black_promote:
            draw_promotion()
            check_promo_select()
            
    if selection != 100:
        valid_moves = check_valid_moves()
        draw_valid(valid_moves)
    
    
    for event in pygame.event.get(): # getting all input
        if event.type == pygame.QUIT: # prebuilt pygame
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over: # left click
            x_coord = event.pos[0] // 100 #each grid is 100 wide and floor division will round down
            y_coord = event.pos[1] // 100
            clicks_coords = (x_coord, y_coord)


            # piece taking
            if turn_step <= 1: #like turn_step<2
                if clicks_coords == (8, 8) or clicks_coords == (9, 8):
                    winner = 'black'
                if clicks_coords in white_locations:
                    selection = white_locations.index(clicks_coords)
                    if turn_step == 0:
                        turn_step = 1
                if clicks_coords in valid_moves and selection != 100: # a square that we are allowed to move
                    white_locations[selection] = clicks_coords

                    if clicks_coords in black_locations: #white takes black
                        black_piece = black_locations.index(clicks_coords) # checking the black piece with this coords
                        captured_pieces_white.append(black_pieces[black_piece])
                        if black_pieces[black_piece] == 'king':
                            winner = 'white'

                        black_pieces.pop(black_piece)
                        black_locations.pop(black_piece)

                    black_options = check_options(black_pieces, black_locations, 'black')
                    white_options = check_options(white_pieces, white_locations, 'white')

                    turn_step = 2
                    selection = 100
                    valid_moves = [] # re calculate

            if turn_step > 1: #like turn_step<2
                if clicks_coords == (8, 8) or clicks_coords == (9, 8):
                    winner = 'white'
                if clicks_coords in black_locations:
                    selection = black_locations.index(clicks_coords)
                    if turn_step == 2:
                        turn_step = 3
                if clicks_coords in valid_moves and selection != 100: # a square that we are allowed to move
                    black_locations[selection] = clicks_coords

                    if clicks_coords in white_locations: # takes
                        white_piece = white_locations.index(clicks_coords) # checking the black piece with this coords
                        captured_pieces_black.append(white_pieces[white_piece])
                        if white_pieces[white_piece] == 'king':
                            winner = 'black'
                        white_pieces.pop(white_piece)
                        white_locations.pop(white_piece)

                    black_options = check_options(black_pieces, black_locations, 'black')
                    white_options = check_options(white_pieces, white_locations, 'white')

                    turn_step = 0
                    selection = 100
                    valid_moves = [] # re calculate
        
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_RETURN: #ENTER KEY
                game_over = False
                winner = ''
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
                turn_step = 0
                selection = 100
                valid_moves = []

                black_options = check_options(black_pieces, black_locations, 'black')
                white_options = check_options(white_pieces, white_locations, 'white')
            


    if winner != '':
        game_over = True
        draw_game_over()

    pygame.display.flip()
pygame.quit()