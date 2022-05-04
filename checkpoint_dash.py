#-------------------------------------------------------------------------------
# Name:         Karanvir Basson
# Purpose:      Personal Project
# Name of Game: Checkpoint Dash
#-------------------------------------------------------------------------------

import pygame, pygame_gui, time, random

class Level: #Holds info about levels
    pass

cars = [ #Holds info about each car, (name, speed, is_locked)
    
    ["Universal", 4, False],
    ["Beetle", 6, True],
    ["Minivan", 7, True],
    ["Coupe", 10, True],
    ["Booster", 12, True],
    ["Speedster", 13, True],

]

num_levels = 5
levels = []
for i in range(1, num_levels + 1): #Populates an array of levels

    is_locked = True
    if i == 1:
        is_locked = False

    level = Level()
    level.number = i #level number
    level.opponent = cars[i][0] #Name of the opponenet
    level.is_locked = is_locked #Is level locked
    level.num_checkpoints = i * 5 #Target checkpoints in level
    level.label = f"Level {i}: Head2Head Against the {cars[i][0]}" #String display on level menu

    levels.append(level)

pygame.init()

(width, height) = (1250, 700) #Size of screen
screen = pygame.display.set_mode((width, height)) #Create game screen
pygame.display.set_caption("Checkpoint Dash")

manager = pygame_gui.UIManager((width, height))
clock = pygame.time.Clock()

while True: #Entire game loop

    start_button = pygame_gui.elements.UIButton(pygame.Rect(80, 275, 500, 300), 'Start', manager)
    instructions_button = pygame_gui.elements.UIButton(pygame.Rect(675, 275, 500, 300), 'Instructions', manager)

    user_car = None
    user_level = None
    opponent_car = None

    #Play menu theme song
    pygame.mixer.init()
    pygame.mixer.music.load("./Soundtracks/StartMenu.mp3")
    pygame.mixer.music.play(-1)

    at_start = True
    while at_start: #start menu loop

        at_levels = False
        at_instructions = False

        screen.fill((0,0,0))
        screen.blit(pygame.font.Font(None, 183).render(f"CHECKPOINT DASH", True, (111,144,202), None), (0, 0))

        seconds = clock.tick(60)/1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == start_button: #If start button pressed, go to level menu
                    manager.clear_and_reset()
                    screen.fill((0,0,0))
                    back_button = pygame_gui.elements.UIButton(pygame.Rect(width/3, height - 100, 200, 50), 'Back', manager)

                    level_choose_buttons = []
                    for level in levels:
                        i = level.number
                        label = level.label

                        if level.is_locked:
                            label += " (LOCKED)"

                        opponent = None

                        for car in cars:
                            if car[0] == level.opponent:
                                opponent = car

                        screen.blit(pygame.font.Font(None, 50).render(label, True, (111,144,202), None), (0, ((i-1) * 120)))
                        level_choose_buttons.append((pygame_gui.elements.UIButton(pygame.Rect(width - 300, ((i-1) * 135), 300, 100), 'Choose', manager), level, opponent))
                        print(level_choose_buttons[-1])
                    
                    at_levels = True              
                else:
                    manager.clear_and_reset()
                    screen.fill((0,0,0))
                    back_button = pygame_gui.elements.UIButton(pygame.Rect(width/3, height - 100, 200, 50), 'Back', manager)

                    screen.blit(pygame.font.Font(None, 50).render(f'These are the instructions for Checkpoint Dash!', True, (111,144,202), None), (200, 0))
                    screen.blit(pygame.font.Font(None, 40).render(f'Move Up: Up Arrow Key', True, (111,144,202), None), (width/3, 200))
                    screen.blit(pygame.font.Font(None, 40).render(f'Move Down: Down Arrow Key', True, (111,144,202), None), (width/3, 300))
                    screen.blit(pygame.font.Font(None, 40).render(f'Move Right: Right Arrow Key', True, (111,144,202), None), (width/3, 400))
                    screen.blit(pygame.font.Font(None, 40).render(f'Move Left: Left Arrow Key', True, (111,144,202), None), (width/3, 500))

                    at_instructions = True

            manager.process_events(event)

        manager.update(seconds)
        manager.draw_ui(screen)
        pygame.display.update()

        while at_instructions:
            seconds = clock.tick(60)/1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == back_button: #If back button pressed, go to start menu
                        manager.clear_and_reset()
                        screen.fill((0,0,0))
                        start_button = pygame_gui.elements.UIButton(pygame.Rect(80, 275, 500, 300), 'Start', manager)
                        instructions_button = pygame_gui.elements.UIButton(pygame.Rect(675, 275, 500, 300), 'Instructions', manager)

                        at_instructions = False

                manager.process_events(event)

            manager.update(seconds)
            manager.draw_ui(screen)
            pygame.display.update()

        while at_levels: #Level menu loop
            
            at_cars = False
            seconds = clock.tick(60)/1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == back_button: #If back button pressed, go to start menu
                        manager.clear_and_reset()
                        screen.fill((0,0,0))
                        start_button = pygame_gui.elements.UIButton(pygame.Rect(80, 275, 500, 300), 'Start', manager)
                        instructions_button = pygame_gui.elements.UIButton(pygame.Rect(675, 275, 500, 300), 'Instructions', manager)

                        at_levels = False
                    else: #If choose button pressed, go to car menu
                        for level_choose_button in level_choose_buttons:
                            if event.ui_element == level_choose_button[0]:
                                user_level = level_choose_button[1]
                                opponent_car = level_choose_button[2]
                        
                        if (not user_level.is_locked):
                            print(user_level.label)
                            print(opponent_car[0])
                            manager.clear_and_reset()
                            screen.fill((0,0,0))

                            back_button = pygame_gui.elements.UIButton(pygame.Rect(0, height - 50, 200, 50), 'Back', manager)
                            
                            i = 0
                            car_choose_buttons = []
                            for car in cars: 
                                name = car[0]
                                sprite = pygame.sprite.Sprite()
                                sprite.image = pygame.image.load(f"./Sprites/{name}.png")
                                sprite.image = pygame.transform.rotate(sprite.image, -90)

                                if car[2]:
                                    name += " (LOCKED)"

                                screen.blit(pygame.font.Font(None, 50).render(name, True, (111,144,202), None), (0, i * 120))
                                screen.blit(sprite.image, (width - 600, i * 120))
                                car_choose_buttons.append((pygame_gui.elements.UIButton(pygame.Rect(width - 300, i * 115, 300, 90), 'Choose', manager), car))                   
                                i += 1

                            at_cars = True

                manager.process_events(event)

            while at_cars: #Car menu loop
                seconds = clock.tick(60)/1000.0

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        quit()

                    if event.type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == back_button: #If back button pressed, go back to level menu
                            manager.clear_and_reset()
                            screen.fill((0,0,0))
                            back_button = pygame_gui.elements.UIButton(pygame.Rect(width/3, height - 100, 200, 50), 'Back', manager)

                            level_choose_buttons = []
                            for level in levels:
                                i = level.number
                                label = level.label

                                if level.is_locked:
                                    label += " (LOCKED)"

                                opponent = None

                                for car in cars:
                                    if car[0] == level.opponent:
                                        opponent = car

                                screen.blit(pygame.font.Font(None, 50).render(label, True, (111,144,202), None), (0, ((i-1) * 120)))
                                level_choose_buttons.append((pygame_gui.elements.UIButton(pygame.Rect(width - 300, ((i-1) * 135), 300, 100), 'Choose', manager), level, opponent))
                                print(level_choose_buttons[-1])
                    
                            at_cars = False
                        else: #If choose button pressed, begin game
                            for car_choose_button in car_choose_buttons:
                                if event.ui_element == car_choose_button[0]:
                                    user_car = car_choose_button[1]

                            if (not user_car[2]):
                                print(user_car[0])
                                at_cars = False
                                at_levels = False
                                at_start = False

                    manager.process_events(event)
                
                manager.update(seconds)
                manager.draw_ui(screen)
                pygame.display.update()

            manager.update(seconds)
            manager.draw_ui(screen)
            pygame.display.update()

    #PLAY IN GAME MUSIC

    pygame.mixer.music.stop()
    pygame.mixer.init()

    music = random.randint(1,2)
    if music==1:
        pygame.mixer.music.load("./Soundtracks/Gameplay1.mp3")
    elif music == 2:
        pygame.mixer.music.load("./Soundtracks/Gameplay2.mp3")

    pygame.mixer.music.play(-1)

    replay = True
    while replay: #GAME LOOP FOR REPLAY

        seconds = clock.tick(60)/1000.0

        user_car_sprite = pygame.sprite.Sprite()
        user_car_sprite.image = pygame.image.load(f"./Sprites/{user_car[0]}.png")

        opponent_car_sprite = pygame.sprite.Sprite()
        opponent_car_sprite.image = pygame.image.load(f"./Sprites/{opponent_car[0]}.png")

        user_score = 0
        opponent_score = 0
        required_score = user_level.num_checkpoints

        adjustment = 60

        checkpoint = pygame.sprite.Sprite()
        checkpoint.image = pygame.image.load("./Sprites/Checkpoint.png")

        #Where user is currently located
        current_user_x = (width / 2) - 100
        current_user_y = height / 2
        current_user_angle = 90

        #Where opponent is currently located
        current_opponent_x = (width / 2) + 100
        current_opponent_y = height / 2
        current_opponent_angle = 90

        #Where checkpoint is currently located
        current_checkpoint_x = random.randint(10, width - adjustment)
        current_checkpoint_y = random.randint(10, height - adjustment)

        countdown_time = 5
        execute_countdown = True
        checkpoint_reached_dist = 75
        opponent_reached_checkpoint_dist = 25

        while user_score < required_score and opponent_score < required_score: #MAIN GAME LOOP

            seconds = clock.tick(60)/1000.0

            screen.fill((0,0,0))
            screen.blit(user_car_sprite.image, (current_user_x, current_user_y))
            screen.blit(opponent_car_sprite.image, (current_opponent_x, current_opponent_y))
            screen.blit(pygame.font.Font(None, 50).render(f"User: {user_score}", True, (255,255,255), None), (75, 0))
            screen.blit(pygame.font.Font(None, 75).render(f"Target: {required_score}", True, (255,0,0), None), ((width - 275) / 2, 0))
            screen.blit(pygame.font.Font(None, 50).render(f"Opponent: {opponent_score}", True, (255,255,255), None), (width - 275, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            if execute_countdown == True: #Execute countdown

                for count in range(countdown_time, 0, -1):

                    screen.fill((0,0,0))
                    screen.blit(user_car_sprite.image, (current_user_x, current_user_y))
                    screen.blit(opponent_car_sprite.image, (current_opponent_x, current_opponent_y))
                    screen.blit(pygame.font.Font(None, 50).render(f"User: {user_score}", True, (255,255,255), None), (75, 0))
                    screen.blit(pygame.font.Font(None, 75).render(f"Target: {required_score}", True, (255,0,0), None), ((width - 275) / 2, 0))
                    screen.blit(pygame.font.Font(None, 50).render(f"Opponent: {opponent_score}", True, (255,255,255), None), (width - 275, 0))
                    screen.blit(pygame.font.Font(None, 228).render(str(count), True, (200,0,0), None), (width / 2, (height / 2) - adjustment))
                    pygame.display.update()

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            quit()
                    else:
                        time.sleep(1)

                screen.fill((0,0,0))
                screen.blit(user_car_sprite.image, (current_user_x, current_user_y))
                screen.blit(opponent_car_sprite.image, (current_opponent_x, current_opponent_y))
                screen.blit(pygame.font.Font(None, 50).render(f"User: {user_score}", True, (255,255,255), None), (75, 0))
                screen.blit(pygame.font.Font(None, 75).render(f"Target: {required_score}", True, (255,0,0), None), ((width - 275) / 2, 0))
                screen.blit(pygame.font.Font(None, 50).render(f"Opponent: {opponent_score}", True, (255,255,255), None), (width - 275, 0))
                screen.blit(pygame.font.Font(None, 228).render("GO!", True, (0,200,0), None), (width / 2, (height / 2) - adjustment))
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        quit()
                else:
                    time.sleep(1)

                execute_countdown = False

            else: #Run normal game
                screen.blit(checkpoint.image, (current_checkpoint_x, current_checkpoint_y))

                user_car_sprite.rect = user_car_sprite.image.get_rect()
                user_car_sprite.rect.center = (current_user_x, current_user_y)
                
                opponent_car_sprite.rect = opponent_car_sprite.image.get_rect()
                opponent_car_sprite.rect.center = (current_opponent_x, current_opponent_y)

                if (not pygame.sprite.collide_rect(user_car_sprite, opponent_car_sprite)):
                    slowdown = random.randint(0, opponent_car[1] // 2)
                    
                    #Determine next cpu move
                    if (current_checkpoint_x - current_opponent_x > opponent_reached_checkpoint_dist):
                        opponent_car_sprite.image = pygame.transform.rotate(opponent_car_sprite.image, 0 - current_opponent_angle)
                        current_opponent_x += opponent_car[1] - slowdown
                        current_opponent_angle = 0
                    elif (current_opponent_x - current_checkpoint_x > opponent_reached_checkpoint_dist):
                        opponent_car_sprite.image = pygame.transform.rotate(opponent_car_sprite.image, 180 - current_opponent_angle)
                        current_opponent_x -= opponent_car[1] - slowdown
                        current_opponent_angle = 180
                    elif (current_opponent_y - current_checkpoint_y > opponent_reached_checkpoint_dist):
                        opponent_car_sprite.image = pygame.transform.rotate(opponent_car_sprite.image, 90 - current_opponent_angle)
                        current_opponent_y -= opponent_car[1] - slowdown
                        current_opponent_angle = 90
                    elif (current_checkpoint_y - current_opponent_y > opponent_reached_checkpoint_dist):
                        opponent_car_sprite.image = pygame.transform.rotate(opponent_car_sprite.image, 270 - current_opponent_angle)
                        current_opponent_y += opponent_car[1] - slowdown
                        current_opponent_angle = 270
                    else:
                        pass
                else: #if user and CPU collide
                    knockback = 15

                    #Determine how cars should get knocked back
                    if current_opponent_x > current_user_x:
                        current_user_x -= knockback
                        current_opponent_x += knockback
                    else:
                        current_user_x += knockback
                        current_opponent_x -= knockback

                    if current_opponent_y > current_user_y:
                        current_user_y -= knockback
                        current_opponent_y += knockback
                    else:
                        current_user_y += knockback
                        current_opponent_y -= knockback

                checkpoint_x_dist_opponent = abs(current_checkpoint_x - current_opponent_x)
                checkpoint_y_dist_opponent = abs(current_checkpoint_y - current_opponent_y)
                opponent_at_checkpoint = (checkpoint_x_dist_opponent < checkpoint_reached_dist and checkpoint_y_dist_opponent < checkpoint_reached_dist)

                checkpoint_x_dist_user = abs(current_checkpoint_x - current_user_x)
                checkpoint_y_dist_user = abs(current_checkpoint_y - current_user_y)
                user_at_checkpoint = (checkpoint_x_dist_user < checkpoint_reached_dist and checkpoint_y_dist_user < checkpoint_reached_dist)

                if user_at_checkpoint or opponent_at_checkpoint:
                    
                    #Calcuate location of new checkpoint
                    new_x = current_checkpoint_x
                    new_y = current_checkpoint_y

                    while (abs(new_x - current_checkpoint_x) < 200 and abs(new_y - current_checkpoint_y) < 200):
                        new_x = random.randint(10, width - adjustment)
                        new_y = random.randint(10, height - adjustment)

                    current_checkpoint_x = new_x
                    current_checkpoint_y = new_y

                    if user_at_checkpoint and not opponent_at_checkpoint: #If user reached checkpoint
                        user_score += 1
                    elif opponent_at_checkpoint and not user_at_checkpoint: #If opponent reached checkpoint
                        opponent_score += 1
                    else: #If tie (not likely)
                        pass
                
                keys = pygame.key.get_pressed()

                if (keys[pygame.K_RIGHT]): #If right key pressed, move right
                    if (current_user_x < (width - adjustment)): 
                        user_car_sprite.image = pygame.transform.rotate(user_car_sprite.image, 0 - current_user_angle)
                        current_user_x += user_car[1]
                        current_user_angle = 0
                elif (keys[pygame.K_LEFT]): #If left key pressed, move left
                    if (current_user_x > 0): 
                        user_car_sprite.image = pygame.transform.rotate(user_car_sprite.image, 180 - current_user_angle)
                        current_user_x -= user_car[1]
                        current_user_angle = 180
                elif (keys[pygame.K_UP]): #If up key pressed, move up
                    if (current_user_y > 0): 
                        user_car_sprite.image = pygame.transform.rotate(user_car_sprite.image, 90 - current_user_angle)
                        current_user_y -= user_car[1]
                        current_user_angle = 90
                elif (keys[pygame.K_DOWN]): #If down key pressed, move down
                    if (current_user_y < (height - adjustment)): 
                        user_car_sprite.image = pygame.transform.rotate(user_car_sprite.image, 270 - current_user_angle)
                        current_user_y += user_car[1]
                        current_user_angle = 270
                else:
                    pass

            pygame.display.update()

        manager.clear_and_reset()
        screen.fill((0,0,0))
        replay_button = pygame_gui.elements.UIButton(pygame.Rect(80, 275, 500, 300), 'Replay', manager)
        continue_button = pygame_gui.elements.UIButton(pygame.Rect(675, 275, 500, 300), 'Back To Menu', manager)

        if user_score == required_score: #If user won
            screen.blit(pygame.font.Font(None, 175).render(f"You Win!", True, (0,255,0), None), ((width - 475) / 2, 0))
            
            #Unlock new car and level
            for car in cars:
                if car[0] == opponent_car[0]:
                    car[2] = False

            if user_level.number < num_levels:
                levels[user_level.number].is_locked = False

        else: #if opponent won
            screen.blit(pygame.font.Font(None, 175).render(f"You Lose!", True, (255,0,0), None), ((width - 475) / 2, 0))

        at_game_end = True
        while at_game_end: #Display end of game screen
            seconds = clock.tick(60)/1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

                if event.type == pygame_gui.UI_BUTTON_PRESSED:

                    if event.ui_element == replay_button:
                        pass
                    else:
                        replay = False

                    at_game_end = False

                manager.process_events(event)

            manager.update(seconds)
            manager.draw_ui(screen)
            pygame.display.update()

        manager.clear_and_reset()
