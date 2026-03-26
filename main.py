import pygame, sys, random
from game import Game
import av

pygame.init()

SCREEN_WIDTH = 750
SCREEN_HEIGHT = 700
OFFSET = 50

Grey = (29, 29, 27)
Yellow = (243, 216, 63)

font = pygame.font.Font("Font/monogram.ttf", 40)
minecraft_font_play_again = pygame.font.Font("Font/Minecraft.ttf", 50)
minecraft_font_thanks = pygame.font.Font("Font/Minecraft.ttf", 20)
game_over_surface = font.render("GAME OVER", False, Yellow)
score_text_surface = font.render("SCORE", False, Yellow)
highscore_text_surface = font.render("HIGH  SCORE", False, Yellow)

screen = pygame.display.set_mode((SCREEN_WIDTH + OFFSET, SCREEN_HEIGHT + 2*OFFSET))
pygame.display.set_caption("Galaga")

clock = pygame.time.Clock()

game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, OFFSET, screen)

next_level_rect = pygame.Rect(290, 378, 220, 45)  # button for next level
play_again_rect = pygame.Rect((SCREEN_WIDTH+OFFSET)/2-185, 528, 370, 95)  # button for play again
thanks_rect = pygame.Rect((SCREEN_WIDTH+OFFSET)/2-85, 585, 180, 45)  # thank the player
SHOOT_LASER = pygame.USEREVENT
pygame.time.set_timer(SHOOT_LASER, 300)

MYSTERYSHIP = pygame.USEREVENT + 1
pygame.time.set_timer(MYSTERYSHIP, random.randint(4000, 8000))

while True:
    try:
        #Checking for events
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and game.waiting_for_next_level:  # making button for next level clickable
                if next_level_rect.collidepoint(event.pos):
                    game.start_next_level()

            if event.type == pygame.MOUSEBUTTONDOWN and game.waiting_for_play_again:  # making button for play again clickable
                if play_again_rect.collidepoint(event.pos):
                    game.reset()

            # if game.play_winning_video:
            #     video = av.open("Sounds/winning_video.mp4")
            #     game.play_winning_video = True
            #
            #     for frame in video.decode(video=0):
            #         image = frame.to_ndarray(format="rgb24")
            #         surface = pygame.image.frombuffer(image.tobytes(), (240, 240), "RGB")
            #         screen.blit(surface, (0, 0))
            #         pygame.display.flip()
            #         clock.tick(60)

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and game.run and not game.waiting_for_next_level:
                game.spaceship_group.sprite.shoot()
            if event.type == SHOOT_LASER and game.run and not game.waiting_for_next_level:
                game.alien_shoot_laser()
            if event.type == MYSTERYSHIP and game.run and not game.waiting_for_next_level and not game.waiting_for_play_again:
                game.create_mystery_ship()
                pygame.time.set_timer(MYSTERYSHIP, random.randint(4000, 8000))

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] and game.run == False:
                game.reset()


        #Updating
        if game.run and not game.waiting_for_next_level and not game.waiting_for_play_again:
            game.spaceship_group.update()
            game.move_aliens()
            game.alien_lasers_group.update()
            game.mystery_ship_group.update()
            game.check_for_collisions()
            # game.play_winning_video


        #Drawing
        screen.fill(Grey)

        #UI
        pygame.draw.rect(screen, Yellow, (10, 10, 780, 780), 2, 0, 60, 60, 60, 60)
        pygame.draw.line(screen, Yellow, (25, 730), (775, 730), 3)

        if game.waiting_for_next_level:
            if game.level == 1:
                next_level_surface = font.render("LEVEL 2", False, Yellow)
            elif game.level == 2:
                next_level_surface = font.render("BOSS!!!", False, Yellow)

            pygame.draw.rect(screen, Yellow, next_level_rect, 2)
            screen.blit(next_level_surface, next_level_surface.get_rect(center=next_level_rect.center))


        elif game.waiting_for_play_again:
            play_again_surface = minecraft_font_play_again.render("PLAY AGAIN ?", False, Yellow)
            thanks = minecraft_font_thanks.render("Thanks For Playing ;)", False, Yellow)
            pygame.draw.rect(screen, Yellow, play_again_rect, 2)

            screen.blit(play_again_surface, play_again_surface.get_rect(center=play_again_rect.center))
            screen.blit(thanks, thanks.get_rect(center=thanks_rect.center))

            if game.play_winning_video:
                video = av.open("Sounds/winning_video.mp4")
                game.play_winning_video = False
                stop_video = False

                print("video opened")

                while not stop_video:
                    video.seek(0)
                    for frame in video.decode(video=0):
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                stop_video = True
                                pygame.quit()
                                sys.exit()

                            if event.type == pygame.MOUSEBUTTONDOWN and game.waiting_for_play_again:
                                if play_again_rect.collidepoint(event.pos):
                                    game.reset()
                                    stop_video = True

                        if stop_video:
                            break

                        video_location = ((SCREEN_WIDTH+OFFSET)/2 - 190 , 75)
                        print(video_location)

                        image = frame.to_ndarray(format="rgb24")
                        surface = pygame.image.frombuffer(image.tobytes(), (240, 240), "RGB")
                        surface = pygame.transform.scale(surface, (380, 380))
                        screen.blit(surface, (video_location))
                        pygame.display.flip()
                        clock.tick(60)




        elif game.run:
            level_surface = font.render(f"LEVEL {str(game.level).zfill(2)}", False, Yellow)
            screen.blit(level_surface, (570, 740, 50, 50))

        else:
            screen.blit(game_over_surface, (570, 740, 50, 50))

        x = 50
        for life in range(game.lives):
            screen.blit(game.spaceship_group.sprite.image, (x, 745))
            x += 50

        screen.blit(score_text_surface, (50, 15, 50, 50))
        formatted_score = str(game.score).zfill(5)
        score_surface = font.render(formatted_score, False, Yellow)
        screen.blit(score_surface, (50, 40, 50, 50))
        screen.blit(highscore_text_surface, (550, 15, 50, 50))
        formatted_highscore = str(game.highscore).zfill(5)
        highscore_surface = font.render(formatted_highscore, False, Yellow)
        screen.blit(highscore_surface, (625, 40, 50, 50))

        game.spaceship_group.draw(screen)
        game.spaceship_group.sprite.lasers_group.draw(screen)
        for obstacle in game.obstacles:
            obstacle.blocks_group.draw(screen)
        game.aliens_group.draw(screen)
        game.alien_lasers_group.draw(screen)
        game.mystery_ship_group.draw(screen)


        pygame.display.update()
        clock.tick(80)

    except KeyboardInterrupt:
        print("Stop Success")