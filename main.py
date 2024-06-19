import argparse
import logging
import pygame
import sys
import math
import random

from engine.game_log import GameActionType, GameLog
from engine.location import Location
from engine.team import Team
from engine.world import World
from engine.unit_player import UnitPlayerBase

from engine.world_manager import WorldManager
from reinforcement.genetic_manager import GeneticManager


BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
RED = (225, 22, 22)
BLUE = (22, 22, 225)
GREEN = (22, 225, 22)
RENDER_SPEED = 8
INFOBAR_HEIGHT = 80


POPULATION_SIZE = 100


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="""
        This is a simple script to run the main program.
        """)
    parser.add_argument("-m", "--map", type=str, default="maps/medium.txt",
                        help="The map file to load.")
    parser.add_argument("-upc1", "--unit_player_class_1", type=str,
                        default="brain",)
    parser.add_argument("-upc2", "--unit_player_class_2", type=str,
                        default="random_player_att",)
    parser.add_argument("-s", "--seed", type=int, default=0,
                        help="The seed to use for the random number generator.")
    parser.add_argument("-r", "--render", action="store_true", default=True,
                        help="Render the game.")
    parser.add_argument("-t", "--train", action="store_true", default=True,
                        help="Train the neural network.")
    return parser.parse_args()


def draw_arrow(screen, color, start, end):
    pygame.draw.line(screen, color, start, end, 3)
    rotation = math.degrees(math.atan2(start[1]-end[1], end[0]-start[0]))+90
    pygame.draw.polygon(screen, color, ((end[0]+4*math.sin(math.radians(rotation)), end[1]+4*math.cos(math.radians(rotation))), (end[0]+4*math.sin(math.radians(
        rotation-120)), end[1]+4*math.cos(math.radians(rotation-120))), (end[0]+4*math.sin(math.radians(rotation+120)), end[1]+4*math.cos(math.radians(rotation+120)))))


def draw_ui(turn: int) -> None:
    # Fill the last 80 pixels with black
    # pygame.draw.rect(SCREEN, BLACK, (0, WINDOW_HEIGHT - INFOBAR_HEIGHT, WINDOW_WIDTH, INFOBAR_HEIGHT))
    font = pygame.font.SysFont(None, 32)
    img = font.render(f'TURN {turn}', True, WHITE)
    SCREEN.blit(img, (20, WINDOW_HEIGHT - INFOBAR_HEIGHT + 20))


def draw_map(world: World) -> None:
    for x in range(0, WINDOW_WIDTH, BLOCK_SIZE):
        for y in range(0, WINDOW_HEIGHT - INFOBAR_HEIGHT, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            loc = Location(x // BLOCK_SIZE, y // BLOCK_SIZE)

            if world.has_obstacle(loc):
                pygame.draw.rect(SCREEN, BLACK, rect)
            elif world.is_occupied(loc):
                if world.get_unit_at_location(loc).team == Team.RED:
                    pygame.draw.rect(SCREEN, RED, rect)
                elif world.get_unit_at_location(loc).team == Team.BLUE:
                    pygame.draw.rect(SCREEN, BLUE, rect)
                else:
                    pygame.draw.rect(SCREEN, GREEN, rect)
            else:
                pygame.draw.rect(SCREEN, WHITE, rect)


def draw_debug(game_log: GameLog, turn: int) -> None:
    for action in game_log.actions[turn-1]:
        subject_center = (action.subject_location.x * BLOCK_SIZE + BLOCK_SIZE // 2,
                          action.subject_location.y * BLOCK_SIZE + BLOCK_SIZE // 2)
        target_center = (action.target_location.x * BLOCK_SIZE + BLOCK_SIZE // 2,
                         action.target_location.y * BLOCK_SIZE + BLOCK_SIZE // 2)

        if action.action_type == GameActionType.MOVE:
            color = GREEN
        elif action.action_type == GameActionType.ATTACK:
            color = RED
        elif action.action_type == GameActionType.HEAL:
            color = BLUE
        else:
            color = WHITE

        # Draw an arrow from the subject to the target
        # pygame.draw.line(SCREEN, color, subject_center, target_center, 5)
        draw_arrow(SCREEN, color, subject_center, target_center)


def render_screen(world: World, game_log: GameLog, turn: int) -> None:
    SCREEN.fill(BLACK)
    draw_map(world)
    draw_ui(turn)
    draw_debug(game_log, turn)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    CLOCK.tick(RENDER_SPEED)


def train(args: argparse.Namespace, unit_player_class_1: UnitPlayerBase, unit_player_class_2: UnitPlayerBase):
    genetic_manager = GeneticManager(
        population_size=POPULATION_SIZE,
        mutation_rate=0.05,
        crossover_rate=0.1,
        net_params={
            'input_nodes': 118,
            'hidden_nodes': 16,
            'output_nodes': 9,
        }
    )
    genetic_manager.initialize_population()
    GeneticManager.set_instance(genetic_manager)

    for generation in range(100):
        for i in range(POPULATION_SIZE):
            logging.info(f'Generation {generation+1} - {i+1}/{POPULATION_SIZE}')
            game_manager = WorldManager(args.map, unit_player_class_1, unit_player_class_2, {
                "max_turns": 100,
            })

            random.seed(42)

            winner = game_manager.run_game(None)

            if winner == Team.BLUE:
                genetic_manager.get_current_net().fitness += (100-game_manager.turn) * 2

            # logging.info(f"Sample fitness: {genetic_manager.get_current_iteration_fitness()}")
            genetic_manager.next_iteration()

        genetic_manager.new_generation()
        logging.info(f"Average fitness of generation {generation+1}: {genetic_manager.current_fitness}")
        logging.info(f"Best fitness of generation {generation+1}: {genetic_manager.best_fitness}")


def render_game(args: argparse.Namespace, unit_player_class_1: UnitPlayerBase, unit_player_class_2: UnitPlayerBase):
    global SCREEN, CLOCK, WINDOW_HEIGHT, WINDOW_WIDTH, BLOCK_SIZE

    render_method = None
    game_manager = WorldManager(args.map, unit_player_class_1, unit_player_class_2, {
                "max_turns": 2000,
            })

    if args.render:
        BLOCK_SIZE = 20
        WINDOW_WIDTH = BLOCK_SIZE * game_manager.world.width
        WINDOW_HEIGHT = BLOCK_SIZE * game_manager.world.height + INFOBAR_HEIGHT

        pygame.init()
        SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        CLOCK = pygame.time.Clock()
        SCREEN.fill(BLACK)
        render_method = render_screen

    game_manager.run_game(render_method)


def load_unit_player_class(name: str) -> UnitPlayerBase:
    upc = f"brains.{name}.unit_player.UnitPlayer"
    upc = getattr(__import__(upc.rsplit(".", 1)[0], fromlist=[
                                upc.rsplit(".", 1)[1]]), upc.rsplit(".", 1)[1])
    return upc


def main(args: argparse.Namespace) -> None:
    logging.basicConfig(level=logging.INFO)

    unit_player_class_1 = load_unit_player_class(args.unit_player_class_1)
    unit_player_class_2 = load_unit_player_class(args.unit_player_class_2)

    if args.train:
        train(args, unit_player_class_1, unit_player_class_2)
    else:
        render_game(args, unit_player_class_1, unit_player_class_2)


if __name__ == "__main__":
    args = parse_args()
    main(args)
