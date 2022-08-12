import sys
import os

import pgzrun
import random


TITLE = 'Tank vs Zombies by EscapeFromHell'
WIDTH = 800
HEIGHT = 600
TANK_SIZE = 20
ZOMBIE_SPEED = 1
BULLET_SPEED = 20
BULLET_SIZE = 6
CHOICES = {
    1: 'easy',
    2: 'medium',
    3: 'hard'
}
ANGLE = {
    'w': 180,
    'a': 270,
    's': 0,
    'd': 90,
    'wd': 135,
    'sd': 45,
    'wa': 225,
    'sa': 315
}

tank = Actor('tank.png')
tank.x = 400
tank.y = 300

bullet = Actor('bullet.png')
bullet_fired = False

score = 0
play_music = True
play_sound = True
game_start = True
game_over = False
game_win = False
zombie_list = []
count_of_zombies = 0


def input_difficulty(difficulty):
    '''Функция изменения сложности.'''
    global count_of_zombies
    if difficulty == 'easy':
        count_of_zombies = 5
    if difficulty == 'medium':
        count_of_zombies = 7
    if difficulty == 'hard':
        count_of_zombies = 10


def draw():
    '''Функция отрисовки объектов и экранов начала/конца игры'''
    global game_start, game_over, game_win, score, play_sound, play_music
    if game_start:
        screen.fill('black')
        screen.draw.text('Choose difficulty:', (300, 150))
        screen.draw.text('Press "E" to "easy"', (300, 200))
        screen.draw.text('Press "M" to "medium"', (300, 250))
        screen.draw.text('Press "H" to "hard"', (300, 300))
        if keyboard.e:
            input_difficulty(CHOICES[1])
            game_start = False
        if keyboard.m:
            input_difficulty(CHOICES[2])
            game_start = False
        if keyboard.h:
            input_difficulty(CHOICES[3])
            game_start = False
    else:
        if not game_over:
            screen.blit('tank_background.png', (0, 0))
            tank.draw()
            bullet.draw()
            shoot_bullet()
            create_zombies()
            move_zombie()
            screen.draw.text(f'score: {score}', (350, 150))
            if play_music:
                music.play('music.wav')
                play_music = False
        if game_over:
            screen.fill('red')
            screen.draw.text(f'GAME OVER, Your score: {score}', (285, 150))
            screen.draw.text('Press "Space" to restart', (300, 250))
            music.stop()
            if play_sound:
                sounds.gameover.play()
                play_sound = False
        if game_win:
            screen.fill('blue')
            screen.draw.text(f'You Win, Your score: {score}', (300, 150))
            screen.draw.text('Press "Space" to restart', (300, 250))
            music.stop()
            if play_sound:
                sounds.gamewin.play()
                play_sound = False


def update():
    '''Функция настраивает управление и поворочивает/располагает объекты.'''
    global bullet_fired, game_over
    if keyboard.escape:
        quit()
    if game_over:
        if keyboard.space:
            restart_program()
    if (keyboard.w) and (tank.y > TANK_SIZE):
        tank.y = tank.y - 5
        tank.angle = ANGLE['w']
    if (keyboard.a) and (tank.x > TANK_SIZE):
        tank.x = tank.x - 5
        tank.angle = ANGLE['a']
    if (keyboard.s) and (tank.y < (HEIGHT - TANK_SIZE)):
        tank.y = tank.y + 5
        tank.angle = ANGLE['s']
    if (keyboard.d) and (tank.x < (WIDTH - TANK_SIZE)):
        tank.x = tank.x + 5
        tank.angle = ANGLE['d']
    if (keyboard.w) and (keyboard.d):
        tank.angle = ANGLE['wd']
    if (keyboard.s) and (keyboard.d):
        tank.angle = ANGLE['sd']
    if (keyboard.w) and (keyboard.a):
        tank.angle = ANGLE['wa']
    if (keyboard.s) and (keyboard.a):
        tank.angle = ANGLE['sa']
    if keyboard.space:
        if not bullet_fired:
            sounds.explosion.play()
            bullet_fired = True
            if tank.angle == ANGLE['w']:
                bullet.x = tank.x
                bullet.y = tank.y - 30
                bullet.angle = ANGLE['w']
            if tank.angle == ANGLE['a']:
                bullet.x = tank.x - 30
                bullet.y = tank.y
                bullet.angle = ANGLE['a']
            if tank.angle == ANGLE['s']:
                bullet.x = tank.x
                bullet.y = tank.y + 30
                bullet.angle = ANGLE['s']
            if tank.angle == ANGLE['d']:
                bullet.x = tank.x + 30
                bullet.y = tank.y
                bullet.angle = ANGLE['d']
            if tank.angle == ANGLE['wd']:
                bullet.x = tank.x + TANK_SIZE
                bullet.y = tank.y - TANK_SIZE
                bullet.angle = ANGLE['wd']
            if tank.angle == ANGLE['sd']:
                bullet.x = tank.x + TANK_SIZE
                bullet.y = tank.y + TANK_SIZE
                bullet.angle = ANGLE['sd']
            if tank.angle == ANGLE['wa']:
                bullet.x = tank.x - TANK_SIZE
                bullet.y = tank.y - TANK_SIZE
                bullet.angle = ANGLE['wa']
            if tank.angle == ANGLE['sa']:
                bullet.x = tank.x - TANK_SIZE
                bullet.y = tank.y + TANK_SIZE
                bullet.angle = ANGLE['sa']


def shoot_bullet():
    '''Функция настраивает полет снаряда.'''
    global bullet_fired, bullet, game_over, game_win
    if bullet_fired:
        if bullet.angle == ANGLE['w']:
            bullet.y -= BULLET_SPEED
        if bullet.angle == ANGLE['a']:
            bullet.x -= BULLET_SPEED
        if bullet.angle == ANGLE['s']:
            bullet.y += BULLET_SPEED
        if bullet.angle == ANGLE['d']:
            bullet.x += BULLET_SPEED
        if bullet.angle == ANGLE['wd']:
            bullet.x += BULLET_SPEED
            bullet.y -= BULLET_SPEED
        if bullet.angle == ANGLE['sd']:
            bullet.x += BULLET_SPEED
            bullet.y += BULLET_SPEED
        if bullet.angle == ANGLE['wa']:
            bullet.x -= BULLET_SPEED
            bullet.y -= BULLET_SPEED
        if bullet.angle == ANGLE['sa']:
            bullet.x -= BULLET_SPEED
            bullet.y += BULLET_SPEED
        if bullet.x >= WIDTH + BULLET_SIZE or bullet.x <= - BULLET_SIZE or \
           bullet.y >= HEIGHT + BULLET_SIZE or bullet.y <= - BULLET_SIZE:
            bullet_fired = False
        if game_over or game_win:
            bullet_fired = False


def create_zombies():
    '''Функция настраивает создание противников.'''
    global zombie_list, count_of_zombies
    if len(zombie_list) < count_of_zombies:
        rand_place = random.randint(0, 3)
        if rand_place == 0:
            y = random.randint(40, HEIGHT - 40)
            zombie = Actor('zombie_stand.png')
            zombie.x = 1
            zombie.y = y
            zombie_list.append(zombie)
        if rand_place == 1:
            y = random.randint(40, HEIGHT - 40)
            zombie = Actor('zombie_stand.png')
            zombie.x = WIDTH - 1
            zombie.y = y
            zombie_list.append(zombie)
        if rand_place == 2:
            x = random.randint(40, WIDTH - 40)
            zombie = Actor('zombie_stand.png')
            zombie.x = x
            zombie.y = 1
            zombie_list.append(zombie)
        if rand_place == 3:
            x = random.randint(40, WIDTH - 40)
            zombie = Actor('zombie_stand.png')
            zombie.x = x
            zombie.y = HEIGHT - 1
            zombie_list.append(zombie)


def move_zombie():
    '''Функция настраивает движение противников и условия победы/поражения.'''
    global score, game_over, game_win, zombie_list, tank
    for zombie in zombie_list:
        if zombie.x < tank.x:
            zombie.x += ZOMBIE_SPEED
        if zombie.x > tank.x:
            zombie.x -= ZOMBIE_SPEED
        if zombie.y < tank.y:
            zombie.y += ZOMBIE_SPEED
        if zombie.y > tank.y:
            zombie.y -= ZOMBIE_SPEED
        for zombie in zombie_list:
            zombie.draw()
            if zombie.colliderect(bullet):
                zombie_list.remove(zombie)
                sounds.hit.play()
                score += 1
                if score == 50:
                    game_win = True
            if zombie.colliderect(tank):
                game_over = True


def restart_program():
    '''Рестарт программы.'''
    python = sys.executable
    os.execl(python, python, * sys.argv)


pgzrun.go()
