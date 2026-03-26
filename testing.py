import pygame
import cv2

pygame.init()
screen = pygame.display.set_mode((240, 240))
clock = pygame.time.Clock()

cap = cv2.VideoCapture("Sounds/winning_video.mp4")   # or absolute path
fps = 60

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ok, frame = cap.read()
    if not ok:
        break  # video ended

    # OpenCV gives BGR, pygame expects RGB
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    h, w = frame.shape[:2]
    surf = pygame.image.frombytes(frame.tobytes(), (w, h), "RGB")

    # optional: fit video into your existing screen
    surf = pygame.transform.scale(surf, screen.get_size())

    # draw whatever background / game scene you want first
    screen.fill((0, 0, 0))

    # then draw video into the existing pygame screen
    screen.blit(surf, (0, 0))

    pygame.display.flip()
    clock.tick(fps)

cap.release()
pygame.quit()