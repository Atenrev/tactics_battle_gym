# Tactics Battle Gym
This project is a strategy game simulation where two teams, each controlled by a UnitPlayer script describing the algorithm, compete against each other. The goal of the game is to outlast the opponent. 

The game is played on a grid-based map, where each cell can be occupied by a unit. The units can move and attack other units within their range. The game is turn-based, with each unit of each player taking turns to perform their actions. The game ends when one of the players has no units left on the map.

## Getting Started
To get started with this project, clone the repository to your local machine.

```
git clone https://github.com/Atenrev/tactics-battle-gym.git
```

## Prerequisites
This project requires Python and the following Python libraries installed:

- pygame
- numpy
- pytorch


## Running the Game
To run the game, navigate to the project directory and run the main.py script:

```
python main.py
```

You can customize the game by passing arguments to the script. Here are the available options:

```
-m or --map: The map file to load. Default is "maps/medium.txt".
-upc1 or --unit_player_class_1: The class of the first player's units. Default is "random_player_att".
-upc2 or --unit_player_class_2: The class of the second player's units. Default is "random_player_att".
-s or --seed: The seed to use for the random number generator. Default is 0.
-r or --render: Whether to render the game to a window. Default is True.
-t or --train: Train the neural network. Default is True.
Training the Neural Network
The neural network is trained using a genetic algorithm implemented in the GeneticManager class. The training process is initiated in the train function in main.py.
```

### Game Rendering
The game can be rendered to a window using the Pygame library. The rendering process is handled in the render_game function in main.py.

## Coding your own UnitPlayer
You can create your own UnitPlayer class by inheriting from the UnitPlayerBase class in the ```engine/unit_player.py``` file. You will need to implement the following methods:

- ```__init__(self, uc)```: The constructor for the class. The uc parameter is the unit controller for the unit.
- ```run(self)```: The main method for the class. This method is called each turn to determine the unit's actions.

You can start by copying the random player in ```brains/random_player/unit_player.py``` and modifying it to implement your own strategy.

## TODO
- [ ] Introduce more unit types (e.g. warriors, buildings, etc.)
- [ ] Allow units that can instantiate other units (e.g. summoners, builders, etc.)
- [ ] Implement a shared memory for the units of the same player to communicate with each other
- [ ] Abstract the training method to allow for different training algorithms (e.g. Q-learning, DQN, etc.)
- [ ] Implement Reinforcement Learning strategy for UnitPlayer
- [ ] Implement Monte Carlo Tree Search strategy for UnitPlayer
- [ ] Tool for creating maps
- [ ] Tournament mode that runs games on multiple maps and records the results

## Contributing
<!-- Please read CONTRIBUTING.md for details on our code of conduct, and the process for submitting pull requests to us. -->
Currently, there is no specific information available on contributing to this project. However, if you would like to contribute, please contact the author.

## License
This project is licensed under the MIT License - see the LICENSE.md file for details.