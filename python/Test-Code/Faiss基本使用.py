from operator import index

import faiss
import numpy as np

# 基本操作
def test01():

    # 1. 创建索引

    # 指定存储的向量维度
    # index = faiss.IndexFlatL2(256) # 线性搜索Flat，L2表示相似度计算是欧氏距离
    # index = faiss.IndexFlatIP(256) # 线性搜索，IP 点积相似度，点积值越大，越相似。

    # 工厂方法创建索引
    # index = faiss.index_factory(256, 'Flat', faiss.METRIC_L2)
    index = faiss.index_factory(256, 'Flat', faiss.METRIC_INNER_PRODUCT)


    # 2. 添加向量
    vectors = np.random.rand(10000, 256)
    index.add(vectors)

    # 3. 搜索向量
    query = np.random.rand(2, 256)
    D, I = index.search(query, k=2)
    # print(D)
    # print(I)


    # 4. 删除向量
    index.remove_ids(np.array([1,2,3]))
    # print(index.ntotal)

    index.reset() # 删除全部向量

    # 5. 存储索引
    faiss.write_index(index, 'vectors.faiss')


    # 6 .加载索引
    index = faiss.read_index('vectors.faiss')
    print(index)
    pass



# ID 映射
def test02():

    # 创建索引
    index = faiss.IndexFlatIP(256)
    # ID自定义指定
    index = faiss.IndexIDMap(index)

    vectors = np.random.rand(10000, 256)
    # 有的索引是没有实现add_with_ids方法，所以需要提供一个IndexIDMap ID索引映射，有的有这个方法的实现的话，直接使用方法即可
    index.add_with_ids(vectors, np.arange(10000, 20000))

    index.remove_ids(np.array([0, 1, 2]))
    index.remove_ids(np.array([10000, 1, 2]))

    print(index.ntotal)


    #

if __name__ == '__main__':
    test01()