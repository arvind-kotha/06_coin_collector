"""
GameEngine: owns the player and all coins.

Starter version: one coin type, no obstacles, no timer yet. Coin
collection also has a known bug (see how `update` uses check_collection
below) that Task 1 asks you to fix - collected coins are never removed,
so standing on one keeps awarding points every frame.
"""

import random
import pygame

from game.player import Player
from game.coin import Coin
from game.collection import check_collection
from game.renderer import WIDTH, HEIGHT

NUM_COINS = 6
COIN_TYPES = [
    (1, (180, 120, 60)),   # bronze
    (3, (200, 200, 200)),  # silver
    (5, (230, 190, 60)),   # gold
]


class GameEngine:
    def __init__(self):
        self.player = Player(x=WIDTH / 2, y=HEIGHT / 2)
        self.coins = [self._random_coin() for _ in range(NUM_COINS)]
        self.score = 0
        self.lives = 3
        self.obstacles = [
             pygame.Rect(150, 100, 120, 30),
             pygame.Rect(430, 180, 30, 140),
             pygame.Rect(220, 350, 180, 30),
        ]
        self.round_time = 30
        self.start_time = pygame.time.get_ticks()
        self.game_over = False

    def _random_coin(self):
        x = random.randint(30, WIDTH - 30)
        y = random.randint(30, HEIGHT - 30)
        value, color = random.choice(COIN_TYPES)
        return Coin(x=x, y=y, radius=12, value=value, color=color)

    def handle_input(self, keys_pressed):
        if self.game_over:
            return
        dx = dy = 0
        if keys_pressed[pygame.K_UP]:
            dy -= self.player.speed
        if keys_pressed[pygame.K_DOWN]:
            dy += self.player.speed
        if keys_pressed[pygame.K_LEFT]:
            dx -= self.player.speed
        if keys_pressed[pygame.K_RIGHT]:
            dx += self.player.speed
        self.player.move(dx, dy, WIDTH, HEIGHT)
        old_x, old_y = self.player.x, self.player.y
        self.player.move(dx, dy, WIDTH, HEIGHT)
 
        if any(self.player.get_rect().colliderect(obstacle)
                for obstacle in self.obstacles):
             self.player.x, self.player.y = old_x, old_y
             self.lives = max(0, self.lives - 1)

    def update(self):
        if self.game_over:
            return
    
        elapsed = (pygame.time.get_ticks() - self.start_time) / 1000
        self.round_time = max(0, 30 - int(elapsed))
    
        if self.round_time == 0 or self.lives <= 0:
            self.game_over = True
            return
     
        collected = check_collection(self.player, self.coins)
        for coin in collected:
            self.score += coin.value
            self.coins.remove(coin)

    def draw(self, surface, font):
        from game import renderer
        renderer.draw_scene(surface, self.player, self.coins, self.obstacles)
        renderer.draw_text(surface, font, f"Score: {self.score}", (10, 10))
        renderer.draw_text(surface, font, f"Lives: {self.lives}", (10, 40))
        renderer.draw_text(surface, font, f"Time: {self.round_time}", (10, 70))
    
        if self.game_over:
            renderer.draw_banner(
                surface,
                font,
                f"Game Over! Final Score: {self.score} | Press R to restart"
            )
    def reset(self):
        self.player = Player(x=WIDTH / 2, y=HEIGHT / 2)
        self.coins = [self._random_coin() for _ in range(NUM_COINS)]
        self.score = 0
        self.lives = 3
        self.round_time = 30
        self.start_time = pygame.time.get_ticks()
        self.game_over = False
