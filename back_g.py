#!/usr/bin/env python
# coding: utf-8


import torchvision
import torchvision.datasets as dset
import torchvision.transforms as transforms
from torch.utils.data import DataLoader,Dataset
import matplotlib.pyplot as plt
import torchvision.utils
import numpy as np
import random
from PIL import Image
import torch
from torch.autograd import Variable
import PIL.ImageOps    
import torch.nn as nn
from torch import optim
import torch.nn.functional as F
from time import time


class SiameseNetwork(nn.Module):
    def __init__(self):
        super(SiameseNetwork, self).__init__()
        self.cnn1 = nn.Sequential(
            nn.ReflectionPad2d(1),
            nn.Conv2d(1, 4, kernel_size=3),
            nn.ReLU(inplace=True),
            nn.BatchNorm2d(4),
            
            nn.ReflectionPad2d(1),
            nn.Conv2d(4, 8, kernel_size=3),
            nn.ReLU(inplace=True),
            nn.BatchNorm2d(8),

            nn.ReflectionPad2d(1),
            nn.Conv2d(8, 8, kernel_size=3),
            nn.ReLU(inplace=True),
            nn.BatchNorm2d(8),

        )

        self.fc1 = nn.Sequential(
            nn.Linear(8*100*100, 500),
            nn.ReLU(inplace=True),

            nn.Linear(500, 500),
            nn.ReLU(inplace=True),

            nn.Linear(500, 5))

    def forward_once(self, x):
        output = self.cnn1(x)
        output = output.view(output.size()[0], -1)
        output = self.fc1(output)
        return output

    def forward(self, input1, input2):
        output1 = self.forward_once(input1)
        output2 = self.forward_once(input2)
        return output1, output2
    


def change(img0,img1):
   
    ##调整图像大小
    rimg0 = transforms.Resize((100,100))(img0)
    rimg1 = transforms.Resize((100,100))(img1)

    ##将图像转化成张量
    timg0 = transforms.ToTensor()(rimg0)
    timg1 = transforms.ToTensor()(rimg1)


    ##修改通道数和维度（目标格式【1，1，100，100】）
    simg0 = torch.unsqueeze(timg0,0)
    simg1 = torch.unsqueeze(timg1,0) 

    mimg0 = torch.mean(simg0, dim = 1)
    mimg1 = torch.mean(simg1, dim = 1)

    simg0 = torch.unsqueeze(mimg0,0)
    simg1 = torch.unsqueeze(mimg1,0) 
    return simg0, simg1

def distance(vec1,vec2):
    dist = F.pairwise_distance(vec1, vec2)
    return dist



def process(img0, img1):

    net = SiameseNetwork()
    net.load_state_dict(torch.load("net_state_dict.pt", map_location=torch.device("cpu")))
    img0, img1 = change(img0, img1)
    start = time()
    output1, output2 = net(img0, img1)
    end = time()
    return float(distance(output1, output2)),end-start

if __name__ == '__main__':
    img0 = Image.open('11.png')
    img1 = Image.open('11.png')

    A = process(img0, img1)
    print(A[0], A[1])
    