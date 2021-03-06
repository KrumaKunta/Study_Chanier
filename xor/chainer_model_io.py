# coding: UTF-8

# Chainerを使ってXORを学習する
# 重みをエクスポート，インポート

import argparse
import six.moves.cPickle as pickle

import chainer
import chainer.functions as F
from chainer import optimizers
import numpy as np

np.random.seed(0)

TIME = 2000
middle_units = 2

# ネットワークモデル
parser = argparse.ArgumentParser(description='Chainer example: XOR')
parser.add_argument('--model', '-m', default=0, help ='Trained Model')
args = parser.parse_args()

if args.model != 0:
  model = pickle.load(open(args.model, 'rb'))
else:
  model = chainer.FunctionSet(l1=F.Linear(2, middle_units),
                              l2=F.Linear(middle_units, 1))

def forward(x_data, y_data):
  x = chainer.Variable(x_data)
  y = chainer.Variable(y_data)
  X1 = model.l1(x)
  out1 = F.sigmoid(X1)
  X2 = model.l2(out1)
  out2 = F.sigmoid(X2)
  return F.mean_squared_error(out2, y), out2

x_train = np.array([[0,0], [0,1], [1,0], [1,1]], dtype=np.float32)
y_train = np.array([[0], [1], [1], [0]], dtype=np.float32)
datasize = len(x_train)

optimizer = optimizers.SGD(lr=0.1)
optimizer.setup(model)

for epoch in range(TIME):
  sum = np.zeros(())
  optimizer.zero_grads()
  loss, out = forward(x_train, y_train)
  sum += loss.data.reshape(())

  loss.backward()
  optimizer.update()

  if ((epoch) % 1000) == 0:
    print('Epoch %d: Error = %f' % (epoch, sum))

print(out.data)

# モデルを保存
if args.model == 0:
  pickle.dump(model, open('model', 'wb'), -1)
