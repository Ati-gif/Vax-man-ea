import pygame
import time
import random


# TheForage Module 1



# completed:
# Vax-Man can kill a ghost if he comes into contact with it (vaccinates it).
# Contact with a ghost does not kill Vax-Man.
# The goal of the game is to collect all the dots before the number of ghosts grows to 32 times the original number.
#   original number = 4; goal is while num_ghosts < 128
# Each ghost that has not yet been hit multiplies itself every 30 seconds (the infection grows).
# Duplicated ghosts have to be able to move



black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)
purple = (255, 0, 255)
yellow = (255, 255, 0)

count = 4

# keep track of size of monsta_list
# if size >= 128 then game over

Vaxman = pygame.image.load('images/baymax.png')
pygame.display.set_icon(Vaxman)

# Add music
# pygame.mixer.init()
# pygame.mixer.music.load('pacman.mp3')
# pygame.mixer.music.play(-1, 0.0)

# This class represents the bar at the bottom that the player controls


class Wall(pygame.sprite.Sprite):
    # Constructor function
    def __init__(self, x, y, width, height, color):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        # Make a blue wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x

# This creates all the walls in room 1


def setupRoomOne(all_sprites_list):
    # Make the walls. (x_pos, y_pos, width, height)
    wall_list = pygame.sprite.RenderPlain()

    # This is a list of walls. Each is in the form [x, y, width, height]
    walls = [[0, 0, 6, 600],
             [0, 0, 600, 6],
             [0, 600, 606, 6],
             [600, 0, 6, 606],
             [300, 0, 6, 66],
             [60, 60, 186, 6],
             [360, 60, 186, 6],
             [60, 120, 66, 6],
             [60, 120, 6, 126],
             [180, 120, 246, 6],
             [300, 120, 6, 66],
             [480, 120, 66, 6],
             [540, 120, 6, 126],
             [120, 180, 126, 6],
             [120, 180, 6, 126],
             [360, 180, 126, 6],
             [480, 180, 6, 126],
             [180, 240, 6, 126],
             [180, 360, 246, 6],
             [420, 240, 6, 126],
             [240, 240, 42, 6],
             [324, 240, 42, 6],
             [240, 240, 6, 66],
             [240, 300, 126, 6],
             [360, 240, 6, 66],
             [0, 300, 66, 6],
             [540, 300, 66, 6],
             [60, 360, 66, 6],
             [60, 360, 6, 186],
             [480, 360, 66, 6],
             [540, 360, 6, 186],
             [120, 420, 366, 6],
             [120, 420, 6, 66],
             [480, 420, 6, 66],
             [180, 480, 246, 6],
             [300, 480, 6, 66],
             [120, 540, 126, 6],
             [360, 540, 126, 6]
             ]

    # Loop through the list. Create the wall, add it to the list
    for item in walls:
        wall = Wall(item[0], item[1], item[2], item[3], blue)
        wall_list.add(wall)
        all_sprites_list.add(wall)

    # return our new list
    return wall_list


def setupGate(all_sprites_list):
    gate = pygame.sprite.RenderPlain()
    gate.add(Wall(282, 242, 42, 2, white))
    all_sprites_list.add(gate)
    return gate

# This class represents the ball
# It derives from the "Sprite" class in Pygame


class Block(pygame.sprite.Sprite):

    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill(white)
        self.image.set_colorkey(white)
        pygame.draw.ellipse(self.image, color, [0, 0, width, height])

        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()

# This class represents the bar at the bottom that the player controls


class Player(pygame.sprite.Sprite):

    # Set speed vector
    change_x = 0
    change_y = 0

    # Constructor function
    def __init__(self, x, y, filename):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        # Set height, width
        self.image = pygame.image.load(filename).convert()

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x
        self.prev_x = x
        self.prev_y = y

    # def getX(self):
    #     return self.prev_x
    # def getY(self):
    #     return self.prev_y
    # Clear the speed of the player
    def prevdirection(self):
        self.prev_x = self.change_x
        self.prev_y = self.change_y

    # Change the speed of the player
    def changespeed(self, x, y):
        self.change_x += x
        self.change_y += y

    # Find a new position for the player
    def update(self, walls, gate):
        # Get the old position, in case we need to go back to it

        old_x = self.rect.left
        new_x = old_x + self.change_x
        prev_x = old_x + self.prev_x
        self.rect.left = new_x

        old_y = self.rect.top
        new_y = old_y+self.change_y
        prev_y = old_y+self.prev_y

        # Did this update cause us to hit a wall?
        x_collide = pygame.sprite.spritecollide(self, walls, False)
        if x_collide:
            # Whoops, hit a wall. Go back to the old position
            self.rect.left = old_x
            # self.rect.top=prev_y
            # y_collide = pygame.sprite.spritecollide(self, walls, False)
            # if y_collide:
            #     # Whoops, hit a wall. Go back to the old position
            #     self.rect.top=old_y
            #     print('a')
        else:

            self.rect.top = new_y

            # Did this update cause us to hit a wall?
            y_collide = pygame.sprite.spritecollide(self, walls, False)
            if y_collide:
                # Whoops, hit a wall. Go back to the old position
                self.rect.top = old_y
                # self.rect.left=prev_x
                # x_collide = pygame.sprite.spritecollide(self, walls, False)
                # if x_collide:
                #     # Whoops, hit a wall. Go back to the old position
                #     self.rect.left=old_x
                #     print('b')

        if gate != False:
            gate_hit = pygame.sprite.spritecollide(self, gate, False)
            if gate_hit:
                self.rect.left = old_x
                self.rect.top = old_y

# Inheritime Player klassist


class Ghost(Player):
    # Change the speed of the ghost
    def changespeed(self, list, ghost, turn, steps, l):
        try:
            z = list[turn][2]
            if steps < z:
                self.change_x = list[turn][0]
                self.change_y = list[turn][1]
                steps += 1
            else:
                if turn < l:
                    turn += 1
                elif ghost == "O":
                    turn = 2
                else:
                    turn = 0
                self.change_x = list[turn][0]
                self.change_y = list[turn][1]
                steps = 0
            return [turn, steps]
        except IndexError:
            return [0, 0]


P_directions = [
    [0, -30, 4],
    [15, 0, 9],
    [0, 15, 11],
    [-15, 0, 23],
    [0, 15, 7],
    [15, 0, 3],
    [0, -15, 3],
    [15, 0, 19],
    [0, 15, 3],
    [15, 0, 3],
    [0, 15, 3],
    [15, 0, 3],
    [0, -15, 15],
    [-15, 0, 7],
    [0, 15, 3],
    [-15, 0, 19],
    [0, -15, 11],
    [15, 0, 9]
]

R_directions = [
    [0, -15, 4],
    [15, 0, 9],
    [0, 15, 11],
    [15, 0, 3],
    [0, 15, 7],
    [-15, 0, 11],
    [0, 15, 3],
    [15, 0, 15],
    [0, -15, 15],
    [15, 0, 3],
    [0, -15, 11],
    [-15, 0, 3],
    [0, -15, 11],
    [-15, 0, 3],
    [0, -15, 3],
    [-15, 0, 7],
    [0, -15, 3],
    [15, 0, 15],
    [0, 15, 15],
    [-15, 0, 3],
    [0, 15, 3],
    [-15, 0, 3],
    [0, -15, 7],
    [-15, 0, 3],
    [0, 15, 7],
    [-15, 0, 11],
    [0, -15, 7],
    [15, 0, 5]
]

B_directions = [
    [30, 0, 2],
    [0, -15, 4],
    [15, 0, 10],
    [0, 15, 7],
    [15, 0, 3],
    [0, -15, 3],
    [15, 0, 3],
    [0, -15, 15],
    [-15, 0, 15],
    [0, 15, 3],
    [15, 0, 15],
    [0, 15, 11],
    [-15, 0, 3],
    [0, -15, 7],
    [-15, 0, 11],
    [0, 15, 3],
    [-15, 0, 11],
    [0, 15, 7],
    [-15, 0, 3],
    [0, -15, 3],
    [-15, 0, 3],
    [0, -15, 15],
    [15, 0, 15],
    [0, 15, 3],
    [-15, 0, 15],
    [0, 15, 11],
    [15, 0, 3],
    [0, -15, 11],
    [15, 0, 11],
    [0, 15, 3],
    [15, 0, 1],
]

O_directions = [
    [-30, 0, 2],
    [0, -15, 4],
    [15, 0, 5],
    [0, 15, 7],
    [-15, 0, 11],
    [0, -15, 7],
    [-15, 0, 3],
    [0, 15, 7],
    [-15, 0, 7],
    [0, 15, 15],
    [15, 0, 15],
    [0, -15, 3],
    [-15, 0, 11],
    [0, -15, 7],
    [15, 0, 3],
    [0, -15, 11],
    [15, 0, 9],
]

directions = [P_directions, R_directions,
              B_directions, O_directions]

pl = len(P_directions)-1
bl = len(R_directions)-1
il = len(B_directions)-1
cl = len(O_directions)-1


# Call this function so the Pygame library can initialize itself
pygame.init()

# Create an 606x606 sized screen
screen = pygame.display.set_mode([606, 606])

# This is a list of 'sprites.' Each block in the program is
# added to this list. The list is managed by a class called 'RenderPlain.'


# Set the title of the window
pygame.display.set_caption('Pacman')

# Create a surface we can draw on
background = pygame.Surface(screen.get_size())

# Used for converting color maps and such
background = background.convert()

# Fill the screen with a black background
background.fill(black)


clock = pygame.time.Clock()

pygame.font.init()
font = pygame.font.Font("emulogic.ttf", 24)

# default locations for Pacman and monstas
w = 303-16  # Width
i_w = 303-16-32  # Inky width
c_w = 303+(32-16)  # Clyde width

p_h = (7*60)+19  # Pacman height
m_h = (4*60)+19  # Monster height
b_h = (3*60)+19  # Binky height

pac_coord = (w, p_h)
blink_coord = (w, b_h)
pink_coord = (w, m_h)
inky_coord = (i_w, m_h)
clyd_coord = (c_w, m_h)

# spawnpoint_w = [w, i_w, c_w]
spawnpoint_w = [w, i_w, c_w]
spawnpoint_h = [m_h, b_h]


def startGame():
    all_sprites_list = pygame.sprite.RenderPlain()

    block_list = pygame.sprite.RenderPlain()

    monsta_list = pygame.sprite.RenderPlain()

    pacman_collide = pygame.sprite.RenderPlain()

    wall_list = setupRoomOne(all_sprites_list)

    gate = setupGate(all_sprites_list)

    p_turn = 0
    p_steps = 0

    b_turn = 0
    b_steps = 0

    i_turn = 0
    i_steps = 0

    c_turn = 0
    c_steps = 0

    g_turn = 0
    g_steps = 0
    # Create the player paddle object
    Pacman = Player(w, p_h, "images/pac-man.png")
    all_sprites_list.add(Pacman)
    pacman_collide.add(Pacman)

    R = Ghost(w, b_h, "images/R.png")
    monsta_list.add(R)
    all_sprites_list.add(R)

    # iterate through the monsta_list
    # for monsta in monsta_list:
    #   all_sprites_list.add(monsta)

    P = Ghost(w, m_h, "images/P.png")
    monsta_list.add(P)
    all_sprites_list.add(P)

    B = Ghost(i_w, m_h, "images/B.png")
    monsta_list.add(B)
    all_sprites_list.add(B)

    O = Ghost(c_w, m_h, "images/O.png")
    monsta_list.add(O)
    all_sprites_list.add(O)

    # Draw the grid
    for row in range(19):
        for column in range(19):
            if (row == 7 or row == 8) and (column == 8 or column == 9 or column == 10):
                continue
            else:
                block = Block(yellow, 4, 4)

                # Set a random location for the block
                block.rect.x = (30*column+6)+26
                block.rect.y = (30*row+6)+26

                b_collide = pygame.sprite.spritecollide(
                    block, wall_list, False)
                p_collide = pygame.sprite.spritecollide(
                    block, pacman_collide, False)
                if b_collide:
                    continue
                elif p_collide:
                    continue
                else:
                    # Add the block to the list of objects
                    block_list.add(block)
                    all_sprites_list.add(block)

    bll = len(block_list)

    score = 0

    done = False

    i = 0
    t0 = time.time()

    gen_arr = []
    dir_arr = []
    local_turn_steps = []
    while not done:
        # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT

        if len(monsta_list) >= 128:
            done = True
            doNext("Game Over", 235, all_sprites_list, block_list,
                   monsta_list, pacman_collide, wall_list, gate)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    Pacman.changespeed(-30, 0)
                if event.key == pygame.K_RIGHT:
                    Pacman.changespeed(30, 0)
                if event.key == pygame.K_UP:
                    Pacman.changespeed(0, -30)
                if event.key == pygame.K_DOWN:
                    Pacman.changespeed(0, 30)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    Pacman.changespeed(30, 0)
                if event.key == pygame.K_RIGHT:
                    Pacman.changespeed(-30, 0)
                if event.key == pygame.K_UP:
                    Pacman.changespeed(0, 30)
                if event.key == pygame.K_DOWN:
                    Pacman.changespeed(0, -30)

        # ALL EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT

        # ALL GAME LOGIC SHOULD GO BELOW THIS COMMENT
        Pacman.update(wall_list, gate)

        returned = P.changespeed(
            P_directions, False, p_turn, p_steps, pl)
        p_turn = returned[0]
        p_steps = returned[1]
        P.changespeed(P_directions, False, p_turn, p_steps, pl)
        P.update(wall_list, False)

        returned = R.changespeed(
            R_directions, False, b_turn, b_steps, bl)
        b_turn = returned[0]
        b_steps = returned[1]
        R.changespeed(R_directions, False, b_turn, b_steps, bl)
        R.update(wall_list, False)

        returned = B.changespeed(
            B_directions, False, i_turn, i_steps, il)
        i_turn = returned[0]
        i_steps = returned[1]
        B.changespeed(B_directions, False, i_turn, i_steps, il)
        B.update(wall_list, False)

        returned = O.changespeed(
            O_directions, "O", c_turn, c_steps, cl)
        c_turn = returned[0]
        c_steps = returned[1]
        O.changespeed(O_directions, "O", c_turn, c_steps, cl)
        O.update(wall_list, False)

        # See if the Pacman block has collided with anything.
        blocks_hit_list = pygame.sprite.spritecollide(Pacman, block_list, True)

        # Check the list of collisions.
        if len(blocks_hit_list) > 0:
            score += len(blocks_hit_list)

        # ALL GAME LOGIC SHOULD GO ABOVE THIS COMMENT

        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        screen.fill(black)

        wall_list.draw(screen)
        gate.draw(screen)
        all_sprites_list.draw(screen)  # just draw pacman
        monsta_list.draw(screen)

        text = font.render("Score: "+str(score)+"/"+str(bll), True, white)
        screen.blit(text, [10, 10])

        text = font.render("Ghosts: "+str(len(monsta_list)), True, white)
        screen.blit(text, [10, 35])

        t1 = time.time()  # https://stackoverflow.com/questions/20023709/resetting-pygames-timer
        dt = t1 - t0
        dupe_time = 2
        if dt >= dupe_time:
            print(dupe_time, "seconds reached")
            t0 = t1  # when this is called, timer goes back to "0"

            for monsta in monsta_list:
                # creating generic ghost

                # R_coord = (w, b_h)
                # P_coord = (w, m_h)
                # B_coord = (i_w, m_h)
                # O_coord = (c_w, m_h)

                # spawnpoint_w = [w, i_w, c_w]
                # spawnpoint_h = [m_h, b_h]

                g_spawn_w = random.choice(spawnpoint_w)
                if g_spawn_w == w:
                    g_spawn_h = random.choice(spawnpoint_h)
                else:
                    g_spawn_h = m_h

                G = Ghost(g_spawn_w, g_spawn_h,
                                "images/G.png")
                monsta_list.add(G)
                all_sprites_list.add(G)


                if g_spawn_w == w and g_spawn_h == m_h:  # P
                    g_directions = P_directions.copy()  # setting variable equal to array
                    # print("w, m_h", g_directions == P_directions)
                elif g_spawn_w == w and g_spawn_h == b_h:
                    g_directions = R_directions.copy()
                    # print("w, b_h", g_directions == R_directions)
                elif g_spawn_w == i_w:
                    g_directions = B_directions.copy()
                    # print("i_w", g_directions == B_directions)
                else:
                    g_directions = O_directions.copy()
                    pass
                    # print("c_w", g_directions == O_directions)

                gen_arr.append(G)             # [Ghost1, Ghost2]
                dir_arr.append(g_directions)  # [Direction1, Direction2]
                local_turn_steps.append([0, 0])

        else:
            pass

        for i in range(len(gen_arr) - 1):
            G = gen_arr[i]
            g_directions = dir_arr[i]

            g_turn = local_turn_steps[i][0]
            g_steps = local_turn_steps[i][1]

            gl = len(g_directions) - 1

            try:
                returned = G.changespeed(
                    g_directions, False, g_turn, g_steps, gl)
                local_turn_steps[i][0] = returned[0]
                local_turn_steps[i][1] = returned[1]
                g_turn = local_turn_steps[i][0]
                g_steps = local_turn_steps[i][1]
                G.changespeed(g_directions,
                                    False, g_turn, g_steps, gl)
                G.update(wall_list, False)
            except:
                print("except")
                returned = G.changespeed(
                    g_directions, "O", g_turn, g_steps, gl)
                local_turn_steps[i][0] = returned[0]
                local_turn_steps[i][1] = returned[1]
                g_turn = local_turn_steps[i][0]
                g_steps = local_turn_steps[i][1]
                G.changespeed(g_directions,
                                    "O", g_turn, g_steps, gl)
                G.update(wall_list, False)

        text = font.render("Duplicating in: " + str(round(dt, 2)), True, red)
        screen.blit(text, [200, 10])

        monsta_hit_list = pygame.sprite.spritecollide(
            Pacman, monsta_list, True)  # changing to true enables dokill

        if monsta_hit_list:

            print("Ghost Killed")

        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

        pygame.display.flip()

        if len(monsta_list) == 0:
            try:
                for t in monsta_list:
                    t.kill()
            except:
                pass
            doNext("Congratulations, you won!", 145, all_sprites_list,
                   block_list, monsta_list, pacman_collide, wall_list, gate)
            done = True
        clock.tick(10)


def doNext(message, left, all_sprites_list, block_list, monsta_list, pacman_collide, wall_list, gate):
    while True:
        # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                if event.key == pygame.K_RETURN:
                    del all_sprites_list
                    del block_list
                    del monsta_list
                    del pacman_collide
                    del wall_list
                    del gate
                    startGame()

        # Grey background
        w = pygame.Surface((400, 200))  # the size of your rect
        w.set_alpha(10)                # alpha level
        w.fill((128, 128, 128))           # this fills the entire surface
        screen.blit(w, (100, 200))    # (0,0) are the top-left coordinates

        # Won or lost
        text1 = font.render(message, True, white)
        screen.blit(text1, [left, 233])

        text2 = font.render("To play again, press ENTER.", True, white)
        screen.blit(text2, [135, 303])
        text3 = font.render("To quit, press ESCAPE.", True, white)
        screen.blit(text3, [165, 333])

        pygame.display.flip()

        clock.tick(1000)


startGame()

pygame.quit()
