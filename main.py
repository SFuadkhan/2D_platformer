import random
import sys

import pygame as p

image_path = ""

clock = p.time.Clock()
start_ticks = p.time.get_ticks()
current_ticks = start_ticks

p.init()
screen = p.display.set_mode((618, 359))
p.display.set_caption("GAME")
running = True
icon = p.image.load(image_path + "images/icon.jpeg").convert_alpha()
p.display.set_icon(icon)
ammo_box = p.image.load(image_path + "images/ammo_box.png").convert_alpha()
health_box = p.image.load(image_path + "images/first-aid-box.png").convert_alpha()
bg = p.image.load(image_path + "images/bg3.png").convert_alpha()
player = p.image.load(image_path + "images/player_right/right_1.png").convert_alpha()
bg_x = 0
player_pov = p.image.load(image_path + "images/player_right/right_1.png").convert_alpha()
walk_right = [
    p.image.load(image_path + "images/player_right/right_1.png").convert_alpha(),
    p.image.load(image_path + "images/player_right/right_2.png").convert_alpha(),
    p.image.load(image_path + "images/player_right/right_3.png").convert_alpha(),
    p.image.load(image_path + "images/player_right/right_4.png").convert_alpha()
]
walk_left = [
    p.image.load(image_path + "images/player_left/left_1.png").convert_alpha(),
    p.image.load(image_path + "images/player_left/left_2.png").convert_alpha(),
    p.image.load(image_path + "images/player_left/left_3.png").convert_alpha(),
    p.image.load(image_path + "images/player_left/left_4.png").convert_alpha()
]

soundtracks = [
    p.mixer.Sound(image_path + "sounds/1-04. Polargeist.mp3"),
    p.mixer.Sound(image_path + "sounds/1-02. Stereo Madness.mp3"),
    p.mixer.Sound(image_path + "sounds/1-03. Back On Track.mp3"),
    p.mixer.Sound(image_path + "sounds/1-07. Can't Let Go.mp3"),
    p.mixer.Sound(image_path + "sounds/1-06. Base After Base.mp3")
]
game_over_sound = p.mixer.Sound(image_path + "sounds/game_over.wav")
shot_sound = p.mixer.Sound(image_path + "sounds/cartoon-shot.wav")
jump_sound = p.mixer.Sound(image_path + "sounds/cartoon-jump-6462.mp3")

heart_icon = p.image.load(image_path + "images/heart.png").convert_alpha()
player_hp = 0
muted_icon = p.image.load(image_path + "images/mute.png").convert_alpha()
volume_icon = p.image.load(image_path + "images/volume.png").convert_alpha()
music_icon = p.image.load(image_path + "images/music.png").convert_alpha()
music_muted_icon = p.image.load(image_path + "images/music_mute.png").convert_alpha()

kill_sounds = [
    p.mixer.Sound(image_path + "sounds/tom_scream1.mp3"),
    p.mixer.Sound(image_path + "sounds/tom_scream2.mp3")
]
player_hit = [
    p.mixer.Sound(image_path + "sounds/player_hit1.mp3"),
    p.mixer.Sound(image_path + "sounds/player_hit2.mp3")
]
reload_sound = p.mixer.Sound(image_path + "sounds/reload.mp3")
health_sound = p.mixer.Sound(image_path + "sounds/health_charger.mp3")
player_speed = 5
player_x = 150
player_walk_anim = 0
player_y = 250
jump_count = 8
is_jump = False
last_x = player_x
last_y = player_y

game_over = False
game_over_icon = p.image.load(image_path + "images/game_over(1).png").convert_alpha()

monsters = []
monsters_rect = []

gh1 = p.image.load(image_path + "images/ghost1.png").convert_alpha()
gh2 = p.image.load(image_path + "images/ghost2.png").convert_alpha()
gh3 = p.image.load(image_path + "images/ghost3.png").convert_alpha()
zm1 = p.image.load(image_path + "images/zombie.png").convert_alpha()
zm2 = p.image.load(image_path + "images/zombie1.png").convert_alpha()
gh = gh1
ghosts = [
    gh1, gh2, gh3, zm1, zm2, zm1, zm2, zm1, zm2
]

ghost_timer = p.USEREVENT + 1
p.time.set_timer(ghost_timer, 2000)
score_timer = p.USEREVENT + 2
p.time.set_timer(score_timer, 100)
soundtracks_timer = p.USEREVENT + 3
p.time.set_timer(soundtracks_timer, 60000)

label = p.font.Font(image_path + "fonts/KodeMono-Bold.ttf", 40)
label1 = p.font.Font(image_path + "fonts/KodeMono-Bold.ttf", 20)

play_again_label = label.render("Play Again?", True, "green")

mouse = p.mouse.get_pos()

bullets = 5
bullet = p.image.load(image_path + "images/bullet.png").convert_alpha()
bullets_shot = []
ammo = p.image.load(image_path + "images/bullets.png").convert_alpha()

score = 0

ticks = 40
choose_diff1 = label.render("Choose Difficulty:", True, "green")
choose_diff2 = label1.render("Easy(E)   Hard(H)   Impossible(I)", True, "green")
change_diff1 = label1.render("To change difficulty[C]", True, "green")
change_diff2 = label1.render("(progress will be erased)", True, "green")
is_difficulty_selected = False
difficulty = None
is_godmode = False
is_sounds_muted = False
is_music_muted = False
is_paused = False
pause_icon = p.image.load(image_path + "images/pause_icon.png").convert_alpha()
some_soundtrack = random.randint(0, 4)
soundtracks[some_soundtrack].play()
ammunition_boxes = [
    ammo_box, health_box
]
bonuses_in_game = []
bonus = ammo_box
while running:

    if not is_difficulty_selected:
        screen.fill(color=(54, 69, 79))
        screen.blit(choose_diff1, (70, 50))
        screen.blit(choose_diff2, (90, 200))
        is_godmode = False
        controls = p.key.get_pressed()
        if controls[p.K_e]:
            difficulty = "easy"
            player_hp = 3
            is_difficulty_selected = True
            ammunition_timer = p.USEREVENT + 4
            p.time.set_timer(ammunition_timer, 10000)
        elif controls[p.K_h]:
            difficulty = "hard"
            player_hp = 1
            is_difficulty_selected = True
            ammunition_timer = p.USEREVENT + 4
            p.time.set_timer(ammunition_timer, 30000)
        elif controls[p.K_i]:
            difficulty = "impossible"
            player_hp = 1
            is_difficulty_selected = True
            ammunition_timer = None
            ticks = 100
            bullets = 0
        elif controls[p.K_g]:
            is_godmode = True
            difficulty = "godmode"
            ammunition_timer = p.USEREVENT + 4
            player_hp = 42
            p.time.set_timer(ammunition_timer, 5000)
            bullets = 999
            is_difficulty_selected = True
        clock.tick(60)
        p.display.update()
        for event in p.event.get():
            if event.type == p.QUIT or (event.type == p.KEYUP and p.key.get_pressed()[p.K_ESCAPE]):
                running = False
                p.quit()
                sys.exit(0)
    else:
        if difficulty == "easy":
            ticks = 30
        elif difficulty == "hard":
            if ticks <= 70:
                ticks = score / 100
        elif difficulty == "impossible":
            ticks = 100
        ammo_num = label.render("X" + bullets.__str__(), True, "purple")
        score_show = label.render(score.__str__(), True, (255, 255, 255))
        hp_show = label.render("X" + player_hp.__str__(), True, "red")
        if is_paused:
            screen.fill((54, 69, 79))
            screen.blit(pause_icon, ((screen.get_width() - pause_icon.get_width()) / 2, 20))
            screen.blit(change_diff1,
                        ((screen.get_width() - change_diff1.get_width()) / 2, pause_icon.get_height() + 50))
            screen.blit(change_diff2,
                        ((screen.get_width() - change_diff2.get_width()) / 2, pause_icon.get_height() + 80))
            is_music_muted = True
            is_sounds_muted = True

        elif not game_over:
            screen.blit(bg, (bg_x, 0))
            screen.blit(bg, (bg_x + 618, 0))
            player_walk_anim += 1
            player_walk_anim %= 4
            bg_x -= 2
            if bg_x == -618:
                bg_x = 0
            if bonuses_in_game:
                for (index, el) in enumerate(bonuses_in_game):
                    screen.blit(bonus, (el.x, el.y))
                    el.x -= 2
                    if el.x < -10:
                        bonuses_in_game.pop(index)
                    if player_rect.colliderect(el):
                        if bonus == ammo_box:
                            if not is_sounds_muted:
                                reload_sound.play()
                            bullets += 3
                        elif bonus == health_box:
                            if not is_sounds_muted:
                                health_sound.play()
                            player_hp += 1

                        bonuses_in_game.pop(index)

            if monsters and monsters_rect:
                for (index, el) in enumerate(monsters_rect):
                    screen.blit(monsters[index], (el.x, el.y))
                    el.x -= 10

                    if el.x < -10:
                        monsters.pop(index)
                        monsters_rect.pop(index)

                    if player_rect.colliderect(el) and not is_godmode:
                        player_hp -= 1
                        if not is_sounds_muted:
                            random.choice(player_hit).play()
                        monsters.pop(index)
                        monsters_rect.pop(index)
                        if player_hp == 0:
                            # is_sounds_muted = True
                            game_over = True
                            if not is_sounds_muted:
                                game_over_sound.play()
            if bullets_shot:
                for (index, el) in enumerate(bullets_shot):
                    screen.blit(bullet, (el.x, el.y))
                    el.x += 15

                    if el.x > 650:
                        bullets_shot.pop(index)

                    if monsters and bullets_shot:
                        for (i, ghost) in enumerate(monsters_rect):
                            if ghost.colliderect(el) and (monsters[i] == zm1 or monsters[i] == zm2):
                                if not is_sounds_muted:
                                    random.choice(kill_sounds).play()
                                monsters.pop(i)
                                monsters_rect.pop(i)
                                bullets_shot.pop(index)

            player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))

            if player_x == last_x:
                screen.blit(player_pov, (player_x, player_y))

            keys = p.key.get_pressed()
            if keys[p.K_d] or keys[p.K_RIGHT]:
                screen.blit(walk_right[player_walk_anim], (player_x, player_y))
                player_pov = p.image.load("images/player_right/right_1.png").convert_alpha()
            elif keys[p.K_a] or keys[p.K_LEFT]:
                screen.blit(walk_left[player_walk_anim], (player_x, player_y))
                player_pov = p.image.load("images/player_left/left_1.png").convert_alpha()

            if (keys[p.K_a] or keys[p.K_LEFT]) and player_x > 50:
                player_x -= player_speed
            elif (keys[p.K_d] or keys[p.K_RIGHT]) and player_x < 550:
                player_x += player_speed

            if not is_jump:
                if keys[p.K_SPACE] or keys[p.K_w] or keys[p.K_UP]:
                    is_jump = True
                    if not is_sounds_muted:
                        jump_sound.play()
            else:
                if jump_count >= -8:
                    if jump_count > 0:
                        player_y -= (jump_count ** 2) / 2
                    else:
                        player_y += (jump_count ** 2) / 2
                    jump_count -= 1
                else:
                    is_jump = False
                    jump_count = 8

            screen.blit(ammo, (10, 10))
            screen.blit(ammo_num, (70, 10))
            screen.blit(heart_icon, (17, ammo.get_height() + 13))
            screen.blit(hp_show, (70, ammo.get_height() + 2))

            if is_sounds_muted:
                screen.blit(muted_icon, (550, 10))
            else:
                screen.blit(volume_icon, (550, 10))
            if is_music_muted:
                screen.blit(music_muted_icon, (550, 45))
            else:
                screen.blit(music_icon, (550, 45))

            screen.blit(score_show, ((618 - score_show.get_width()) / 2, 0))
        else:
            screen.fill(color="Black")
            screen.blit(game_over_icon, (180, 20))
            screen.blit(play_again_label, (180, 250))
            screen.blit(score_show, ((618 - score_show.get_width()) / 2, 0))
            if p.mouse.get_pressed()[0]:
                player_x = 150
                player_y = 250
                jump_count = 8
                monsters.clear()
                bonuses_in_game.clear()
                bullets_shot.clear()
                if difficulty == "impossible":
                    bullets = 0
                    player_hp = 1
                elif difficulty == "hard":
                    bullets = 5
                    player_hp = 1
                elif difficulty == "easy":
                    bullets = 5
                    player_hp = 3
                elif difficulty == "godmode":
                    bullets = 999
                    player_hp = 42
                score = 0
                game_over = False

        for event in p.event.get():
            if event.type == p.QUIT or keys[p.K_ESCAPE]:
                running = False
                p.quit()
                sys.exit(0)
            if event.type == p.KEYDOWN and event.key == p.K_p:
                is_paused = not is_paused
                if difficulty != "impossible":
                    if is_paused:
                        start_ticks = p.time.get_ticks()
                        ammunition_timer = None
                    elif not is_paused:
                        ammunition_timer = p.USEREVENT + 4
                        current_ticks = p.time.get_ticks()
                        elapsed_time = (current_ticks - start_ticks) // 1000 * 1000
                        if difficulty == "easy":
                            p.time.set_timer(ammunition_timer, 10000 - elapsed_time % 10000)
                        elif difficulty == "hard":
                            p.time.set_timer(ammunition_timer, 30000 - elapsed_time % 30000)
                        elif difficulty == "godmode":
                            p.time.set_timer(ammunition_timer, 5000 - elapsed_time % 5000)

            else:
                if (event.type == ammunition_timer and not game_over) and not is_paused:
                    if difficulty == "easy":
                        p.time.set_timer(ammunition_timer, 10000)
                    elif difficulty == "hard":
                        p.time.set_timer(ammunition_timer, 30000)
                    elif difficulty == "godmode":
                        p.time.set_timer(ammunition_timer, 5000)
                    bonus = random.choice(ammunition_boxes)
                    bonuses_in_game.append(bonus.get_rect(topleft=(620, 255)))
                if (event.type == ghost_timer and not game_over) and not is_paused:
                    p.time.set_timer(ghost_timer, 2000 - random.randint(-10 + score // 100, 15) * 100)
                    gh = ghosts[random.randint(0, 8)]
                    monsters.append(gh)
                    monsters_rect.append(gh.get_rect(topleft=(620, 255)))
                if (event.type == score_timer and not game_over) and not is_paused:
                    score += 1
                if ((event.type == soundtracks_timer and not game_over and not is_music_muted) or
                        (event.type == p.KEYUP and is_music_muted and event.key == p.K_n)):
                    soundtracks[some_soundtrack].stop()
                    while True:
                        temp = random.randint(0, 4)
                        if some_soundtrack != temp:
                            some_soundtrack = temp
                            break
                    soundtracks[some_soundtrack].play()
                if not game_over and bullets > 0 and event.type == p.KEYUP and event.key == p.K_x:
                    bullets_shot.append(bullet.get_rect(topleft=(player_x + 30, player_y)))
                    bullets -= 1
                    if not is_sounds_muted:
                        shot_sound.play()
                if event.type == p.KEYUP and event.key == p.K_m:
                    is_sounds_muted = not is_sounds_muted
                if event.type == p.KEYUP and event.key == p.K_n:
                    is_music_muted = not is_music_muted
                if event.type == p.KEYUP and event.key == p.K_c and is_paused:
                    is_difficulty_selected = False
                    game_over = True

            last_x = player_x
            last_y = player_y
            if is_music_muted:
                soundtracks[some_soundtrack].stop()
        clock.tick(20 + ticks)
        p.display.update()
