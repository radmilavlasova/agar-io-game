import random
from typing import List, Tuple
from src.models.cell import Cell


FOOD_COLORS: List[Tuple[int, int, int]] = [
    (255, 87, 87),
    (87, 255, 132),
    (87, 179, 255),
    (255, 224, 87),
    (214, 87, 255),
]


class World:

    def __init__(
        self,
        width: int = 2000,
        height: int = 2000,
        food_count: int = 250,
        bot_count: int = 12,
    ) -> None:

        self.width = width
        self.height = height
        self.food_count = food_count
        self.bot_count = bot_count
        self.player: Cell
        self.foods: List[Cell] = []
        self.bots: List[Cell] = []
        self.game_over = False
        self.reset()

    def reset(self) -> None:
        self.game_over = False
        self.player = Cell(
            x=self.width / 2,
            y=self.height / 2,
            mass=40.0,
            color=(255, 255, 255),
        )
        self.foods = [self._create_food() for _ in range(self.food_count)]
        self.bots = [self._create_bot() for _ in range(self.bot_count)]

    def _create_food(self) -> Cell:
        return Cell(
            x=random.uniform(20, self.width - 20),
            y=random.uniform(20, self.height - 20),
            mass=4.0,
            color=random.choice(FOOD_COLORS),
        )

    def _create_bot(self) -> Cell:
        return Cell(
            x=random.uniform(50, self.width - 50),
            y=random.uniform(50, self.height - 50),
            mass=random.uniform(25.0, 90.0),
            color=random.choice(FOOD_COLORS),
            is_bot=True,
        )

    def update(self, target_world_x: float, target_world_y: float) -> None:
        if self.game_over:
            return

        self.player.move_towards(
            target_world_x, target_world_y, self.width, self.height
        )

        for bot in self.bots:
            bot.update_bot_ai(self.width, self.height)

        self._handle_collisions()

    def _handle_collisions(self) -> None:
        for food in self.foods[:]:
            if self.player.can_eat(food):
                self.player.absorb(food)
                self.foods.remove(food)
                self.foods.append(self._create_food())

        for bot in self.bots:
            for food in self.foods[:]:
                if bot.can_eat(food):
                    bot.absorb(food)
                    self.foods.remove(food)
                    self.foods.append(self._create_food())

        for bot in self.bots[:]:
            if self.player.can_eat(bot):
                self.player.absorb(bot)
                self.bots.remove(bot)
                self.bots.append(self._create_bot())
            elif bot.can_eat(self.player):
                bot.absorb(self.player)
                self.game_over = True
                return

        for i, bot_a in enumerate(self.bots):
            for bot_b in self.bots[i + 1 :]:
                if bot_a.can_eat(bot_b):
                    bot_a.absorb(bot_b)
                    if bot_b in self.bots:
                        self.bots.remove(bot_b)
                        self.bots.append(self._create_bot())
                elif bot_b.can_eat(bot_a):
                    bot_b.absorb(bot_a)
                    if bot_a in self.bots:
                        self.bots.remove(bot_a)
                        self.bots.append(self._create_bot())
                    break
