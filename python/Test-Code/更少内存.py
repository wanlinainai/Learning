import os
import time
import faiss
import numpy as np


np.random.seed(0)
vectors = np.random.rand(1000000, 256)
query = np.random.rand(1, 256)

# 1. 使用线性搜索
def test01():
    index = faiss.IndexFlatL2(256)

    index.add(vectors)

    startTime = time.time()
    D, I = index.search(query, k=2)

    print("Time:", time.time() - startTime)

    print(D)
    print(I)

    faiss.write_index(index, "a.faiss")
    print(os.stat('a.faiss').st_size)

# 内存优化
def test02():

    quantizer = faiss.IndexFlatL2(256)

    # 1. 量化参数
    # 2. 向量维度
    # 3. 质心数量
    # 4. 子空间数量，较大的值意味着将原始向量空间划分成更多的子空间进行索引和搜索
    # 5. 聚类的数量，量化码本中码字的位数，每一个段聚类的数量（8位256）
    index = faiss.IndexIVFPQ(quantizer, 256, 100, 128, 8)

    index.nprobe = 10

    index.train(vectors)

    index.add(vectors)

    startTime = time.time()
    D, I = index.search(query, k=2)
    print("Time:", time.time() - startTime)
    print( D)
    print(I)

    faiss.write_index(index, "b.faiss")
    print(os.stat('b.faiss').st_size)


if __name__ == '__main__':
    test01()
    print("-" * 30)
    test02()