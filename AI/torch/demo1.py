import torch
import numpy as np
import random

def test01():
  # 创建张量标量
  data = torch.tensor(10)
  print(data)

  # numpy 数组，由于data为 float64
  data = np.random.randn(2, 3)
  data = torch.tensor(data)
  print(data)


if __name__ == '__main__':
  test01()