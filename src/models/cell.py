import math
import random
from typing import Tuple


class Cell:

    def __init__(
        self,
        x: float,
        y: float,
        mass: float,
        color: Tuple[int, int, int],
        is_bot: bool = False,
    ) -> None:

        self.x = x
        self.y = y
        self.mass = mass
        self.color = color
        self.is_bot = is_bot
        self.target_x = x
        self.target_y = y

    @property
    def radius(self) -> float:
        return math.sqrt(self.mass / math.pi) * 4.0

    @property
    def speed(self) -> float:
        base_speed = 6.5
        return max(1.2, base_speed / (self.mass ** 0.25))

    def move_towards(
        self,
        target_x: float,
        target_y: float,
        world_width: int,
        world_height: int,
    ) -> None:

        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.hypot(dx, dy)

        if distance > 1.0:
            step = min(self.speed, distance)
            self.x += (dx / distance) * step
            self.y += (dy / distance) * step

        self.x = max(self.radius, min(world_width - self.radius, self.x))
        self.y = max(self.radius, min(world_height - self.radius, self.y))

    def update_bot_ai(self, world_width: int, world_height: int) -> None:

        if math.hypot(self.target_x - self.x, self.target_y - self.y) < 30.0:
            self.target_x = random.uniform(50, world_width - 50)
            self.target_y = random.uniform(50, world_height - 50)
        self.move_towards(self.target_x, self.target_y, world_width, world_height)

    def can_eat(self, other: "Cell") -> bool:
        if self.mass <= other.mass * 1.15:
            return False
        distance = math.hypot(self.x - other.x, self.y - other.y)
        return distance < self.radius

    def absorb(self, other: "Cell") -> None:
        self.mass += other.mass
