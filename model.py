import torch
import torch.nn as nn
import torch.optim as optim
from torch.distributions import Categorical


class PolicyNetwork(nn.Module):
    def __init__(self, num_inputs, num_outputs):
        super(PolicyNetwork, self).__init__()
        self.fc = nn.Linear(num_inputs, num_outputs)

    def forward(self, x):
        return Categorical(torch.softmax(self.fc(x), dim=-1))


class ValueNetwork(nn.Module):
    def __init__(self, num_inputs):
        super(ValueNetwork, self).__init__()
        self.fc = nn.Linear(num_inputs, 1)

    def forward(self, x):
        return self.fc(x)


policyNet = PolicyNetwork(15, 1)
valueNet = ValueNetwork(15)

policyOptimizer = optim.Adam(policyNet.parameters())
valueOptimizer = optim.Adam(valueNet.parameters())
