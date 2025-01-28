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

font1 = pygame.font.Font(None, round(screen_size[1] / 28))
text1 = font1.render("Выберите количество команд", 1, (15, 15, 10))
text1_set_dot = (screen_size[0] // 2 - text1.get_size()[0] // 2, screen_size[1] // 2 - text1.get_size()[1] // 2)

button_text = []
button_text_set_dots = []
font2 = pygame.font.Font(None, round(screen_size[1] / 14))
for group_size in range(7):
    if group_size < 3:
        button_text.append(font2.render(str(group_size + 2) + " команды", 1, (5, 5, 5)))
        button_text_set_dots.append((screen_size[0] * group_size // 3 + screen_size[0] // 6 -
                                     button_text[-1].get_size()[0] // 2, screen_size[1] - text1_set_dot[1] * 3 // 4 -
                                     button_text[-1].get_size()[1] // 2))
    else:
        button_text.append(font2.render(str(group_size + 2) + " команд", 1, (5, 5, 5)))
        group_size -= 3
        button_text_set_dots.append((screen_size[0] * group_size // 4 + screen_size[0] // 8 -
                                     button_text[-1].get_size()[0] // 2, screen_size[1] - text1_set_dot[1] // 4 -
                                     button_text[-1].get_size()[1] // 2))

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
            font1 = pygame.font.Font(None, round(screen_size[1] / 28))
            text1 = font1.render("Выберите количество команд", 1, (15, 15, 10))
            text1_set_dot = (
            screen_size[0] // 2 - text1.get_size()[0] // 2, screen_size[1] // 2 - text1.get_size()[1] // 2)
            button_text = []
            button_text_set_dots = []
            font2 = pygame.font.Font(None, round(screen_size[1] / 14))
            for group_size in range(7):
                button_text.append(font2.render(str(group_size + 2) + " команд", 1, (5, 5, 5)))
                if group_size < 4:
                    button_text_set_dots.append((screen_size[0] * group_size // 4 + screen_size[0] // 8 -
                                                 button_text[-1].get_size()[0] // 2,
                                                 screen_size[1] - text1_set_dot[1] * 3 // 4 -
                                                 button_text[-1].get_size()[1] // 2))
                else:
                    group_size -= 4
                    button_text_set_dots.append((screen_size[0] * group_size // 3 + screen_size[0] // 6 -
                                                 button_text[-1].get_size()[0] // 2,
                                                 screen_size[1] - text1_set_dot[1] // 4 -
                                                 button_text[-1].get_size()[1] // 2))
    if game_running:
        pass
    else:
        window.blit(menu_image, (0, 0))
        window.blit(text1, text1_set_dot)
        for button_number in range(len(button_text)):
            window.blit(button_text[button_number], button_text_set_dots[button_number])
    pygame.display.flip()
pygame.quit()