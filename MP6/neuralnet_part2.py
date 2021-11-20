# neuralnet.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 10/29/2019
# Modified by Mahir Morshed for the spring 2021 semester
# Modified by Joao Marques (jmc12) for the fall 2021 semester 

"""
This is the main entry point for MP3. You should only modify code
within this file and neuralnet_part1.py,neuralnet_leaderboard -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""

import numpy as np

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from utils import get_dataset_from_arrays
from torch.utils.data import DataLoader


class NeuralNet(nn.Module):
    def __init__(self, lrate, loss_fn, in_size, out_size):
        """
        Initializes the layers of your neural network.

        @param lrate: learning rate for the model
        @param loss_fn: A loss function defined as follows:
            @param yhat - an (N,out_size) Tensor
            @param y - an (N,) Tensor
            @return l(x,y) an () Tensor that is the mean loss
        @param in_size: input dimension
        @param out_size: output dimension

        For Part 1 the network should have the following architecture (in terms of hidden units):

        in_size -> 32 ->  out_size
        
        We recommend setting lrate to 0.01 for part 1.
        """

        super(NeuralNet, self).__init__()
        self.lrate = lrate
        self.loss_fn = loss_fn
        self.in_size = in_size
        self.out_size = out_size
        self.hidden_size = 100

        self.seq1 = nn.Sequential( #ELU best activ. 
            nn.Conv2d(self.in_size, 20, 3),
            nn.ELU(),
            nn.Conv2d(20, 10, 3), 
            nn.ELU()
        )
        
        self.seq2 = nn.Sequential(
            nn.Linear(7840, 20), #25088 = 10 * 28 * 28
            nn.ELU(),
            nn.Linear(20, self.out_size)
        )

        self.optimizer = optim.SGD(self.parameters(), lr=lrate, momentum=0.9)
    

    def forward(self, x):
        """Performs a forward pass through your neural net (evaluates f(x)).

        @param x: an (N, in_size) Tensor
        @return y: an (N, out_size) Tensor of output from the network
        """
        #resize x
        # print(x.size())
        # print(x.shape[0])
        x = x.view(torch.numel(x) // 3072, 3, 32, 32)
        x = self.seq1(x)
        # print(x.size())
        x = torch.flatten(x, 1) #turn back into vector of N by 100 * 32 * 28 * 28 = 100 * 25088
        # print(x.size())
        x = self.seq2(x)
        return x

    def step(self, x, y):
        """
        Performs one gradient step through a batch of data x with labels y.

        @param x: an (N, in_size) Tensor
        @param y: an (N,) Tensor
        @return L: total empirical risk (mean of losses) for this batch as a float (scalar)
        """

        self.optimizer.zero_grad()
        output = self.forward(x)
        loss = self.loss_fn(output, y)
        loss.backward()
        self.optimizer.step()

        return loss.detach().cpu().numpy()


def fit(train_set,train_labels,dev_set,epochs,batch_size=100):
    """ Make NeuralNet object 'net' and use net.step() to train a neural net
    and net(x) to evaluate the neural net.

    @param train_set: an (N, in_size) Tensor
    @param train_labels: an (N,) Tensor
    @param dev_set: an (M,) Tensor
    @param epochs: an int, the number of epochs of training
    @param batch_size: size of each batch to train on. (default 100)

    This method _must_ work for arbitrary M and N.

    The model's performance could be sensitive to the choice of learning rate.
    We recommend trying different values in case your first choice does not seem to work well.

    @return losses: list of floats containing the total loss at the beginning and after each epoch.
            Ensure that len(losses) == epochs.
    @return yhats: an (M,) NumPy array of binary labels for dev_set
    @return net: a NeuralNet object
    """
    #standardize input 
    mean = torch.mean(train_set)
    std = torch.std(train_set, False)
    train_set = torch.sub(train_set, mean)
    train_set = torch.div(train_set, std)

    #standardize output
    mean = torch.mean(dev_set)
    std = torch.std(dev_set, False)
    dev_set = torch.sub(dev_set, mean)
    dev_set = torch.div(dev_set, std)

    #create datasets
    train_dataset = get_dataset_from_arrays(train_set, train_labels)
    train_generator = DataLoader(dataset=train_dataset, batch_size=batch_size, shuffle=False)

    #NN training
    net = NeuralNet(0.001, nn.CrossEntropyLoss(), 3, 4)
    # print(len(train_set[0]))

    losses, yhats = [], []
    for epoch in range(epochs):
        loss = 0
        for batch in train_generator:
            loss += net.step(batch['features'], batch['labels'])
            
        losses.append(loss)


    # #use NN to generate tags
    for pic in dev_set:
        output = net.forward(pic)
        # print(output)
        yhats.append(torch.argmax(output))
    
    # raise NotImplementedError("You need to write this part!")
    return losses, np.array(yhats).astype(int), net