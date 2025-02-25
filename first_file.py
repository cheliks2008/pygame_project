import pygame

pygame.init()
screen_size = (500, 300)
pygame.display.set_caption("")
window = pygame.display.set_mode(screen_size, pygame.RESIZABLE)
clock = pygame.time.Clock()
FPS = 60
running = True
game_running = False
level_not_running = True
press_on_button = ()
clicked_button = ()
stage = 0
rest_of_time = 0
command = 0
account = []
number_of_commands = 0
main_circuit = ""
levels = set()
levels_score = {}
level = []
command1_text = []
wire = {"I": [pygame.image.load("wire_I.png").subsurface(pygame.Rect(i * 200, 0, 200, 200)) for i in range(4)],
        "L": [pygame.image.load("wire_L.png").subsurface(pygame.Rect(i * 200, 0, 200, 200)) for i in range(4)],
        "T": [pygame.image.load("wire_T.png").subsurface(pygame.Rect(i * 200, 0, 200, 200)) for i in range(4)],
        "X": [pygame.image.load("wire_X.png").subsurface(pygame.Rect(i * 200, 0, 200, 200)) for i in range(4)]}
Resistor = [pygame.image.load("resistor.png").subsurface(pygame.Rect(i * 200, 0, 200, 200)) for i in range(4)]
Meter = [pygame.image.load("meter.png").subsurface(pygame.Rect(i * 200, 0, 200, 200)) for i in range(4)]

group1 = pygame.sprite.Group()
group2 = pygame.sprite.Group()
group3 = pygame.sprite.Group()
group4 = pygame.sprite.Group()
group5 = pygame.sprite.Group()


class ElectricalElement(pygame.sprite.Sprite):
    def __init__(self, images, angle, h, w, center_x, center_y, *groups):
        super().__init__(*groups)
        self.hw_xy = (h, w, center_x, center_y)
        self.images = [pygame.transform.rotate(images[i], angle) for i in range(4)]
        size = (screen_size[0] * self.hw_xy[0], screen_size[1] * self.hw_xy[1])
        self.sized_images = [pygame.transform.scale(self.images[0], size), pygame.transform.scale(self.images[1], size),
                             pygame.transform.scale(self.images[2], size), pygame.transform.scale(self.images[3], size)]
        self.image = self.sized_images[0]
        self.rect = self.image.get_rect()
        self.rect.center = (int(screen_size[0] * self.hw_xy[2]), int(screen_size[1] * self.hw_xy[3]))
        self.current_conduction = False

    def update(self, *args):
        global clicked_button
        if args[0]:
            if self.current_conduction:
                self.image = self.sized_images[stage]
            else:
                self.current_conduction = True
        else:
            size = (screen_size[0] * self.hw_xy[0], screen_size[1] * self.hw_xy[1])
            self.sized_images = [pygame.transform.scale(self.images[0], size), pygame.transform.scale(self.images[1],
                                                                                                      size),
                                 pygame.transform.scale(self.images[2], size), pygame.transform.scale(self.images[3],
                                                                                                      size)]
            self.image = self.sized_images[stage]
            self.rect = self.image.get_rect()
            self.rect.center = (int(screen_size[0] * self.hw_xy[2]), int(screen_size[1] * self.hw_xy[3]))


class Button(pygame.sprite.Sprite):
    def __init__(self, image, image_ready, image_pressed, h, w, center_x, center_y, index, *groups):
        super().__init__(*groups)
        self.hw_xy = (h, w, center_x, center_y)
        self.images = [pygame.image.load(image), pygame.image.load(image_ready), pygame.image.load(image_pressed)]
        size = (screen_size[0] * self.hw_xy[0], screen_size[1] * self.hw_xy[1])
        self.sized_images = [pygame.transform.scale(self.images[0], size), pygame.transform.scale(self.images[1], size),
                             pygame.transform.scale(self.images[2], size)]
        self.image = self.sized_images[0]
        self.rect = self.image.get_rect()
        self.rect.center = (int(screen_size[0] * self.hw_xy[2]), int(screen_size[1] * self.hw_xy[3]))
        self.index = index
        self.mouse_on = False

    def update(self, *args):
        global press_on_button, clicked_button
        if args[0]:
            if self.mouse_on:
                self.mouse_on = False
                self.image = self.sized_images[0]
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                if args[1]:
                    if press_on_button:
                        if self.index == press_on_button:
                            clicked_button = self.index
                        press_on_button = ()
                    else:
                        press_on_button = self.index
                self.mouse_on = True
                if pygame.mouse.get_pressed()[0]:
                    self.image = self.sized_images[2]
                else:
                    self.image = self.sized_images[1]
        else:
            size = (screen_size[0] * self.hw_xy[0], screen_size[1] * self.hw_xy[1])
            self.sized_images = [pygame.transform.scale(self.images[0], size), pygame.transform.scale(self.images[1],
                                                                                                      size),
                                 pygame.transform.scale(self.images[2], size)]
            if self.mouse_on:
                if pygame.mouse.get_pressed()[0]:
                    self.image = self.sized_images[2]
                else:
                    self.image = self.sized_images[1]
            else:
                self.image = self.sized_images[0]
            self.rect = self.image.get_rect()
            self.rect.center = (int(screen_size[0] * self.hw_xy[2]), int(screen_size[1] * self.hw_xy[3]))


class NotButton(Button):
    def __init__(self, image, image_ready, h, w, center_x, center_y, index, *groups):
        super().__init__(image, image_ready, image_ready, h, w, center_x, center_y, index, *groups)

    def update(self, *args):
        if args[0]:
            if args[1] == self.index:
                self.mouse_on = True
                self.image = self.sized_images[1]
            else:
                self.mouse_on = False
        else:
            size = (screen_size[0] * self.hw_xy[0], screen_size[1] * self.hw_xy[1])
            self.sized_images = [pygame.transform.scale(self.images[0], size), pygame.transform.scale(self.images[1],
                                                                                                      size)]
            if self.mouse_on:
                self.image = self.sized_images[1]
            else:
                self.image = self.sized_images[0]
            self.rect = self.image.get_rect()
            self.rect.center = (int(screen_size[0] * self.hw_xy[2]), int(screen_size[1] * self.hw_xy[3]))


menu_image_real = pygame.image.load("main_menu.png")
menu_image = pygame.transform.scale(menu_image_real, screen_size)

font1 = pygame.font.Font(None, round(screen_size[1] / 28))
text1 = font1.render("Выберите количество команд", 1, (15, 15, 10))
text1_set_dot = (screen_size[0] // 2 - text1.get_size()[0] // 2, screen_size[1] // 2 - text1.get_size()[1] // 2)

button_text = []
button_text_set_dots = []
font2 = pygame.font.Font(None, round(screen_size[1] / 14))
button_images = ("r", "o", "y", "g", "lb", "b", "p", "grey", "back")
for group_size in range(7):
    if group_size < 3:
        Button(f"button_{button_images[group_size + 1]}.png", f"button_{button_images[group_size + 1]}_ready.png",
               f"button_{button_images[group_size + 1]}_pressed.png", 3 / 12, text1_set_dot[1] / screen_size[1] / 2,
               1 / 6 + group_size / 3, (screen_size[1] - text1_set_dot[1] * 0.75) / screen_size[1],
               (0, group_size + 1), group1)
        button_text.append(font2.render(str(group_size + 2) + " команды", 1, (5, 5, 5)))
        button_text_set_dots.append((screen_size[0] * group_size // 3 + screen_size[0] // 6 -
                                     button_text[-1].get_size()[0] // 2, screen_size[1] - text1_set_dot[1] * 3 // 4 -
                                     button_text[-1].get_size()[1] // 2))
    else:
        Button(f"button_{button_images[group_size + 1]}.png", f"button_{button_images[group_size + 1]}_ready.png",
               f"button_{button_images[group_size + 1]}_pressed.png", 0.20, text1_set_dot[1] / screen_size[1] / 2,
               0.125 + (group_size - 3) / 4, (screen_size[1] - text1_set_dot[1] * 0.25) / screen_size[1],
               (0, group_size + 1), group1)
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
                if game_running:
                    if level_not_running:
                        group3.update(True, True)
                    else:
                        group5.update(True, True)
                else:
                    group1.update(True, True)
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == pygame.BUTTON_LEFT:
                if game_running:
                    if level_not_running:
                        group3.update(True, True)
                        if clicked_button:
                            if clicked_button in levels:
                                levels.remove(clicked_button)
                                level_not_running = False
                                with open(clicked_button + ".txt", mode="rt", encoding="utf-8") as file:
                                    level.append(file.readline().split("\n")[0])
                                    font5 = pygame.font.Font(None, round(screen_size[1] / 14))
                                    text5 = font5.render(level[0], 1, (15, 15, 10))
                                    text5_set_dot = (screen_size[0] / 2.5 - text5.get_size()[0] / 2,
                                                     screen_size[1] / 10 - text5.get_size()[1] / 2)
                                    level.append(file.readline().split("\n")[0])
                                    level.append(clicked_button)
                                    level_circuit_size = file.readline().split("\n")[0].split("x")
                                    level.append(int(file.readline().split("\n")[0]))
                                    level_circuit_size = (int(level_circuit_size[0]), int(level_circuit_size[1]))
                                    level_element_size = (1 / level_circuit_size[0], 4 / 5 / level_circuit_size[1])
                                    Button("button_enter.png", "button_enter_ready.png", "button_enter_pressed.png",
                                           0.2, 0.2, 0.9, 0.1, 42, group5)
                                    font4 = pygame.font.Font(None, round(screen_size[1] / 28))
                                    met_and_res_text_original = []
                                    met_and_res_text = []
                                    met_and_res_text_set_dots = []
                                    for line in range(level_circuit_size[1]):
                                        files_line = file.readline().split("\n")[0].split()
                                        for element in range(level_circuit_size[0]):
                                            if files_line[element][0] == "s":
                                                continue
                                            elif files_line[element][0] in "LIXT":
                                                ElectricalElement(wire[files_line[element][0]], 90 * int(files_line
                                                                                                         [element][1]),
                                                                  level_element_size[0], level_element_size[1],
                                                                  level_element_size[0] * element + 0.5 *
                                                                  level_element_size[0], level_element_size[1] * line +
                                                                  0.5 * level_element_size[1] + 1 / 5, group4)
                                            else:
                                                if files_line[element][0] == "M":
                                                    ElectricalElement(Meter, 90 * int(files_line[element][1]),
                                                                      level_element_size[0], level_element_size[1],
                                                                      level_element_size[0] * element + 0.5 *
                                                                      level_element_size[0], level_element_size[1] *
                                                                      line + 0.5 * level_element_size[1] + 1 / 5,
                                                                      group4)
                                                else:
                                                    ElectricalElement(Resistor, 90 * int(files_line[element][1]),
                                                                      level_element_size[0], level_element_size[1],
                                                                      level_element_size[0] * element + 0.5 *
                                                                      level_element_size[0], level_element_size[1] *
                                                                      line + 0.5 * level_element_size[1] + 1 / 5,
                                                                      group4)
                                                met_and_res_text_original.append((files_line[element][2:], element,
                                                                                  line))
                                                met_and_res_text.append(font4.render(files_line[element][2:], 1, (5, 5,
                                                                                                                  5)))
                                                met_and_res_text_set_dots.append(((element + 0.5) *
                                                                                  level_element_size[0] * screen_size[0]
                                                                                  - met_and_res_text[-1].get_size()[0]
                                                                                  // 2, ((line + 0.5) *
                                                                                         level_element_size[1] + 0.2) *
                                                                                  screen_size[1] - met_and_res_text[-1].
                                                                                  get_size()[1] // 2))
                                clicked_button = ()
                    else:
                        group5.update(True, True)
                        if clicked_button:
                            if len(level) == 4:
                                level = level[1:]
                                text5 = font5.render(level[0], 1, (15, 15, 10))
                                text5_set_dot = (screen_size[0] / 2.5 - text5.get_size()[0] / 2,
                                                 screen_size[1] / 10 - text5.get_size()[1] / 2)
                                command = 80
                                clicked_button = ()
                            else:
                                if command:
                                    command = 0
                                    stage = 0
                                    rest_of_time = 0
                                    side = 1 / number_of_commands
                                    command1_text = []
                                    command1_text_set_dots = []
                                    font2 = pygame.font.Font(None, round(screen_size[1] / 20))
                                    for button_number in range(number_of_commands):
                                        Button(f"button_{button_images[button_number]}.png",
                                               f"button_{button_images[button_number]}_ready.png",
                                               f"button_{button_images[button_number]}_pressed.png", side, 4 / 5, side *
                                               button_number + 0.5 * side, 0.6, button_number, group5)
                                        command1_text.append(font2.render(str(button_number + 1) + " команда", 1, (5, 5,
                                                                                                                   5)))
                                        command1_text_set_dots.append(((0.5 + button_number) * screen_size[0] /
                                                                       number_of_commands - command1_text[-1].get_size()
                                                                       [0] / 2, screen_size[1] * 0.6 -
                                                                       command1_text[-1].get_size()[1] / 2))
                                else:
                                    command1_text = []
                                    group5.empty()
                                    group4.empty()
                                    if clicked_button != 42:
                                        levels_score[level[1]] = (clicked_button, level[-1])
                                        account[clicked_button] += level[-1]
                                    else:
                                        levels_score[level[1]] = (-1, level[-1])
                                    level_not_running = True
                                    level = []
                                    clicked_button = ()
                                    if main_circuit[:-4] in levels:
                                        clicked_button = main_circuit[:-4]
                                    else:
                                        level_not_running = False
                                        NotButton(f"button_{button_images[account.index(max(account))]}.png",
                                                  f"button_{button_images[account.index(max(account))]}_ready.png",
                                                  1, 1, 0.5, 0.5, group5)
                                        font5 = pygame.font.Font(None, round(screen_size[1] / 5))
                                        text5 = font5.render(f"Побеждает команда {account.index(max(account)) + 1}", 1,
                                                             (15, 15, 10))
                                        text5_set_dot = (screen_size[0] / 2 - text5.get_size()[0] / 2,
                                                         screen_size[1] / 2 - text5.get_size()[1] / 2)
                else:
                    group1.update(True, True)
                    if clicked_button:
                        group1.empty()
                        game_running = True
                        number_of_commands = 1 + clicked_button[1]
                        side = 1 / number_of_commands
                        command_text = []
                        command_text_set_dots = []
                        font2 = pygame.font.Font(None, round(screen_size[1] / 20))
                        for button_number in range(clicked_button[1] + 1):
                            NotButton(f"button_{button_images[button_number]}.png",
                                      f"button_{button_images[button_number]}_ready.png", side, 1 / 5, side *
                                      button_number + 0.5 * side, 0.1, button_number, group2)
                            command_text.append(font2.render(str(button_number + 1) + " команда", 1, (5, 5, 5)))
                            command_text_set_dots.append(((side / 2 + side * button_number) * screen_size[0] -
                                                          command_text[-1].get_size()[0] / 2, screen_size[1] / 10 -
                                                          command_text[-1].get_size()[1] / 2))
                        group2.update(True, 0)
                        account = [0 for i in range(clicked_button[1] + 1)]
                        if clicked_button[1] in [7, 3, 5]:
                            main_circuit = "electronic_circuit1.txt"
                        elif clicked_button[1] in [4, 2]:
                            main_circuit = "electronic_circuit2.txt"
                        else:
                            main_circuit = "electronic_circuit3.txt"
                        with open(main_circuit, mode="rt", encoding="utf-8") as file:
                            file.readline()
                            file.readline()
                            circuit_size = file.readline().split("\n")[0].split("x")
                            file.readline()
                            circuit_size = (int(circuit_size[0]), int(circuit_size[1]))
                            element_size = (1 / circuit_size[0], 4 / 5 / circuit_size[1])
                            font3 = pygame.font.Font(None, round(screen_size[1] / 20))
                            meter_text_original = []
                            meter_text = []
                            meter_text_set_dots = []
                            font4 = pygame.font.Font(None, round(screen_size[1] / 28))
                            resistor_text_original = []
                            resistor_text = []
                            resistor_text_set_dots = []
                            for line in range(circuit_size[1]):
                                files_line = file.readline().split("\n")[0].split()
                                for element in range(circuit_size[0]):
                                    if files_line[element][0] == "s":
                                        continue
                                    elif files_line[element][0] in "LIXT":
                                        ElectricalElement(wire[files_line[element][0]], 90 *
                                                          int(files_line[element][1]), element_size[0], element_size[1],
                                                          element_size[0] * element + 0.5 * element_size[0],
                                                          element_size[1] * line + 0.5 * element_size[1] + 1 / 5,
                                                          group1)
                                    elif files_line[element][0] == "M":
                                        ElectricalElement(Meter, 90 * int(files_line[element][1]), element_size[0],
                                                          element_size[1], element_size[0] * element + 0.5 *
                                                          element_size[0], element_size[1] * line + 0.5 *
                                                          element_size[1] + 1 / 5, group1)
                                        meter_text_original.append((files_line[element][2:], element, line))
                                        meter_text.append(font3.render(files_line[element][2:], 1, (5, 5, 5)))
                                        meter_text_set_dots.append(((element + 0.5) * element_size[0] * screen_size[0] -
                                                                    meter_text[-1].get_size()[0] // 2,
                                                                    ((line + 0.5) * element_size[1] + 0.2) *
                                                                    screen_size[1] - meter_text[-1].get_size()[1] // 2))
                                    else:
                                        button_cont = Button("button_resistor.png", "button_resistor_ready.png",
                                                             "button_resistor_pressed.png", element_size[0],
                                                             element_size[1], element_size[0] * element + 0.5 *
                                                             element_size[0], element_size[1] * line + 0.5 *
                                                             element_size[1] + 1 / 5, "B" + files_line[element][2:5],
                                                             group3)
                                        if int(files_line[element][1]):
                                            button_cont.images = [pygame.transform.rotate(button_cont.images[0], 90),
                                                                  pygame.transform.rotate(button_cont.images[1], 90),
                                                                  pygame.transform.rotate(button_cont.images[2], 90)]
                                            button_cont.update(False)
                                        resistor_text_original.append((files_line[element][2:5] + " " +
                                                                       files_line[element][5:], element, line))
                                        resistor_text.append(font4.render(resistor_text_original[-1][0], 1, (5, 5, 5)))
                                        resistor_text_set_dots.append(((element + 0.5) * element_size[0] *
                                                                       screen_size[0] - resistor_text[-1].get_size()[0]
                                                                       // 2, ((line + 0.5) * element_size[1] + 0.2) *
                                                                       screen_size[1] - resistor_text[-1].get_size()[1]
                                                                       // 2))
                                        levels.add("B" + files_line[element][2:5])
                                        levels_score["B" + files_line[element][2:5]] = -1
                                levels.add(main_circuit[:-4])
                                levels_score[main_circuit[:-4]] = -1
                        clicked_button = ()
        if event.type == pygame.MOUSEMOTION:
            if game_running:
                if level_not_running:
                    group3.update(True, False)
                else:
                    group5.update(True, False)
            else:
                group1.update(True, False)
        if event.type == pygame.VIDEORESIZE:
            screen_size = (max(500, event.size[0]), max(300, event.size[1]))
            window = pygame.display.set_mode(screen_size, pygame.RESIZABLE)
            menu_image = pygame.transform.scale(menu_image_real, screen_size)
            if game_running:
                if level_not_running:
                    group2.update(False)
                    group1.update(False)
                    group3.update(False)
                    font3 = pygame.font.Font(None, round(screen_size[1] / 20))
                    meter_text = []
                    meter_text_set_dots = []
                    font4 = pygame.font.Font(None, round(screen_size[1] / 28))
                    resistor_text = []
                    resistor_text_set_dots = []
                    for meter_place in meter_text_original:
                        meter_text.append(font3.render(meter_place[0], 1, (5, 5, 5)))
                        meter_text_set_dots.append(((meter_place[1] + 0.5) * element_size[0] * screen_size[0] -
                                                    meter_text[-1].get_size()[0] // 2,
                                                    ((meter_place[2] + 0.5) * element_size[1] + 0.2) *
                                                    screen_size[1] - meter_text[-1].get_size()[1] // 2))
                    for resistor_place in resistor_text_original:
                        resistor_text.append(font4.render(resistor_place[0], 1, (5, 5, 5)))
                        resistor_text_set_dots.append(((resistor_place[1] + 0.5) * element_size[0] *
                                                       screen_size[0] - resistor_text[-1].get_size()[0]
                                                       // 2, ((resistor_place[2] + 0.5) * element_size[1] + 0.2) *
                                                       screen_size[1] - resistor_text[-1].get_size()[1]
                                                       // 2))
                    command_text = []
                    command_text_set_dots = []
                    font2 = pygame.font.Font(None, round(screen_size[1] / 20))
                    for button_number in range(number_of_commands):
                        command_text.append(font2.render(str(button_number + 1) + " команда", 1, (5, 5, 5)))
                        command_text_set_dots.append(((0.5 + button_number) * screen_size[0] / number_of_commands -
                                                      command_text[-1].get_size()[0] / 2, screen_size[1] / 10 -
                                                      command_text[-1].get_size()[1] / 2))
                else:
                    group4.update(False)
                    group5.update(False)
                    if level:
                        font5 = pygame.font.Font(None, round(screen_size[1] / 14))
                        text5 = font5.render(level[0], 1, (15, 15, 10))
                        text5_set_dot = (screen_size[0] / 2.5 - text5.get_size()[0] / 2,
                                         screen_size[1] / 10 - text5.get_size()[1] / 2)
                    else:
                        font5 = pygame.font.Font(None, round(screen_size[1] / 5))
                        text5 = font5.render(f"Побеждает команда {account.index(max(account)) + 1}", 1,
                                             (15, 15, 10))
                        text5_set_dot = (screen_size[0] / 2 - text5.get_size()[0] / 2,
                                         screen_size[1] / 2 - text5.get_size()[1] / 2)
                    font4 = pygame.font.Font(None, round(screen_size[1] / 28))
                    met_and_res_text = []
                    met_and_res_text_set_dots = []
                    for met_and_res_place in met_and_res_text_original:
                        met_and_res_text.append(font4.render(met_and_res_place[0], 1, (5, 5, 5)))
                        met_and_res_text_set_dots.append(((met_and_res_place[1] + 0.5) *
                                                          level_element_size[0] * screen_size[0]
                                                          - met_and_res_text[-1].get_size()[0]
                                                          // 2, ((met_and_res_place[2] + 0.5) *
                                                                 level_element_size[1] + 0.2) *
                                                          screen_size[1] - met_and_res_text[-1].
                                                          get_size()[1] // 2))
                    if command1_text:
                        command1_text = []
                        command1_text_set_dots = []
                        font2 = pygame.font.Font(None, round(screen_size[1] / 20))
                        for button_number in range(number_of_commands):
                            command1_text.append(font2.render(str(button_number + 1) + " команда", 1, (5, 5, 5)))
                            command1_text_set_dots.append(((0.5 + button_number) * screen_size[0] / number_of_commands -
                                                           command1_text[-1].get_size()[0] / 2, screen_size[1] * 0.6 -
                                                           command1_text[-1].get_size()[1] / 2))
            else:
                font1 = pygame.font.Font(None, round(screen_size[1] / 28))
                text1 = font1.render("Выберите количество команд", 1, (15, 15, 10))
                text1_set_dot = (screen_size[0] // 2 - text1.get_size()[0] // 2, screen_size[1] // 2 -
                                 text1.get_size()[1] // 2)
                button_text = []
                button_text_set_dots = []
                font2 = pygame.font.Font(None, round(screen_size[1] / 14))
                group1.update(False)
                for group_size in range(7):
                    if group_size < 3:
                        button_text.append(font2.render(str(group_size + 2) + " команды", 1, (5, 5, 5)))
                        button_text_set_dots.append((screen_size[0] * group_size // 3 + screen_size[0] // 6 -
                                                     button_text[-1].get_size()[0] // 2,
                                                     screen_size[1] - text1_set_dot[1] * 3 // 4 -
                                                     button_text[-1].get_size()[1] // 2))
                    else:
                        button_text.append(font2.render(str(group_size + 2) + " команд", 1, (5, 5, 5)))
                        group_size -= 3
                        button_text_set_dots.append((screen_size[0] * group_size // 4 + screen_size[0] // 8 -
                                                     button_text[-1].get_size()[0] // 2,
                                                     screen_size[1] - text1_set_dot[1] // 4 -
                                                     button_text[-1].get_size()[1] // 2))
    if game_running:
        window.blit(menu_image, (0, 0))
        if level_not_running:
            group2.draw(window)
            group1.draw(window)
            group3.draw(window)
            for button_number in range(number_of_commands):
                window.blit(command_text[button_number], command_text_set_dots[button_number])
            for resistor_number in range(len(resistor_text)):
                window.blit(resistor_text[resistor_number], resistor_text_set_dots[resistor_number])
            for meter_number in range(len(meter_text)):
                window.blit(meter_text[meter_number], meter_text_set_dots[meter_number])
        else:
            if level:
                if command:
                    rest_of_time += clock.get_time()
                    if rest_of_time > command:
                        rest_of_time = rest_of_time % command
                        stage = stage % 3 + 1
                        group4.update(True)
                group4.draw(window)
                window.blit(text5, text5_set_dot)
                for met_and_res_number in range(len(met_and_res_text)):
                    window.blit(met_and_res_text[met_and_res_number], met_and_res_text_set_dots[met_and_res_number])
                group5.draw(window)
                if command1_text:
                    for button_number in range(number_of_commands):
                        window.blit(command1_text[button_number], command1_text_set_dots[button_number])
            else:
                group5.draw(window)
                window.blit(text5, text5_set_dot)
    else:
        window.blit(menu_image, (0, 0))
        group1.draw(window)
        window.blit(text1, text1_set_dot)
        for button_number in range(len(button_text)):
            window.blit(button_text[button_number], button_text_set_dots[button_number])
    pygame.display.flip()
pygame.quit()
