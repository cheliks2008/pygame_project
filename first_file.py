import pygame

pygame.init()
screen_size = (501, 301)
pygame.display.set_caption("")
window = pygame.display.set_mode(screen_size, pygame.RESIZABLE)
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
        if event.type == pygame.VIDEORESIZE:
            screen_size = (max(500, event.size[0]), max(300, event.size[1]))
            window = pygame.display.set_mode(screen_size, pygame.RESIZABLE)
    pygame.display.flip()
pygame.quit()