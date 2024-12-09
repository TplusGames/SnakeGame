import pygame
import Snake
import Food
import Wall
import HighScoreTracker
import GameStates as gS
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 800
CELL_SIZE = 20

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

state_manager = gS.game_state_manager()

# Game variables
SPEED_INCREASE = 0.25

current_high_score = HighScoreTracker.high_score()


def main():
    global current_high_score
    high_scores = HighScoreTracker.load_high_scores()
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()

    while state_manager.get_current_state() != gS.STATE_QUIT:
        if state_manager.get_current_state() == gS.STATE_MENU:
            state_manager.set_state(main_menu(screen, high_scores))
        elif state_manager.get_current_state() == gS.STATE_PLAY:
            state_manager.set_state(play_game(screen, clock, high_scores))
        elif state_manager.get_current_state() == gS.STATE_END_GAME:
            state_manager.set_state(end_game(current_high_score, high_scores, screen))

    pygame.quit()
    print("Game closed.")


def play_game(screen, clock, high_scores):
    global current_high_score
    current_high_score = HighScoreTracker.high_score()
    snake = Snake.Snake()
    food = Food.Food()
    walls = Wall.Walls()
    food.position = food.random_position(SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE, walls)
    fps = 10
    wall_spawn_counter = 0

    while True:
        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != 'DOWN':
                    snake.direction = 'UP'
                elif event.key == pygame.K_DOWN and snake.direction != 'UP':
                    snake.direction = 'DOWN'
                elif event.key == pygame.K_LEFT and snake.direction != 'RIGHT':
                    snake.direction = 'LEFT'
                elif event.key == pygame.K_RIGHT and snake.direction != 'LEFT':
                    snake.direction = 'RIGHT'

        # Update Game State
        snake.move()
        if snake.body[0] == food.position:
            current_high_score.score += 1  # Increment score
            fps += SPEED_INCREASE  # Increase game speed
            snake.grow()
            food.position = food.random_position(SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE, walls)
        if snake.is_collision(SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE, walls):
            print(f"Game Over! Your score: {current_high_score.score}")
            return gS.STATE_END_GAME

        # Spawn walls after certain time
        wall_spawn_counter += 1
        if wall_spawn_counter >= 50:  # Adjust the value for spawn frequency
            walls.spawn_wall(SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE, food, snake)
            wall_spawn_counter = 0

        screen.fill(BLACK)

        walls.draw(screen, WHITE, CELL_SIZE)

        # Draw Snake
        for segment in snake.body:
            pygame.draw.rect(screen, GREEN,
                             pygame.Rect(segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Draw Food
        pygame.draw.rect(screen, RED,
                         pygame.Rect(food.position[0] * CELL_SIZE, food.position[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Font setup
        font = pygame.font.SysFont("Arial", 24)

        # Draw Score
        score_text = font.render(f"Score: {current_high_score.score}", True, WHITE)
        screen.blit(score_text, (10, 10))  # Top-left corner

        # Update Display
        pygame.display.flip()

        clock.tick(fps)


def main_menu(screen, high_scores):
    menu_font = pygame.font.SysFont("Arial", 36)
    title_text = menu_font.render("Snake Game", True, (255, 255, 255))
    play_text = menu_font.render("Press P to Play", True, (255, 255, 255))
    quit_text = menu_font.render("Press Q to Quit", True, (255, 255, 255))
    high_scores_text = pygame.font.SysFont("Arial", 24).render("High Scores:", True, (255, 255, 255))

    while True:
        screen.fill((0, 0, 0))  # Clear the screen with black
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 5))
        screen.blit(play_text, (SCREEN_WIDTH // 2 - play_text.get_width() // 2, SCREEN_HEIGHT // 2))
        screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
        screen.blit(high_scores_text, (50, SCREEN_HEIGHT // 3))

        score_num = 0

        # Display each high score
        for high_score in high_scores:

            split = " : "

            name = high_score.name
            score = high_score.score

            if name == "":
                name = "No name"

            score_text = pygame.font.SysFont("Arial", 24).render(f"{name + split + str(score)}", True, (255, 255, 255))
            screen.blit(score_text, (50, SCREEN_HEIGHT // 3 + 30 * (score_num + 1)))
            score_num += 1

        pygame.display.flip()  # Update the screen

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return gS.STATE_QUIT
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Start the game
                    return gS.STATE_PLAY
                if event.key == pygame.K_q:  # Quit the game
                    return gS.STATE_QUIT


def end_game(new_high_score, high_scores, screen):
    high_score_to_add = HighScoreTracker.high_score("", new_high_score.score)

    input_box = pygame.Rect(100, 100, 200, 50)
    entering_name = True
    text = ""

    while entering_name:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    high_score_to_add.set_name(text)
                    entering_name = False
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

        # Clear the screen
        screen.fill(BLACK)

        # Draw the input box
        pygame.draw.rect(screen, BLACK, input_box, 2)  # Draw border of input box

        # Render the text inside the input box
        font = pygame.font.Font(None, 36)
        text_surface = font.render(text, True, WHITE)
        screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))
        input_box.w = max(200, text_surface.get_width() + 10)

        # Update the display
        pygame.display.flip()

    # Update and save high scores
    new_high_scores = HighScoreTracker.update_high_scores(high_score_to_add, high_scores)
    HighScoreTracker.save_high_scores(new_high_scores)
    return gS.STATE_MENU


if __name__ == "__main__":
    main()
