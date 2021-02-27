import pygame
import sys
from constants import WINDOW_HEIGHT, WINDOW_WIDTH, FRAMES, WHEAT
from board import Board
import pygame_textinput as pyti

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Catan Companion')

# on click set selected_tile to hexa that was clicked on
def select_tile(game_board, hexa):
    game_board.selected_tile = hexa

# if a board hex was selected and a terrain button was pressed, resolve board changes
def resolve_selections(game_board, hexa):
    resource_to_tile = {
            'bricks' : 'assets/bricks.png',
            'forest': 'assets/forest.png',
            'wheat': 'assets/wheat.png',
            'rocks' : 'assets/rocks.png',
            'pasture' : 'assets/pasture.png',
            'desert' : 'assets/desert.png'
        }
    if game_board.selected_tile:
        hexa_to_change = game_board.selected_tile
        tile_surf = pygame.image.load(resource_to_tile[hexa.resource]).convert_alpha()
        hexa_to_change.resource = hexa.resource
        hexa_to_change.image = pygame.transform.scale(tile_surf, hexa_to_change.scale)
        hexa_to_change.rect = hexa_to_change.image.get_rect(center = hexa_to_change.center)
        hexa_to_change.mask = pygame.mask.from_surface(hexa_to_change.image) 


def draw_screen(window, game_board):
    window.fill(pygame.Color(120, 118, 255))
    game_board.draw_hex_board(window)
    game_board.draw_drawer(window)
    game_board.draw_loc_board(window)

def click_numpad(window, game_board, hexa):
    try:
        hexa_to_change = game_board.selected_tile
        hexa_to_change.value = hexa.value
        img = pygame.image.load('assets/tile_numbers/' + str(hexa.value) + '.png').convert_alpha()
        hexa_to_change.tile_num_image = pygame.transform.scale(img, (36, 40))
    except:
        pass

def select_loc(game_board, loc):
    if loc.taken:
        loc.taken = False
    else:
        loc.taken = True

def check_loc(game_board, x, y):
    for row in game_board.loc_board:
        for loc in row:
            if loc == 0:
                continue
            else:
                if loc.rect.collidepoint((x,y)):
                    select_loc(game_board, loc)
                    return True
    return False
def check_hex(game_board, x, y):
    for row in game_board.hex_board:
        for hexa in row:
            if hexa == None:
                continue
            pos_in_mask = x - hexa.rect.x, y - hexa.rect.y
            # checks if mouse position overlaps with .rect and .mask of hexa
            if hexa.rect.collidepoint((x, y)) and hexa.mask.get_at(pos_in_mask):
                select_tile(game_board, hexa)
                return True
    return False

def check_calc(game_board, x, y):
    return game_board.calc_button_rect.collidepoint((x, y))


def click_calc(game_board):
    i_arr = [-1, 0, 1, 2]
    j_arr = [-1, 0, 1]
    #good_points = set(((0,1), (1,0), (2,0), (3,1), (1, 2), (2,2)))
    for row in game_board.loc_board:
        for loc in row:
            for i, i_index in enumerate(i_arr):
                for j, j_index in enumerate(j_arr):
                    # if (i,j) not in good_points:
                    #     continue
                    try:
                        row = int((loc.row - i_index)/2) - 1
                        col = int((loc.col - j_index)/2) - 1
                        if row == 1 or row == 3:
                            col-=.5
                        loc.adj.add(game_board.hex_board[row][col])
                    except:
                        pass
                    

def main():
    run = True
    clock = pygame.time.Clock()
    game_board = Board()
    game_board.create_loc_board(WINDOW)
    game_board.draw_loc_board(WINDOW)
    draw_screen(WINDOW, game_board)
    while run:
        events = pygame.event.get()
        for event in events:
            x, y = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # checks for loc clicks
                if check_loc(game_board, x, y):
                    draw_screen(WINDOW, game_board)
                    continue
                # checks for clicks on board hexa's
                if check_hex(game_board, x, y):
                    draw_screen(WINDOW, game_board)
                    continue
                # checks if calculate button has been clicked
                if check_calc(game_board, x, y):
                    click_calc(game_board)
                    print('here')
                    print(game_board.loc_board[1][4].adj)
                    for hexa in game_board.loc_board[1][4].adj:
                        print(hexa.value, hexa.resource)
                    print('\n')
                    for hexa in game_board.loc_board[1][6].adj:
                        print(hexa.value, hexa.resource)
                    print('\n')
                    for hexa in game_board.loc_board[3][5].adj:
                        print(hexa.value, hexa.resource)
                    print('\n')
                    for hexa in game_board.loc_board[2][4].adj:
                        print(hexa.value, hexa.resource)
                    print('\n')
                    # for hexa in game_board.loc_board[3][3].adj:
                    #     print(hexa.value, hexa.resource)
                # checks for clicks on terrain buttons
                for row in game_board.hex_buttons:
                    for hexa in row:
                        if hexa == None:
                            continue
                        pos_in_mask = x - hexa.rect.x, y - hexa.rect.y
                        if hexa.rect.collidepoint((x, y)) and hexa.mask.get_at(pos_in_mask):
                            resolve_selections(game_board, hexa)

                for num in game_board.select_nums[1:]:
                    if num.rect.collidepoint((x, y)):
                        click_numpad(WINDOW, game_board, num)
                # check for clicks on reset button
                if game_board.reset_button_rect.collidepoint((x, y)):
                    game_board.create_hex_board()
                draw_screen(WINDOW, game_board)
        pygame.display.update()
        clock.tick(FRAMES)
    pygame.quit()
if __name__ == "__main__":
    main()