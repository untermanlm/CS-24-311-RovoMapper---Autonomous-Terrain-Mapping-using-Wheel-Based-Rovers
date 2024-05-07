import pygame
import sys
import random
import math

# Define screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

class Dot:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)
        self.radius = 10
        self.color = BLACK
        self.speed = 2
        self.angle = random.uniform(0, math.pi * 2)  # Random initial angle in radians
        self.collisions = set()  # set to store collision points

    def move(self, blocks):
        # Update position based on angle
        prev_x, prev_y = self.x, self.y
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)

        # Check for collisions with blocks
        for block in blocks:
            if self.x + self.radius > block.x and self.x - self.radius < block.x + block.width \
                    and self.y + self.radius > block.y and self.y - self.radius < block.y + block.height:
                self.collisions.add((self.x, self.y))
                self.angle = math.atan2(prev_y - self.y, prev_x - self.x) + random.uniform(-0.1, 0.1)
                self.x = max(block.x - self.radius, min(block.x + block.width + self.radius, self.x))
                self.y = max(block.y - self.radius, min(block.y + block.height + self.radius, self.y))

        # Check for collisions with screen edges
        if self.x < 0 or self.x > SCREEN_WIDTH or self.y < 0 or self.y > SCREEN_HEIGHT:
            self.collisions.add((self.x, self.y))
            # Bounce off the edges
            if self.x < 0 or self.x > SCREEN_WIDTH:
                self.angle = math.pi - self.angle  # Reverse the horizontal angle
            if self.y < 0 or self.y > SCREEN_HEIGHT:
                self.angle = -self.angle  # Reverse the vertical angle

        # random deviation to the angle for smooth curve
        self.angle += random.uniform(-0.1, 0.1)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        for collision in self.collisions:
            pygame.draw.circle(screen, RED, (int(collision[0]), int(collision[1])), self.radius)

class Block:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = BLACK

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Bouncing Dot")

    clock = pygame.time.Clock()

    dot = Dot()

    # Define blocks
    blocks = [Block(200, 200, 100, 100), Block(400, 300, 150, 50)]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                for collision in dot.collisions:
                    print(f"{collision},")
                dot.collisions.clear()
                pygame.quit()
                sys.exit()

        dot.move(blocks)

        screen.fill(WHITE)
        for block in blocks:
            block.draw(screen)
        dot.draw(screen)
        pygame.display.flip()

        clock.tick(100)  # Limit frame rate to 60 FPS

if __name__ == "__main__":
    main()
