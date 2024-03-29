# -*- coding: utf-8 -*-
"""simplenet.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Afsu4gFpPRNzvOeP77Lt7w7-am1I0PG8
"""
# Commented out IPython magic to ensure Python compatibility.
# %config IPCompleter.greedy=True

import sys
import numpy as np

train_data = np.loadtxt(sys.argv[1])
test_data = np.loadtxt(sys.argv[2])

import time

import torch
import torch.nn as nn
from torch.autograd import Variable
from torch.utils.data import DataLoader, TensorDataset
from torch.optim import lr_scheduler
from torchvision import transforms

# parameters for the network
epochs = 35
batch_size = 64
workers = 2
num_classes = 100

# Ignore warnings
import warnings
warnings.filterwarnings("ignore")

train_x = np.reshape(train_data[:,:-2], (train_data.shape[0], 3, 32, 32))
# train_x = np.swapaxes(train_x, 1, 2)
# train_x = np.swapaxes(train_x, 2, 3)
train_y = train_data[:, -1]
# enc_y = OneHotEncoder(handle_unknown='ignore')
# enc_y.fit(train_data[:, -1:])
# train_y = enc_y.transform(train_data[:, -1:]).toarray()

test_x = np.reshape(test_data[:,:-2], (test_data.shape[0], 3, 32, 32))
# test_x = np.swapaxes(test_x, 1, 2)
# test_x = np.swapaxes(test_x, 2, 3)

#   # Data transforms
# mean = [0.5071, 0.4867, 0.4408]
# std = [0.2675, 0.2565, 0.2761]

# transformation code
train_r = np.dstack([train_x[i][0] for i in range(len(train_x))])
train_g = np.dstack([train_x[i][1] for i in range(len(train_x))])
train_b = np.dstack([train_x[i][2] for i in range(len(train_x))])
mean = [x/255 for x in [np.mean(train_r), np.mean(train_g), np.mean(train_b)]]
std = [x/255 for x in [np.std(train_r), np.std(train_g), np.std(train_b)]]

train_transforms = transforms.Compose(
    [ transforms.ToPILImage(), transforms.RandomCrop(32, padding=4),transforms.RandomHorizontalFlip(), transforms.ToTensor(),
     transforms.Normalize(mean, std)]
)
train_data = torch.Tensor(train_x)
train_x_tensor = []
for tnsr in train_data:
    train_x_tensor.append(train_transforms(tnsr).numpy())
train_x_tensor =  torch.Tensor(np.array(train_x_tensor))



test_transforms = transforms.Compose(
    [transforms.ToPILImage(), transforms.CenterCrop(32), transforms.ToTensor(), transforms.Normalize(mean, std)]
)
test_data = torch.Tensor(test_x)
test_x_tensor = []
for tnsr in test_data:
    test_x_tensor.append(test_transforms(tnsr).numpy())
test_x_tensor = torch.Tensor(np.array(test_x_tensor))

train_y_tensor = torch.Tensor(train_y)

class simplenet(nn.Module):
    def __init__(self, classes=100):
        super(simplenet, self).__init__()

        self.features = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=[3, 3], stride=(1, 1), padding=(1, 1)),
                             nn.BatchNorm2d(64, eps=1e-05, momentum=0.05, affine=True),
                             nn.ReLU(inplace=True),

                             nn.Conv2d(64, 128, kernel_size=[3, 3], stride=(1, 1), padding=(1, 1)),
                             nn.BatchNorm2d(128, eps=1e-05, momentum=0.05, affine=True),
                             nn.ReLU(inplace=True),

                             nn.Conv2d(128, 128, kernel_size=[3, 3], stride=(1, 1), padding=(1, 1)),
                             nn.BatchNorm2d(128, eps=1e-05, momentum=0.05, affine=True),
                             nn.ReLU(inplace=True),

                             nn.Conv2d(128, 128, kernel_size=[3, 3], stride=(1, 1), padding=(1, 1)),
                             nn.BatchNorm2d(128, eps=1e-05, momentum=0.05, affine=True),
                             nn.ReLU(inplace=True),


                             nn.MaxPool2d(kernel_size=(2, 2), stride=(2, 2), dilation=(1, 1), ceil_mode=False),
                             nn.Dropout2d(p=0.1),


                             nn.Conv2d(128, 128, kernel_size=[3, 3], stride=(1, 1), padding=(1, 1)),
                             nn.BatchNorm2d(128, eps=1e-05, momentum=0.05, affine=True),
                             nn.ReLU(inplace=True),

                             nn.Conv2d(128, 128, kernel_size=[3, 3], stride=(1, 1), padding=(1, 1)),
                             nn.BatchNorm2d(128, eps=1e-05, momentum=0.05, affine=True),
                             nn.ReLU(inplace=True),

                             nn.Conv2d(128, 256, kernel_size=[3, 3], stride=(1, 1), padding=(1, 1)),
                             nn.BatchNorm2d(256, eps=1e-05, momentum=0.05, affine=True),
                             nn.ReLU(inplace=True),



                             nn.MaxPool2d(kernel_size=(2, 2), stride=(2, 2), dilation=(1, 1), ceil_mode=False),
                             nn.Dropout2d(p=0.1),


                             nn.Conv2d(256, 256, kernel_size=[3, 3], stride=(1, 1), padding=(1, 1)),
                             nn.BatchNorm2d(256, eps=1e-05, momentum=0.05, affine=True),
                             nn.ReLU(inplace=True),


                             nn.Conv2d(256, 256, kernel_size=[3, 3], stride=(1, 1), padding=(1, 1)),
                             nn.BatchNorm2d(256, eps=1e-05, momentum=0.05, affine=True),
                             nn.ReLU(inplace=True),



                             nn.MaxPool2d(kernel_size=(2, 2), stride=(2, 2), dilation=(1, 1), ceil_mode=False),
                             nn.Dropout2d(p=0.1),



                             nn.Conv2d(256, 512, kernel_size=[3, 3], stride=(1, 1), padding=(1, 1)),
                             nn.BatchNorm2d(512, eps=1e-05, momentum=0.05, affine=True),
                             nn.ReLU(inplace=True),



                             nn.MaxPool2d(kernel_size=(2, 2), stride=(2, 2), dilation=(1, 1), ceil_mode=False),
                             nn.Dropout2d(p=0.1),


                             nn.Conv2d(512, 2048, kernel_size=[1, 1], stride=(1, 1), padding=(0, 0)),
                             nn.BatchNorm2d(2048, eps=1e-05, momentum=0.05, affine=True),
                             nn.ReLU(inplace=True),



                             nn.Conv2d(2048, 256, kernel_size=[1, 1], stride=(1, 1), padding=(0, 0)),
                             nn.BatchNorm2d(256, eps=1e-05, momentum=0.05, affine=True),
                             nn.ReLU(inplace=True),


                             nn.MaxPool2d(kernel_size=(2, 2), stride=(2, 2), dilation=(1, 1), ceil_mode=False),
                             nn.Dropout2d(p=0.1),


                             nn.Conv2d(256, 256, kernel_size=[3, 3], stride=(1, 1), padding=(1, 1)),
                             nn.BatchNorm2d(256, eps=1e-05, momentum=0.05, affine=True),
                             nn.ReLU(inplace=True),

        )

        for m in self.features.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.xavier_uniform(m.weight.data, gain=nn.init.calculate_gain('relu'))
        
        self.classifier = nn.Linear(256, classes)
        # can change to tweak
        self.final_dropout = nn.Dropout(0.1)

    def forward(self, x):
        output = self.features(x)
        output = self.final_dropout(output)

        output = output.view(output.size(0), -1)
        output = self.classifier(output)
        return output

def accuracy(output, target, topk=(1,)):
  """Computes the precision@k for the specified values of k"""
  maxk = max(topk)
  batch_size = target.size(0)

  _, pred = output.topk(maxk, 1, True, True)
  pred = pred.t()
  correct = pred.eq(target.view(1, -1).expand_as(pred))
  
  res = []
  for k in topk:
    correct_k = correct[:k].view(-1).float().sum(0)
    res.append(correct_k.mul_(100.0 / batch_size))
  return res

def train(train_loader, model, optimizer, loss_func, epoch):
    batch_time = 0
    data_time = 0
    losses = 0
    top1 = 0
    top5 = 0
    count = 0
    model.train()

    end = time.time()
    for i, (inp, target) in enumerate(train_loader):
        time_diff = time.time() - end
        data_time = time_diff
        end = time.time()

        target = target.cuda(async=True)
        target = target.long()
        inp = inp.cuda()
    
        inp_var = Variable(inp)
        target_var = Variable(target)
 
        outp = model(inp)
        # print(inp.shape)
        # print(outp.shape)
        # print(target.shape)
        loss = loss_func(outp, target_var)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # print(loss.data)
        losses = loss.data.item()
        top1, top5 = accuracy(outp.data, target, topk=(1, 5))

        time_diff = time.time() - end

        batch_time = time_diff
        end = time.time()
        # if i%1000 == 0:
        #     print(i)

        total_time = batch_time + data_time
        print("epoch: {}, i: {}, total_time: {}, batch_time; {}, data_time: {}, losses: {}, top1: {}, top5: {}".format(epoch, i, total_time, batch_time, data_time, losses, top1, top5))

    return top1, losses

# could add seed initializer to add same seed for all random number generators
# used to have reproducibility of result

train_dataset = TensorDataset(train_x_tensor, train_y_tensor)
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=workers, pin_memory=True)

net = simplenet(num_classes)

loss_func = torch.nn.CrossEntropyLoss()

net = torch.nn.DataParallel(net)

optimizer = torch.optim.Adadelta(net.parameters(), lr=0.1, rho=0.9, eps=1e-3, weight_decay=0.001)

milestones = [10, 20, 30, 35, 40, 45]
scheduler = lr_scheduler.MultiStepLR(optimizer, milestones, gamma=0.1)

net.cuda()
loss_func.cuda()

import time
start_time = time.time()

for epoch in range(epochs):
    current_lr = float(scheduler.get_lr()[-1])
    scheduler.step()

    train_acc, train_los = train(train_loader, net, optimizer, loss_func, epoch)

end_time = time.time()
print("Total time taken: ", end_time - start_time)

# del(train_x_tensor)
# del(train_y_tensor)
net.eval()
outlist = []
test_dataset = TensorDataset(test_x_tensor)
test_loader = DataLoader(test_dataset, batch_size=batch_size, num_workers=workers, pin_memory=True)
for i, inp in enumerate(test_loader):
    # print(inp[0].shape)
    out = net(inp[0])
    _, mi = torch.max(out, 1)
    # print(out)
    # print(out.shape)
    # print(mi)
    # print(mi.shape)
    # for i in range(out.shape[0]):
    for item in mi:
        outlist.append(item.item())
    # print(len(outlist))


np.savetxt(sys.argv[3], np.array(outlist), fmt='%i')