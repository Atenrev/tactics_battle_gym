import torch


class Model(torch.nn.Module):
    """
    Simple model.

    Inputs:
        - Location of the unit [2]
        - Location of the three nearest enemies [6]
        - Location of the three nearest allies [6]
        - Location of the three nearest obstacles [6]

    Outputs:
        - Direction to move [9]  
    """

    def __init__(self):
        super().__init__()
        self.fc1 = torch.nn.Linear(2 + 6 + 6 + 6, 128)
        self.fc2 = torch.nn.Linear(128, 128)
        self.fc3 = torch.nn.Linear(128, 9)
        self.activation = torch.nn.ReLU()

    def forward(self, x):
        x = self.activation(self.fc1(x))
        x = self.activation(self.fc2(x))
        x = self.fc3(x)
        return x
