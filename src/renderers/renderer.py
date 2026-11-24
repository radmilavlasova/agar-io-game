import pygame
from src.models.cell import Cell
from src.models.world import World


class Renderer:

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.bg_color = (18, 18, 22)
        self.grid_color = (35, 35, 42)
        self.border_color = (220, 60, 60)
        self.font = pygame.font.SysFont("Arial", 24, bold=True)
        self.big_font = pygame.font.SysFont("Arial", 48, bold=True)

    def draw(self, world: World) -> None:

        self.screen.fill(self.bg_color)

        offset_x = self.width / 2 - world.player.x
        offset_y = self.height / 2 - world.player.y

        self._draw_grid(offset_x, offset_y, world.width, world.height)

        for food in world.foods:
            self._draw_cell(food, offset_x, offset_y)

        active_cells = sorted(
            world.bots + ([world.player] if not world.game_over else []),
            key=lambda c: c.mass,
        )
        for cell in active_cells:
            self._draw_cell(cell, offset_x, offset_y, draw_border=True)

        self._draw_hud(world)

        if world.game_over:
            self._draw_game_over()

        pygame.display.flip()

    def _draw_grid(
        self, offset_x: float, offset_y: float, world_w: int, world_h: int
    ) -> None:
        step = 50
        start_x = int(offset_x % step)
        start_y = int(offset_y % step)

        for x in range(start_x, self.width, step):
            pygame.draw.line(self.screen, self.grid_color, (x, 0), (x, self.height))
        for y in range(start_y, self.height, step):
            pygame.draw.line(self.screen, self.grid_color, (0, y), (self.width, y))

        border_rect = pygame.Rect(offset_x, offset_y, world_w, world_h)
        pygame.draw.rect(self.screen, self.border_color, border_rect, width=4)

    def _draw_cell(
        self,
        cell: Cell,
        offset_x: float,
        offset_y: float,
        draw_border: bool = False,
    ) -> None:
        screen_x = int(cell.x + offset_x)
        screen_y = int(cell.y + offset_y)
        radius = max(3, int(cell.radius))

        pygame.draw.circle(self.screen, cell.color, (screen_x, screen_y), radius)
        if draw_border:
            outline = tuple(max(0, c - 50) for c in cell.color)
            pygame.draw.circle(
                self.screen, outline, (screen_x, screen_y), radius, width=3
            )

    def _draw_hud(self, world: World) -> None:
        score_text = self.font.render(
            f"Масса: {int(world.player.mass)}", True, (240, 240, 240)
        )
        self.screen.blit(score_text, (20, 20))

    def _draw_game_over(self) -> None:
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))

        title = self.big_font.render("ВЫ БЫЛИ ПОГЛОЩЕНЫ", True, (255, 80, 80))
        hint = self.font.render(
            "Нажмите R для перезапуска или ESC для выхода", True, (255, 255, 255)
        )

        self.screen.blit(
            title, title.get_rect(center=(self.width // 2, self.height // 2 - 30))
        )
        self.screen.blit(
            hint, hint.get_rect(center=(self.width // 2, self.height // 2 + 25))
        )
