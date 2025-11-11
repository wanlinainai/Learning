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

# 2. 使用倒排文件索引
def test02():
    # 量化参数、向量维度、质心数量（几个簇数）
    quantizer = faiss.IndexFlatL2(256) # 局部使用线性方法
    index = faiss.IndexIVFFlat(quantizer, 256, 100)
    # 指定在搜索时，在最相似的前多少个簇中进行线性搜索
    index.nprobe = 10
    index.train(vectors) # 进行一个训练， 得到100个质心（簇数）
    index.add(vectors) # 添加向量， 将向量分配到最近的簇中
    startTime = time.time()
    # 近似的最相近搜索
    D, I = index.search(query, k=2)
    print("Time:", time.time() - startTime)
    print( D)
    print(I)


def test03():
    """
    减少内存存储向量数据库
    :return:
    """
    quantizer = faiss.IndexFlatL2(256)
    # 1. 量化参数
    # 2. 向量维度
    # 3. 质心数量
    # 4. 子空间数量，较大的值意味着将原始向量空间划分成更多的子空间进行索引和搜索
    # 5. 量化码本中码字的位数，每一个段聚类的数量（8位256）
    index = faiss.IndexIVFPQ(quantizer, 256, 100, 256, 100)
    index.nprobe = 4
    data = np.random.rand(10000, 32).astype('float32')
    index.train(data)
    index.add_with_ids(data)

if __name__ == '__main__':
    test01()
    test02()