from random import randint
import pygame
import logging

logging.basicConfig(filename='snake-log', level=logging.INFO,
                    format='%(levelname)s:%(message)s')


class snake:
    def __init__(self):
        self.velocity = 25
        self.blocks = [block(250, 500, (0, 200, 0))]
        # fx(forward in x axis),bx(backward in x axis), fy,by
        self.moving_direction = 'fx'
        logging.info('SNAKE INITIALIZED')

    def print_snake(self, win):
        for i in enumerate(self.blocks):
            coor = i[1].get_position()
            color = i[1].get_color()
            pygame.draw.rect(
                win, color, (coor[0], coor[1], 20, 20))
            logging.info(str(i[0]) + str(coor))

    def turn(self):
        keys = pygame.key.get_pressed()

        if self.moving_direction == 'fx' or self.moving_direction == 'bx':
            if keys[pygame.K_UP]:
                self.moving_direction = 'by'
            elif keys[pygame.K_DOWN]:
                self.moving_direction = 'fy'

        if self.moving_direction == 'fy' or self.moving_direction == 'by':
            if keys[pygame.K_LEFT]:
                self.moving_direction = 'bx'
            elif keys[pygame.K_RIGHT]:
                self.moving_direction = 'fx'
        logging.info('MOVING DIRECTION: '+str(self.moving_direction))

    def move(self):
        prev_pos = self.blocks[0].get_position()
        # moves snake forward if already moving forward
        if self.moving_direction == 'fx':
            self.blocks[0].x_coor = self.blocks[0].x_coor+self.velocity

        # moves snake backward of already moving backward
        elif self.moving_direction == 'bx':
            self.blocks[0].x_coor = self.blocks[0].x_coor-self.velocity

        # moves snake downward if already moving downward
        elif self.moving_direction == 'fy':
            self.blocks[0].y_coor = self.blocks[0].y_coor+self.velocity

        # moves snake upward if already moving upward
        else:
            self.blocks[0].y_coor = self.blocks[0].y_coor-self.velocity

        for i in range(1, len(self.blocks)):
            current_pos = self.blocks[i].get_position()
            self.blocks[i].set_position(prev_pos[0], prev_pos[1])
            prev_pos = current_pos

    def grow(self):
        color = (0, 255, 0)
        coor = self.blocks[len(self.blocks)-1].get_position()
        x_coor = coor[0]
        y_coor = coor[1]
        if self.moving_direction == 'fx':
            x_coor -= 35
        elif self.moving_direction == 'bx':
            x_coor += 35
        elif self.moving_direction == 'fy':
            y_coor -= 35
        else:
            y_coor += 35
        b = block(x_coor, y_coor, color)
        self.blocks.append(b)

    def eat(self, food_at):
        coor = self.blocks[0].get_position()
        if food_at[0]-30 <= coor[0] <= food_at[0]+30 and food_at[1]-30 <= coor[1] <= food_at[1]+30:
            return True
        return False

    # checks if snake collided with wall
    def wall_collision(self):
        coor = self.blocks[0].get_position()
        if coor[0] > 957 or coor[0] < 15 or coor[1] > 957 or coor[1] < 15:
            logging.info('WALL COLLIDE')
            return True
        return False

    # checks if snake collided with itself
    def self_collision(self):
        head_pos = self.blocks[0].get_position()
        head_x = head_pos[0]
        head_y = head_pos[1]
        for i in range(1, len(self.blocks)):
            block_pos = self.blocks[i].get_position()
            block_x = block_pos[0]
            block_y = block_pos[1]

            if head_x == block_x and head_y == block_y:
                logging.info('SELF COLLIDE')
                return True
        return False
    # prints speed

    def print_speed(self, win, font, ping):
        if ping == 80:
            speed = 1
        elif ping == 60:
            speed = 1.5
        elif ping == 40:
            speed = 2
        else:
            speed = 4
        text = font.render('Speed: '+str(speed)+'x', 1, (0, 0, 0))
        win.blit(text, (50, 50))


'''
class block containing information about each snake's block
'''


class block:
    def __init__(self, x, y, color):
        self.x_coor = x
        self.y_coor = y
        self.color = color
        logging.info('BLOCK INITIALIZED')

    def get_position(self):
        return [self.x_coor, self.y_coor]

    def set_position(self, x, y):
        self.x_coor, self.y_coor = x, y

    def get_color(self):
        return self.color


class food:
    def __init__(self):
        self.color = (200, 0, 200)
        self.length = 30
        self.bredth = 30
        self.x_coor = randint(20, 955)
        self.y_coor = randint(20, 955)
        logging.info('FOOD INITIALIZED')

    def get_position(self):
        return (self.x_coor, self.y_coor)

    def print_food(self, win):
        pygame.draw.rect(win, self.color,
                         (self.x_coor, self.y_coor, self.length, self.bredth))


class board:
    def __init__(self):
        self.length = 1000
        self.bredth = 1000
        self.background_color = (255, 255, 255)
        logging.info('BOARD INITIALIZED')

    def initialize(self):
        win = pygame.display.set_mode((self.length, self.bredth))
        win.fill(self.background_color)
        pygame.display.set_caption('Snake')
        return win

    # creates a wall boundry around the snake
    def boundry(self, win):
        pygame.draw.line(win, (0, 0, 0), (0, 0), (1000, 0), 30)
        pygame.draw.line(win, (0, 0, 0), (1000, 0), (1000, 1000), 30)
        pygame.draw.line(win, (0, 0, 0), (1000, 1000), (0, 1000), 30)
        pygame.draw.line(win, (0, 0, 0), (0, 1000), (0, 0), 30)

    def exit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

    def wait_for_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_DOWN] or keys[pygame.K_RIGHT] or keys[pygame.K_RIGHT]:
            return True
        return False


class score:
    def __init__(self):
        self.score = 0
        logging.info('SCORE INITIALIZED')

    def inc_score(self):
        self.score += 1

    def get_score(self):
        return self.score

    def print_score(self, win, font):
        text = font.render('Score : '+str(self.score), 1, (0, 0, 0))
        win.blit(text, (850, 50))


def set_ping(score):
    if score <= 3:
        return 80
    elif score <= 6:
        return 60
    elif score <= 12:
        return 40
    else:
        return 20


def print_all(win, font, snake, board, score, food, ping):
    win.fill((255, 255, 255))
    board.boundry(win)
    snake.print_snake(win)
    food.print_food(win)
    score.print_score(win, font)
    snake.print_speed(win, font, ping)
    pygame.display.update()


def main():
    pygame.init()
    logging.info('#'*20)
    logging.info('SCRIPT RUN')

    '''
    Snake Game Main Loop
    '''
    font = pygame.font.SysFont('comicsans', 30, True)
    b = board()
    win = b.initialize()
    run = 0
    Snake = True
    while Snake:
        run += 1
        logging.info('RUN : '+str(run))
        s = snake()
        scr = score()
        is_food = False
        wait = True
        '''
        Play Game Loop
        '''
        while True:
            ping = set_ping(scr.get_score())
            pygame.time.delay(ping)

            if b.wait_for_input():
                wait = False
            if b.exit():
                logging.info('GAME EXIT')
                pygame.quit()
                Snake = False
                break
            if is_food == False:
                f = food()
                is_food = True
            if s.eat(f.get_position()) == True:
                s.grow()
                scr.inc_score()
                is_food = False
            s.turn()
            if not wait:
                s.move()
            if s.wall_collision() or s.self_collision():
                logging.info('GAME ENDED')
                break

            print_all(win, font, s, b, scr, f, ping)


main()
