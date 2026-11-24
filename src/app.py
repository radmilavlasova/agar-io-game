import pygame
from src.models.world import World
from src.renderers.renderer import Renderer


class App:

    def __init__(self, width: int = 1000, height: int = 700, fps: int = 60) -> None:

        pygame.init()
        pygame.display.set_caption("Agar.io — Лабораторная работа №3")
        self.width = width
        self.height = height
        self.fps = fps
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.world = World()
        self.renderer = Renderer(self.screen)
        self.running = True

    def run(self) -> None:
        while self.running:
            self._handle_events()
            self._update()
            self.renderer.draw(self.world)
            self.clock.tick(self.fps)
        pygame.quit()

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r and self.world.game_over:
                    self.world.reset()

    def _update(self) -> None:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        target_world_x = self.world.player.x + (mouse_x - self.width / 2)
        target_world_y = self.world.player.y + (mouse_y - self.height / 2)
        self.world.update(target_world_x, target_world_y)
