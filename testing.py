import av
import pygame

pygame.init()

video = av.open("Sounds/winning_video.mp4")
stream = video.streams.video[0]

width = stream.codec_context.width
height = stream.codec_context.height

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

running = True

for frame in video.decode(video=0):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not running:
        break

    image = frame.to_ndarray(format="rgb24")
    surface = pygame.image.frombuffer(image.tobytes(), (width, height), "RGB")

    screen.blit(surface, (0, 0))
    pygame.display.flip()
    clock.tick(60)

video.close()
pygame.quit()