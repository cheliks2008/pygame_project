import pygame

pygame.init()
screen_size = (201, 201)
pygame.display.set_caption("")
window = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
FPS = 60
runing = True
while runing:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runing = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                pass
    pygame.display.flip()
pygame.quit()