import pygame

pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    raise Exception("No controller found")

controller = pygame.joystick.Joystick(0)
controller.init()

print("Connected:", controller.get_name())

def get_controller_input():
    for event in pygame.event.get():
        pass

    axes = [controller.get_axis(i) for i in range(controller.get_numaxes())]
    buttons = [controller.get_button(i) for i in range(controller.get_numbuttons())]

    return axes, buttons
