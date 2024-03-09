from random import randint, choice

import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
SPEED = 5

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

pygame.display.set_caption('Змейка')

clock = pygame.time.Clock()

TURNS = {
    (pygame.K_UP, DOWN): UP,
    (pygame.K_DOWN, UP): DOWN,
    (pygame.K_LEFT, RIGHT): LEFT,
    (pygame.K_RIGHT, LEFT): RIGHT
}


class GameObject:
    """Base class for all game objects.

    Attributes:
    position (tuple): (x, y) position of the game object,
    by default it's the center of the game screen
    body_color: one of the predefined RGB colors
    """

    def __init__(self, body_color=None):
        """Initialize game object."""
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = body_color

    def draw(self, surface):
        """Draw the object on game screen."""
        raise NotImplementedError

    def draw_block(self, coordinates):
        """Draw one square block of the object on the screen."""
        rect = pygame.Rect(coordinates, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """
    Derived class for Apple game object.

    Inherits from GameObject class
    Attributes:
        free_cells (list): List of screen blocks unoccupied by other objects
    """

    def __init__(self, body_color=APPLE_COLOR, free_cells=[]):
        """Initialize Apple object."""
        super().__init__(body_color)
        self.free_cells = free_cells
        self.randomize_position(self.free_cells)

    def randomize_position(self, free_cells):
        """Randomize the Apple object position on screen."""
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if self.position not in free_cells:
                break

    def draw(self, screen):
        """Draw the Apple object on game screen."""
        super().draw_block((self.position[0], self.position[1]))


class Snake(GameObject):
    """
    Derived class for Snake game object.

    Inherits from GameObject class
    Attributes:
    length: Length of the snake, =1 at the beginning of the game
    positions (tuple): List of (X, y) positions of the Snake blocks
    direction: Direction of Snake movement, one of the predefined directions
    next_direction: next movement direction after the key is pressed by user
    """

    def __init__(self, body_color=SNAKE_COLOR):
        """Initialize Snake object."""
        super().__init__(body_color)
        self.reset()
        self.direction = RIGHT

    def get_head_position(self):
        """Get the head coordinates of the Snake."""
        return self.positions[0]

    def update_direction(self, next_direction):
        """Update the direction of Snake movement."""
        self.direction = self.next_direction
        self.next_direction = None

    def move(self):
        """Define the movement logic of the Snake."""
        x, y = self.get_head_position()
        dx, dy = self.direction

        position = (
            (x + (dx * GRID_SIZE)) % SCREEN_WIDTH,
            (y + (dy * GRID_SIZE)) % SCREEN_HEIGHT,
        )

        self.positions.insert(0, position)
        pygame.display.update()

    def draw(self, screen):
        """Draw the Snake object on game screen."""
        super().draw_block((self.position[0], self.position[1]))
        super().draw_block((self.positions[0]))

        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Reset the Snake to the initial condition."""
        self.length = 1
        self.positions = [self.position]
        self.last = None
        self.next_direction = None
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        screen.fill(BOARD_BACKGROUND_COLOR)


def handle_keys(game_object):
    """Handle user input and changes object's movement direction."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            for turn in TURNS:
                if event.key == turn[0] and game_object.direction != turn[1]:
                    game_object.next_direction = TURNS[turn]


def main():
    """Run game cycle.

    Define behaviour after eating Apple and after hitting itself.
    """
    pygame.init()
    screen.fill(BOARD_BACKGROUND_COLOR)
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()
        if snake.next_direction:
            snake.update_direction(snake.next_direction)

        if snake.positions[0] == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        if len(snake.positions) > snake.length:
            snake.last = snake.positions.pop()
        else:
            snake.last = None

        if snake.get_head_position() in snake.positions[2:]:
            snake.reset()
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()
