"""
Snake Eater
Made with PyGame

https://gist.github.com/rajatdiptabiswas/bd0aaa46e975a4da5d090b801aba0611
"""

import pygame, sys, time, random


# Difficulty settings
# Easy      ->  10
# Medium    ->  25
# Hard      ->  40
# Harder    ->  60
# Impossible->  120
difficulty = 40

# Window size
frame_size_x = 720
frame_size_y = 480

# Checks for errors encountered
check_errors = pygame.init()
# pygame.init() example output -> (6, 0)
# second number in tuple gives number of errors
if check_errors[1] > 0:
    print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
    sys.exit(-1)
else:
    print('[+] Game successfully initialised')


# Initialise game window
pygame.display.set_caption('Snake Eater')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))


# Colors (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)


# FPS (frames per second) controller
fps_controller = pygame.time.Clock()


# Game variables
snake_pos = [100, 50]
snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]

food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
food_spawn = True

direction = 'RIGHT'
change_to = direction

score = 0


# Game Over
def game_over():
    my_font = pygame.font.SysFont('times new roman', 90)
    game_over_surface = my_font.render('YOU DIED', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (frame_size_x/2, frame_size_y/4)
    game_window.fill(black)
    game_window.blit(game_over_surface, game_over_rect)
    show_score(0, red, 'times', 20)
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit()


# Score
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (frame_size_x/10, 15)
    else:
        score_rect.midtop = (frame_size_x/2, frame_size_y/1.25)
    game_window.blit(score_surface, score_rect)
    # pygame.display.flip()


def food_on_snake():
    global snake_pos
    global snake_body
    global food_pos
    for i in snake_body:
        if food_pos[0] == i[0] and food_pos[1] == i[1]:
            return True
    return False


def check_snake():
    global snake_pos
    global snake_body
    unavailable = [] 
    for i in snake_body[1:]:
        if snake_pos[1] - i[1] == 10 and snake_pos[0] == i[0]:
            if "UP" not in unavailable:
                unavailable.append("UP")
        if snake_pos[1] - i[1] == -10 and snake_pos[0] == i[0]:
            if "DOWN" not in unavailable:
                unavailable.append("DOWN")
        if snake_pos[0] - i[0] == 10 and snake_pos[1] == i[1]:
            if "LEFT" not in unavailable:
                unavailable.append("LEFT")
        if snake_pos[0] - i[0] == -10 and snake_pos[1] == i[1]:
            if "RIGHT" not in unavailable:
                unavailable.append("RIGHT")
    return unavailable

'''
def checksnake_left_right():
    for i in snake_body[1:]:
        if i[1] == snake_pos[1]:
            return True
    else:
        return False
'''
def go_left_right():
    global change_to
    global direction    
    if snake_pos[0] < food_pos[0]:
        change_to  = 'RIGHT'
        if direction == 'LEFT':
            if snake_pos[1] < food_pos[1]:
                change_to = 'DOWN'
            else:
                change_to = 'UP'
    elif snake_pos[0] > food_pos[0]:
        change_to = 'LEFT'
        if direction == 'RIGHT':
            if snake_pos[1] < food_pos[1]:
                change_to = 'DOWN'
            else:
                change_to = 'UP'
    else:
        change_to = ""

    return change_to

def go_up_down():
    global change_to
    global direction
    
    if snake_pos[1] < food_pos[1]:
        #print(f"<<<<< {change_to}")
        change_to = 'DOWN'
        if direction == "UP":
            if snake_pos[0] > food_pos[0]:
                #print(f"LEFT1 {change_to}")
                change_to = "LEFT"
            else:
                #print(f"<<<<<11  {change_to}")
                change_to = "RIGHT"
    elif snake_pos[1] > food_pos[1]:
        #print(f">>>>>>>  {change_to}")
        change_to = 'UP'
        if direction == "DOWN":
            if snake_pos[0] > food_pos[0]:
                #print(f"LEFT2  {change_to}")
                change_to = "LEFT"
            else:
                #print(f"<<222< {change_to}")
                change_to = "RIGHT"
    else:
        change_to = ""
    #print(f"change_to is set {change_to}")

    return change_to

def get_opposite(direction):
    if (direction == "UP"):
        return "DOWN"
    elif (direction == "DOWN"):
        return "UP"
    elif (direction == "LEFT"):
        return "RIGHT"
    elif(direction == "RIGHT"):
        return "LEFT"
    else:
        return ""

def autoplay():
    global change_to
    global direction
    priority = [""]*2
    unavailable = check_snake()
    #print(f"autoplay direction={direction}, {snake_pos}, {food_pos} {change_to} --------UNAVAILABLE {unavailable} --------{snake_body}")
    if direction =="RIGHT":
        unavailable.append("LEFT")
    if direction =="LEFT":
        unavailable.append("RIGHT")
    if direction =="UP":
        unavailable.append("DOWN")
    if direction =="DOWN":
        unavailable.append("UP")
    
    if snake_pos[0] == 0:
        unavailable.append("LEFT")
    elif snake_pos[0] == frame_size_x-10:
        unavailable.append("RIGHT")
    if snake_pos[1] == 0:
        unavailable.append("UP")
    elif snake_pos[1] == frame_size_y-10:
        unavailable.append("DOWN")

    if food_pos[0] > snake_pos[0]:
        priority[0] = "RIGHT"
    elif food_pos[0] < snake_pos[0]:
        priority[0] = "LEFT"
    if food_pos[1] < snake_pos[1]:
        priority[1] = "UP"
    elif food_pos[1] > snake_pos[1]:
        priority[1] ="DOWN"
    #---- above we get the direction
    
    
    if priority[0]!= "" and priority[0] not in unavailable:
        change_to = priority[0]
        return change_to

    if priority[1]!= "" and priority[1] not in unavailable:
        change_to = priority[1]
        return change_to
    
    priority[0] = get_opposite(priority[0])
    if priority[0]!= "" and priority[0] not in unavailable:
        #if "LEFT" not in unavailable:
        #    change_to = "LEFT"
        change_to = priority[0]
        return change_to

    priority[1] = get_opposite(priority[1])    
    if priority[1]!= "" and priority[1] not in unavailable:
        change_to = priority[1]
        return change_to

    
    if "UP" not in unavailable:
        change_to = "UP"
    elif "DOWN" not in unavailable:
        change_to = "DOWN"
    elif "LEFT" not in unavailable:
        change_to = "LEFT"
    elif "RIGHT" not in unavailable:
        change_to = "RIGHT"
    else:
        change_to = ""
    print(f"we will change to {change_to}")
    return change_to



# Main logic
isAuto = False
while True:
    for event in pygame.event.get():
        print(f"$[{event.type}]  {event}")
        if event.type == pygame.USEREVENT:
            change_to = autoplay()
            isAuto = True
        elif event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Whenever a key is pressed down
        elif event.type == pygame.KEYDOWN:
            if event.key == ord('p'):
                change_to = autoplay()
                print(f"change_to = {change_to}")
                isAuto = True
            else:    
                # W -> Up; S -> Down; A -> Left; D -> Right
                if event.key == pygame.K_UP or event.key == ord('w'):
                    change_to = 'UP'
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    change_to = 'RIGHT'
                # Esc -> Create event to quit the game
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

            # Making sure the snake cannot move in the opposite direction instantaneously
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Moving the snake
    if direction == 'UP':
        snake_pos[1] -= 10
    if direction == 'DOWN':
        snake_pos[1] += 10
    if direction == 'LEFT':
        snake_pos[0] -= 10
    if direction == 'RIGHT':
        snake_pos[0] += 10

    # Snake body growing mechanism
    snake_body.insert(0, list(snake_pos))
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        score += 1
        food_spawn = False
    else:
        snake_body.pop()

    # Spawning food on the screen
    if not food_spawn:
        while True:
            food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
            if not food_on_snake():
                break

    food_spawn = True

    # GFX
    game_window.fill(black)
    for pos in snake_body:
        # Snake body
        # .draw.rect(play_surface, color, xy-coordinate)
        # xy-coordinate -> .Rect(x, y, size_x, size_y)
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

    # Snake food
    pygame.draw.rect(game_window, white, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    # Game Over conditions
    # Getting out of bounds
    if snake_pos[0] < 0 or snake_pos[0] > frame_size_x-10:
        print(f"you die cus 1 {snake_pos}")
        game_over()
    if snake_pos[1] < 0 or snake_pos[1] > frame_size_y-10:
        print(f"you die cus 2 {snake_pos}")
        game_over()
    # Touching the snake body
    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            print(f"you die cus 3 {snake_pos}")
            game_over()

    show_score(1, white, 'consolas', 20)
    # Refresh game screen
    pygame.display.update()

    if isAuto:
        ev = pygame.event.Event ( pygame.USEREVENT )
        pygame.event.post ( ev )

    # Refresh rate
    fps_controller.tick(difficulty)