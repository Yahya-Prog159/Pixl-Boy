# importing the used libraries
import pygame
import sys

# initializing pygame
pygame.init()

# Const variables
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400


# Creating the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Setting the clock
clock = pygame.time.Clock()

# set the title of the screen 
pygame.display.set_caption("AUC Game")


# Sounds
background_sound = pygame.mixer.Sound('Codes/S6_Game/Assets/game-music-loop-7-145285.mp3')
lost_sound = pygame.mixer.Sound('Codes/S6_Game/Assets/ost.mp3')


# Sky
sky_img = pygame.image.load('Codes/S6_Game/Assets/Sky.png')
sky_rect = sky_img.get_rect(topleft =(0, 0))


# Ground
ground_img = pygame.image.load('Codes/S6_Game/Assets/ground.png')
ground_rect = ground_img.get_rect(topleft =(0, 250) )


# Player
player_img1 = pygame.image.load('Codes/S6_Game/Assets/player_walk_1.png')
player_img2 = pygame.image.load('Codes/S6_Game/Assets/player_walk_2.png')
player_imgs = [player_img1, player_img2]
player_index = 0 
player = player_imgs[player_index]
player_rect = player.get_rect(midbottom =(100, 250))

# Snail
snail1 = pygame.image.load('Codes/S6_Game/Assets/snail1.png')
snail2 = pygame.image.load('Codes/S6_Game/Assets/snail2.png')
snail_imgs = [snail1, snail2]
snail_index = 0 
snail = snail_imgs[snail_index]
snail_rect = snail.get_rect(midbottom =(700, 250))

# Font Styling
font_style = pygame.font.Font('Codes/S6_Game/Assets/Pixeltype.ttf', 50)


# Jumping Variables
jump_H = 11
gravity = .5
player_V_Y = 0
is_jumping = False


# Variables
Start = 0
Play = 1
Pause = 2
Game_over = 3
Game_state = Start


# Anuimation timer
animaion_time = 200
last_update_time = pygame.time.get_ticks()


# Variables
score = 0
start_time = 0
difficulty_increase_time = 5000
last_difficulty_time = pygame.time.get_ticks()


# Game loop
while True:
    
    background_sound.play()

    # main loop
    for _ in pygame.event.get():
        # Close the window
        if _.type == pygame.QUIT:
            sys.exit()
        if _.type == pygame.KEYDOWN:
            if Game_state == Start and _.key == pygame.K_SPACE:
                Game_state = Play
                background_sound.play(-1)
                start_time = pygame.time.get_ticks()
                score = 0
            elif Game_state == Game_over and _.key == pygame.K_SPACE:
                background_sound.stop()
                # lost_sound.play()
                Game_state = Start
                snail_rect.midbottom = (600, 250)
                player_rect.midbottom = (50, 250)
                background_sound.stop()
            
            elif Game_state == Play and _.key == pygame.K_SPACE and not is_jumping:
                player_V_Y = -jump_H
                is_jumping = True
            elif Game_state == Play and _.key == pygame.K_p:
                Game_state = Pause
            elif Game_state == Pause and _.key == pygame.K_p:
                background_sound.stop()
                Game_state = Play
                background_sound.play()
    screen.fill((94, 129, 162))

    if Game_state == Start:
        draw_text = font_style.render('Press SPACE to start', False, 'black')
        draw_rect = draw_text.get_rect(center=(400, 200))
        screen.blit(draw_text, draw_rect)

    elif Game_state == Play:
        if is_jumping:
            player_V_Y += gravity
            player_rect.y += player_V_Y

            if player_rect.bottom >= ground_rect.top:
                player_rect.bottom = ground_rect.top
                is_jumping = False
                player_V_Y = 0


        snail_rect.left -= 5
        if snail_rect.right < 0:
            snail_rect.left = 800
            score += 1


        current_time = pygame.time.get_ticks()
        if current_time - last_update_time > animaion_time:
            snail_index = (snail_index + 1) % len(snail_imgs)
            snail = snail_imgs[snail_index]
            last_update_time = current_time
            player_index = (player_index + 1) % len(player_imgs)
            player = player_imgs[player_index] 

    
        if player_rect.colliderect(snail_rect):
            Game_state = Game_over

        if current_time - last_difficulty_time > difficulty_increase_time:
            last_difficulty_time = current_time
            snail_rect.left -= 1


        elapsed_time = (current_time - start_time) // 1000

    # Loading images in the screen
        screen.blit(sky_img, sky_rect)
        screen.blit(ground_img, ground_rect)
        screen.blit(player, player_rect)
        screen.blit(snail, snail_rect)

    # Render and display the score
        text = font_style.render(f'Score: {score}', False, 'black')
        screen.blit(text, (10, 10))

        time_text = font_style.render(f'Time: {elapsed_time}s', False, 'black')
        screen.blit(time_text, (10, 40))

    elif Game_state == Pause:
        background_sound.stop()
        draw_text = font_style.render('Paused, Press P to Resume', False, 'black')
        draw_rect = draw_text.get_rect(center=(400, 200))
        screen.blit(draw_text, draw_rect)

    elif Game_state == Game_over:
        background_sound.stop()
        draw_text = font_style.render('Game Over| Press SPACE to Restart', False, 'black')
        draw_rect = draw_text.get_rect(center=(400, 200))
        screen.blit(draw_text, draw_rect)


    # Update the screen
    pygame.display.update()
    clock.tick(60)
