# LLMentor（2）RAG

## RAG

### 主要流程

主要分成了两步，一步是构建索引，第二步是检索生成。

第一步索引构建步骤是：在处理索引构建的时候需要注意一个原则：Garbage in, Garbage out（GIGO）。垃圾进垃圾出。由此可见原始数据准确度的正确性。

**原始数据** --预处理--> **文本块** --向量化--> **向量模型** --存储--> **向量数据库**

第二步是检索生成，步骤是：

**用户提问** ----> **提示词** ----> **向量模型** ----> **向量数据库**

​                |

​                |

​				大模型 -----> 生成相关回答

用户提问的时候，根据用户的提示词实时处理用户的问题。首先需要从知识库中匹配出与用户问题相关的**最相似文本块(chunk)**。

## RAG-索引构建

索引构建的开始是：文档

索引构建的结束是：索引

### 文档预处理

文档预处理主要就是将原始文档进行加载、解析，并转成能够统一处理的标准化格式。

首先要做的就是按照不同的文档类型进行加载并转成统一格式的Document，之后还需要去除文档中存在的大量的无效的内容。比如多余的空格、换行符、无意义的特殊符号、重复的内容等等；最后还需要规范化文本格式，例如统一的编码格式、统一大小写等等。

**预处理的目标就是让后续的“分片”和“向量化”能够在干净的数据上进行操作，从源头保证知识库的索引的质量**

### 文档的分片

分片指的就是将文档拆分成多个片段。我们的大模型是存在上下文限制的。需要按照一定的规则切分成较小的文本片段（chunk）。

#### 有哪一些分片的方式

常规的方式有：固定大小分片、递归分片（按照特殊的符号分片）、文档分片、语义分片、智能分片等等。不管是哪一种方式，最终的结果都是将文档切分成多个文本块（Chunk）。

如果Chunk太长了会产生什么问题呢？

1. 一个chunk包含多个内容，与查询相关的内容的部分被无关的内容“淹没”，降低检索的相关性得分。
2. 生成阶段将整个chunk输入到LLM，但是其中的大部分内容无用，挤兑有效的上下文空间。

如果chunk太短会产生什么问题呢？

1. 关键的信息被切断，导致单个chunk语义不完整。
2. LLM缺少足够的上下文，可能误解片段的含义，产生幻觉。

### 向量化

文档切分 + 分片完成之后，每一个分片块都需要被转换成一个高维的数值的向量，这个过程就是向量化。向量化的目的就是：**让文本的语义可以被“机器理解”和“相似度比较”**。

#### 文本块如何变成向量

这个过程叫做**Embedding**，简单来说就是将一个文本投影到高维向量空间里。每一个方向都是代表了文本在某一个“语义方向”的权重，比如：

- 一维：是否包含人物。
- 二维：是否涉及到动作。
- 三维：是否包含时间。
- .....

最终，每一段文字被转成一个高维坐标点，然后就可以进行数学上的比较了。

#### 向量的相似度比较

三种方法：

- **余弦相似度**：计算夹角，查看两个夹角的方向是否接近。夹角越小，向量同方向，语义越相似。

- **欧氏距离**：空间中两点的直线距离。距离越小，相似度越高，主要应用于具有几何意义的场景。
- **点积**：两个向量在同一个方向的重叠程度。值越大，向量越相似，**transformer**注意力机制就是使用了点积来计算权重值。

用的最多的就是**余弦相似度**

### 生成索引

当我们完成了向量化之后，每一个Chunk都对应了一个高维向量，但是如果这些向量只是存储在内存中的话，并不能快速的查找和比较。所以需要将恩本内容和高维向量**持久化存储**下来。利用我们的**向量数据库构建索引结构**。并为后续的检索生成提供相似度查询的功能。

#### 向量数据库

向量数据库是一类专门用于存储、管理和检索**高维向量数据**的数据库。与传统数据库不同，并不是基于精确匹配进行查询，而是通过计算向量之间的相似度进行**”语义检索“**。

**存储了哪一些信息？**
以PGVector为例子。

![image-20260329152942978](images/LLMentor（2）RAG/image-20260329152942978.png)

主要就是：**embedding_id、embedding、text、metadata**几个字段。

高维向量embedding：表示存储的向量数据。

text：表示原始的文本信息。

matadata：元数据。检索的时候可以进行精确的过滤、分组或追溯来源。如文件名过滤、时间戳过滤等，在某一些条件下检索更加精准。

## RAG-检索生成

### 用户提问

起点。用户提出了一个问题或者请求。这个查询将作为后续检索和生成的起点。

### 内容召回

如何从知识库中找到与用户提问最相关的Chunk。

检索的方式有很多，如：

- 向量相似度检索：将用户的问题进行向量化（Embedding），得到用户问题的向量语义表示，之后在向量数据库中通过余弦相似度或点积进行相似度查询，找到一系列最相似的文本块。检索的结果通常是:**top-k**个。
- 混合检索：将关键词检索和相似度检索进行整合：
  - BM25/ES（关键词检索，保证精确匹配，获取核心关键内容）；
  - 向量相似度检索（语义检索，保证相似度，捕捉语义相似内容）。

**通过混合检索**：可以让系统在”查的广“和”查的准“之间取得平衡，让系统既能理解语义，又能保证检索的准确性和可靠性。

**重排序**：之前的操作都是”**粗召回**“，这时候可以再使用一个轻量模型（cross-encoder）对这些粗召回的文本块重新打分排序，理解成”**精筛选**“。将最相关的文本块挑选出来，去除排名靠后的文本块，这样的操作，可以让最终进入提示词的文档更加精准。

### 上下文融合

内容召回指的是找到与用户问题最相关的一些资料，真正让大模型生成回答的关键在于：**如何让大模型正确使用这些资料生成答案**。这一步一般是通过Promt来实现。

```markdown
根据以下的信息回答问题：
[检索结果1]： ...
[检索结果2]： ...

问题：2025年总预约人数是多少？
```

这个增强之后的提示将作为生成模型的输入。



### 内容的生成

拿到上下文融合的提示词之后，就可以让大模型回答问题了。因为大模型能够借助这个**”知识外挂“**回答问题了，有效的减少大模型的输出幻觉。

除此之外，RAG中的Metadata也可以在此处体现真正的作用，比如我们在metadata中设计了文件名、参考链接等，那么这边的大模型在生成答案的时候，在回答中就可以附带引用来源和参考链接，提升回答的可信度。

## LlamaIndex 构建 RAG

- 数据索引的构建：支持各种格式的数据（PDF、word等）转成LLM可理解的索引结构。
- 高效检索：
- 与LLM无缝集成
- 支持多种数据源格式
- 模块化可扩展

解决了LLM的幻觉问题、打通了私有数据与通用LLM、简化RAg的架构开发。

### 使用UV构建一个简单的RAG

```shell
uv init llamaindex_test
cd llamaindex_test
uv venv
source .venv/bin/activate
```

```python
from  llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.embeddings.dashscope import DashScopeEmbedding
from llama_index.llms.dashscope import DashScope
import os

DASHSCOPE_API_KEY = "sk-*****"

# 1. 加载文档（）
documents = SimpleDirectoryReader("data").load_data()

# 2. 设置向量模型
embedding_model = DashScopeEmbedding(model_name="text-embedding-v2",api_key=DASHSCOPE_API_KEY)

# 3. 设置LLM
llm = DashScope(model_name="qwen-max", temperature=0.1, api_key=DASHSCOPE_API_KEY)

# 4 构建索引
index = VectorStoreIndex.from_documents(documents, embed_model=embedding_model)

# 5 创建查询引擎
query_engine = index.as_query_engine(llm=llm)

response = query_engine.query("请分析一下这篇文档的主要内容")
print(response)

def main():
    print("Hello from llamaindex-test!")


if __name__ == "__main__":
    main()
```

需要添加uv相关依赖。

```shell
uv add llama-index llama-index-llms-dashscope llama-index-embeddings-dashscope
```

执行代码：

![image-20260403134642919](LLMentor（2）RAG/image-20260403134642919.png)

### 问题

尽管实现了一个简单的RAG，但是如果想要在生产环境中使用的话还需要考虑更多的因素：

- chunking 分块的策略优化
- 使用持久化向量数据库
- 查询优化
- 文件检索优化
- 对话记忆
- 重排序
- 混合检索
- 多模态
- RAG效果评估

## 文档预处理

预处理的目标是让后续的分片和向量化能够在干净的数据上进行，从源头保证知识库索引的质量。

主要包含了两个步骤：**文档读取**和**数据清洗**。

文档读取就是将不同格式的文档处理成统一的标准化的可供解析的格式。Spring AI已经存在了一个DocumentReader接口。统一的接口，其中存在多种实现。

- TextReader（TXT）
- JsonReader（JSON）
- PagePdfDocumentReader/ ParagraphPdfDocumentReader（PDF格式）
- MarkdownDocumentReader（Markdown）
- JsoupDocumentReader（HTML）
- TikaDocumentReader（几乎通用）

代码文件参考：[github](https://github.com/wanlinainai/LLMentor/tree/main/rag/src/main/java/com/zxh/llm/llmentor/rag/reader)

上述的方式已经能够成功读取到文件，但是数据可能存在干扰，需要数据清洗。将多余的空格、换行符号、无意义的特殊符号和重复内容进行处理。

```java
    public List<Document> cleanDocuments(List<Document> documents) {
        if (CollectionUtils.isEmpty(documents)) {
            return documents;
        }
        return documents.stream().map(doc -> {
            if (doc == null || doc.getText() == null) {
                return doc;
            }
            String text = doc.getText();
            text = text.replaceAll("\\s+"," ").trim();

            // 去除无意义的乱码
            text = text.replaceAll("[^\\p{L}\\p{N}\\p{P}\\p{Z}\\n]", "");
            
            text = text.toLowerCase();

            String[] paragraphs = text.split("\\n+");
            HashSet<String> seen = new LinkedHashSet<>();
            for (String paragraph : paragraphs) {
                String trimmed = paragraph.trim();
                if (!seen.isEmpty()) {
                    seen.add(trimmed);
                }
            }
            
            text = String.join("\n", seen);
            return new Document(text);
        })
                .collect(Collectors.toList());
    }
```

