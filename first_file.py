import pygame

pygame.init()
screen_size = (500, 300)
pygame.display.set_caption("")
window = pygame.display.set_mode(screen_size, pygame.RESIZABLE)
clock = pygame.time.Clock()
FPS = 60
running = True

menu_image_real = pygame.image.load("main_menu.png")
game_running = False
menu_image = pygame.transform.scale(menu_image_real, screen_size)

while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                pass
        if event.type == pygame.VIDEORESIZE:
            screen_size = (max(500, event.size[0]), max(300, event.size[1]))
            window = pygame.display.set_mode(screen_size, pygame.RESIZABLE)
            menu_image = pygame.transform.scale(menu_image_real, screen_size)
    if game_running:
        pass
    else:
        window.blit(menu_image, (0, 0))
    pygame.display.flip()
pygame.quit()