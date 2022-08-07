import os
import sys

import yaml
from yaml.loader import SafeLoader

from tkinter import filedialog
import pygame


class TextButton(object):
    def __init__(self, pos, size, text, screen, element_data=None, hidden=False, shift_left=False):
        self.pos = pos
        self.hidden = hidden
        self.size = size
        self.element_data = element_data
        self.selected = False
        self.restrictions = [None, None, None, None]
        self.shift_left = shift_left
        self.text = text
        self.screen = screen

    def update_text(self, text):
        self.text = text

    def handle(self, mouse_data):
        if not self.hidden:
            collide_test = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
            clicked = False
            if collide_test.collidepoint(mouse_data.pos):
                # TODO: add coloured text
                if mouse_data.left_click:
                    clicked = True
            else:
                # TODO: add white text
                pass
            return clicked


class Mouse:
    def __init__(self):
        self.pos = [0, 0]
        self.last_pos = [0, 0]
        self.left_click = False
        self.left_clicking = False
        self.right_click = False
        self.right_clicking = False
        self.middle_click = False
        self.middle_clicking = False

    def update(self):
        mx, my = pygame.mouse.get_pos()
        self.last_pos = self.pos.copy()
        self.pos = [mx, my]
        self.left_click = False
        self.right_click = False
        self.middle_click = False

    def reset(self):
        self.pos = [0, 0]
        self.last_pos = [0, 0]
        self.left_click = False
        self.left_clicking = False
        self.right_click = False
        self.right_clicking = False
        self.middle_click = False
        self.middle_clicking = False


class RunHandler:

    def __init__(self):

        self.project_directory = os.getcwd()
        self.frames_firectory = os.path.join(self.project_directory, 'frames')
        self.animation_folder = None

        with open(os.path.join(self.project_directory, 'config.yaml')) as file:
            self.configuration_params = list(yaml.load_all(file, Loader=SafeLoader))[0]

        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((self.configuration_params['window_x'],
                                               self.configuration_params['window_y']))

        self.mouse = Mouse()
        pygame.display.set_caption("Animation tool")

    def load_animation_folder(self):
        return filedialog.askdirectory(initialdir=self.frames_firectory, title='Load Animation Folder')

    def run(self):
        while True:
            self.screen.fill((0, 0, 0))  # Fill the screen with the RGB color in brackets
            self.clock.tick(self.configuration_params['fps'])  # FPS
            self.mouse.update()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.mouse.left_click = True
                        self.mouse.left_clicking = True
                    if event.button == 2:
                        self.mouse.middle_click = True
                        self.mouse.middle_clicking = True
                    if event.button == 3:
                        self.mouse.right_click = True
                        self.mouse.right_clicking = True

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.mouse.left_clicking = False
                    if event.button == 2:
                        self.mouse.middle_clicking = False
                    if event.button == 3:
                        self.mouse.right_clicking = False
            pygame.display.update()


if __name__ == '__main__':
    run_handler = RunHandler()
    run_handler.run()
