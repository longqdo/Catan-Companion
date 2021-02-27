import pygame
from hexa import Hexa
from loc import Loc
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, TAN, WHEAT
import math

color = 10

class Board:
    def __init__(self):
        self.hex_board = [[None, Hexa(), Hexa(), Hexa(), None], [Hexa(), Hexa(), Hexa(), Hexa(), None], [Hexa(), Hexa(), Hexa(), Hexa(), Hexa()], [Hexa(), Hexa(), Hexa(), Hexa(), None], [None, Hexa(), Hexa(), Hexa(), None]]
        self.loc_board = [[0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0]]
        self.selected_tile = None
        self.chosen_terrain = None
        self.hex_buttons = [[Hexa(), Hexa(), Hexa()], [Hexa(), Hexa(), Hexa()]]
        self.reset_button_surf = None
        self.reset_button_rect = None
        self.calc_button_surf = None
        self.calc_button_rect = None
        self.select_nums = [Hexa(), Hexa(), Hexa(), Hexa(), Hexa(), Hexa(), Hexa(), Hexa(), Hexa(), Hexa(), Hexa(), Hexa()]
        #self.create_loc_board()
        self.create_hex_board()
        self.create_drawer()
        


    def loc_loop_helper(self, i, j, verts, window):
        i_arr = [-1, 0, 1, 2]
        j_arr = [-1, 0, 1]
        # empty_loc = pygame.image.load('assets/empty_loc.png').convert_alpha()
        # empty_loc = pygame.transform.scale(blank, (4, 4)
        good_points = set(((0,1), (1,0), (2,0), (3,1), (1, 2), (2,2)))
        counter = 0
        for i_coord, i_num in enumerate(i_arr):
            for j_coord, j_num in enumerate(j_arr):
                if (i_coord, j_coord) not in good_points:
                    continue
                row = int(2 * i + i_num)
                col = int(2 * j + j_num)
                #print(row, col)
                # maybe I should just choose one for row and row - 1
                loc = Loc(row, col, verts[counter], None, None)
                pygame.draw.circle(window, (0, 255, 0), verts[counter], 6)
                self.loc_board[row-1][col-1] = loc
                counter+=1


    # draw's all possible settlement locations on board
    def create_loc_board(self, WINDOW):
        # hexa side length from WINDOW_WIDTH
        side = (WINDOW_WIDTH * 8/10) / (5 * 2 * math.cos(math.pi/6))

        # x,y distance between hexa's
        sep_x = 2 * side * math.cos(math.pi/6)
        sep_y = side * (1 + math.sin(math.pi/6))

        # initial x,y coordinates 
        curr_x = ((1/10) * WINDOW_WIDTH) + sep_x/2
        curr_y = ((1.5/10) * WINDOW_HEIGHT) + sep_y/3
        pygame.draw.circle(WINDOW, (255, 0 , 0), (curr_x, curr_y), 10)

        for i in range(len(self.hex_board)):
            if (i == 0 or i == 4):
                curr_x += side * math.cos(math.pi/6)
            elif (i == 2):
                curr_x -= side * math.cos(math.pi/6)
            for j in range(len(self.hex_board[i])):
                if self.hex_board[i][j] == None:
                    continue
                if i == 1 or i == 3:
                    new_j = j+.5
                else:
                    new_j = j
                vert1 = (curr_x , curr_y)
                vert2 = (curr_x + side * math.cos(math.pi/6), curr_y + side * math.sin(math.pi/6))
                vert3 = (curr_x + 2 * side * math.cos(math.pi/6), curr_y)
                vert4 = (curr_x + 2 * side * math.cos(math.pi/6), (curr_y - side))
                vert5 = (curr_x + side * math.cos(math.pi/6), curr_y + (side * math.sin(math.pi/6)) - (2 * side))
                vert6 = (curr_x , curr_y - side)
                verts = [vert5, vert6, vert4, vert1, vert3, vert2]
                self.loc_loop_helper(i+1, new_j+1, verts, WINDOW)
                curr_x += sep_x
            curr_x = ((1/10) * WINDOW_WIDTH) + sep_x/2
            curr_y += sep_y



    # initializes Hexa's and calculates correct coordinates
    # also used to reset board
    def create_hex_board(self):
        # hexa side length from WINDOW_WIDTH
        side = (WINDOW_WIDTH * 8/10) / (5 * 2 * math.cos(math.pi/6))

        # x,y distance between hexa's
        sep_x = 2 * side * math.cos(math.pi/6)
        sep_y = side * (1 + math.sin(math.pi/6)) 

        # initial x,y coordinates 
        curr_x = ((1/10) * WINDOW_WIDTH) + sep_x/2
        curr_y = ((1.5/10) * WINDOW_HEIGHT) + sep_y/3
        # load blank tile
        blank = pygame.image.load('assets/blank.png').convert_alpha()
        # loop through each hex in hexboard and initializes hexa's to blank
        for i in range(len(self.hex_board)):
            # offset 1 on first and last row
            if (i == 0 or i == 4):
                curr_x += side * math.cos(math.pi/6)
            # offset -1 on third row
            elif (i == 2):
                curr_x -= side * math.cos(math.pi/6)
            for j in range(len(self.hex_board[i])):
                if self.hex_board[i][j] == None:
                    continue
                self.hex_board[i][j].image = pygame.transform.scale(blank, (int(sep_x)-1, int(side * (1 + 2 * math.sin(math.pi/6)))-1))
                self.hex_board[i][j].rect = self.hex_board[i][j].image.get_rect(center = (curr_x+.5*sep_x, curr_y-sep_y/3))
                self.hex_board[i][j].mask = pygame.mask.from_surface(self.hex_board[i][j].image) 
                self.hex_board[i][j].row = i
                self.hex_board[i][j].col = j
                self.hex_board[i][j].center = (curr_x+.5*sep_x, curr_y-sep_y/3)
                self.hex_board[i][j].scale = (int(sep_x), int(side * (1 + 2 * math.sin(math.pi/6))))
                curr_x += sep_x
            # reset x to beginning
            curr_x = ((1/10) * WINDOW_WIDTH) + sep_x/2
            # hacky display fix
            curr_y += sep_y

        
          
    # draw's hexboard and outlines selected tile
    def draw_hex_board(self, window):

        # hexa side length from WINDOW_WIDTH
        side = (WINDOW_WIDTH * 8/10) / (5 * 2 * math.cos(math.pi/6))
        # how many pixels to make highlight ring smaller than hex
        highlight_decr = 8

        # x,y distance between hexa's
        sep_x = 2 * side * math.cos(math.pi/6)
        sep_y = side * (1 + math.sin(math.pi/6))

        # initial x,y coordinates 
        curr_x = ((1/10) * WINDOW_WIDTH) + sep_x/2
        curr_y = ((1.5/10) * WINDOW_HEIGHT) + sep_y/3
        
        # loops through each hex in hex_board and draws it
        for i in range(len(self.hex_board)):
            # offset 1 on first and last row
            if (i == 0 or i == 4):
                curr_x += side * math.cos(math.pi/6)
            # offset -1 on third row
            elif (i == 2):
                curr_x -= side * math.cos(math.pi/6)
            for j in range(len(self.hex_board[i])):
                curr_hex = self.hex_board[i][j]
                if curr_hex == None:
                    continue
                # draw current hexa
                window.blit(curr_hex.image, curr_hex.rect)
                # if curr hexa is selected, draw red outline
                if (self.selected_tile == curr_hex):
                    vert1 = (curr_x + (highlight_decr/2 * math.sqrt(3)), curr_y - highlight_decr/2)
                    vert2 = (curr_x + side * math.cos(math.pi/6), curr_y + side * math.sin(math.pi/6) - highlight_decr)
                    vert3 = (curr_x + 2 * side * math.cos(math.pi/6) - (highlight_decr/2 * math.sqrt(3)), curr_y - highlight_decr/2)
                    vert4 = (curr_x + 2 * side * math.cos(math.pi/6) - (highlight_decr/2 * math.sqrt(3)), (curr_y - side) + highlight_decr/2)
                    vert5 = (curr_x + side * math.cos(math.pi/6), curr_y + (side * math.sin(math.pi/6)) - (2 * side) + highlight_decr)
                    vert6 = (curr_x + (highlight_decr/2 * math.sqrt(3)), curr_y - side + highlight_decr/2)
                    color = pygame.Color(222, 30, 30)
                    pygame.draw.polygon(window, color, [vert1,vert2, vert3, vert4, vert5, vert6], 4)

                if (curr_hex.value):
                    window.blit(curr_hex.tile_num_image, (curr_hex.center[0]-18, curr_hex.center[1]-15))
                curr_x += sep_x
            # reset x to beginning
            curr_x = ((1/10) * WINDOW_WIDTH) + sep_x/2
            curr_y += sep_y

    def draw_loc_board(self, window):
        for row in self.loc_board:
            for loc in row:
                if loc == 0:
                    continue
                if loc.taken:
                    color = pygame.Color(255, 98, 64)
                else:
                    color = pygame.Color(180, 180, 180)
                rect = pygame.draw.circle(window, color, loc.coord, 5) 
                loc.rect = rect
    

    def create_drawer(self):
        tile_dict = {
            0 : 'assets/bricks.png',
            1 : 'assets/forest.png',
            2 : 'assets/wheat.png',
            3 : 'assets/rocks.png',
            4 : 'assets/pasture.png',
            5 : 'assets/desert.png'
        }
        resource_dict = {
            0 : 'bricks',
            1 : 'forest',
            2 : 'wheat',
            3 : 'rocks',
            4 : 'pasture',
            5 : 'desert'
        }

        side = .081 * WINDOW_WIDTH
        curr_x = .15 * WINDOW_WIDTH
        curr_y = .86 * WINDOW_HEIGHT

        sep_x = 2 * side * math.cos(math.pi/6)
        sep_y = side * (1 + math.sin(math.pi/6))

        # load and scale reset button
        reset_button = pygame.image.load('assets/reset_button.png').convert_alpha()
        reset_button = pygame.transform.scale(reset_button, (50, 30))
        self.reset_button_surf = reset_button
        self.reset_button_rect = reset_button.get_rect(center = (.72 * WINDOW_WIDTH, .96 * WINDOW_HEIGHT))

        # load and scale calc button
        calc_button = pygame.image.load('assets/calc_button.png').convert_alpha()
        calc_button = pygame.transform.scale(calc_button, (50, 30))
        self.calc_button_surf = calc_button
        self.calc_button_rect = calc_button.get_rect(center = (.81 * WINDOW_WIDTH, .96 * WINDOW_HEIGHT))

        # loops through terrain buttons and loads and draws them (functionality maybe should be split up into two functions)
        for i in range(2):
            if i == 1:
                curr_x += side * math.cos(math.pi/6)
            for j in range(3):
                blank = pygame.image.load(tile_dict[i*3+j]).convert_alpha()
                self.hex_buttons[i][j].image = pygame.transform.scale(blank, (int(sep_x), int(side * (1 + 2 * math.sin(math.pi/6)))))
                self.hex_buttons[i][j].rect = self.hex_buttons[i][j].image.get_rect(center = (curr_x+.5*sep_x, curr_y-sep_y/3))
                self.hex_buttons[i][j].mask = pygame.mask.from_surface(self.hex_buttons[i][j].image) 
                self.hex_buttons[i][j].resource = resource_dict[i*3+j]
                self.hex_buttons[i][j].center = (curr_x+.5*sep_x, curr_y-sep_y/3)
                self.hex_buttons[i][j].scale = (int(sep_x), int(side * (1 + 2 * math.sin(math.pi/6))))
                curr_x += sep_x
            curr_x = .15 * WINDOW_WIDTH
            curr_y += sep_y

        curr_x = .715 * WINDOW_WIDTH
        curr_y = .795 * WINDOW_HEIGHT
        # inits select number buttons
        for i in range(4):
            for j in range(3):
                # skip number one
                if ((3*i)+j) != 0:
                    num = pygame.image.load('assets/select_numbers/' + str(((3*i)+j) + 1) + '.png').convert_alpha()
                    self.select_nums[((3*i)+j)].image = pygame.transform.scale(num, (30,30))
                    self.select_nums[((3*i)+j)].rect = self.select_nums[((3*i)+j)].image.get_rect(center = (curr_x, curr_y))
                    self.select_nums[((3*i)+j)].value = ((3*i)+j) + 1
                curr_x += 31
            curr_x = .715 * WINDOW_WIDTH
            curr_y += 31

            
                

    # draws bottom drawer and tiles inside it
    def draw_drawer(self, window):

        # draws the drawer
        drawer = pygame.image.load('assets/drawer.png').convert_alpha()
        drawer = pygame.transform.scale(drawer, (int(.8 * WINDOW_WIDTH)-1, int(.25 * WINDOW_HEIGHT)-1))
        drawer_rect = drawer.get_rect(center = (.5 * WINDOW_WIDTH, .8725 * WINDOW_HEIGHT))
        window.blit(drawer, drawer_rect)

        # draw number tiles on board
        for i in range(1, 12):
            window.blit(self.select_nums[i].image, self.select_nums[i].rect)
        
        # draw reset button
        window.blit(self.reset_button_surf, self.reset_button_rect)

        # draw calc button
        window.blit(self.calc_button_surf, self.calc_button_rect)

        # loops through terrain buttons and loads and draws them (functionality maybe should be split up into two functions)
        for i in range(2):
            for j in range(3):
                window.blit(self.hex_buttons[i][j].image, self.hex_buttons[i][j].rect)



        