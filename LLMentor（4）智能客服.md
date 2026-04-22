# 智能客服项目（RAG）

## Java中解析PDF的局限

### 使用Spring AI解析

```java
public void read() {
        PdfReaderStrategy pdfReaderStrategy = new PdfReaderStrategy();
        try {
            List<Document> documents = pdfReaderStrategy.read(new File("D:\\github_repository\\Learning\\resources\\r7-product-manual-20250123.pdf"));
            for (Document document : documents) {
                System.out.println(document.getText());
                System.out.println("=======================");
            }

        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
```

最终的结果：

![image-20260415230733493](images/LLMentor（4）智能客服/image-20260415230733493.png)

可以发现，解析出来的位置完全不可控。

同时图片信息完全没有办法解析出来。

同时存在大量的空白字符。

表格解析出来的内容乱七八糟。![image-20260415230924946](images/LLMentor（4）智能客服/image-20260415230924946.png)

对比：![image-20260415230938492](images/LLMentor（4）智能客服/image-20260415230938492.png)

### 多模态解析

```java
    @Test
    public void readByMultipleFiles() throws Exception {
        String content = pdfMultimodalProcessor.processPdf(new File("D:\\github_repository\\Learning\\resources\\r7-product-manual-20250123.pdf"));
        System.out.println(content);
    }
```

最终解析出来的结果：![image-20260415231239312](images/LLMentor（4）智能客服/image-20260415231239312.png)

可以看出来能够解析出来图片的内容，但是表格的解析存在问题：

![image-20260415231345562](images/LLMentor（4）智能客服/image-20260415231345562.png)

![image-20260415231354611](images/LLMentor（4）智能客服/image-20260415231354611.png)

很明显不知道什么对应什么。

同时还是存在空白字符的问题。

### Langchain4J

使用Langchain4J的时候问题其实依旧，但是结构的问题其实解决了：

![image-20260415231625993](images/LLMentor（4）智能客服/image-20260415231625993.png)

但是空白字符一类的问题依旧。需要解决。

## 使用MinerU解析PDF文档





## chunkSize和overlap设置多少合适？

### 通用起点推荐

RAG系统中没有黄金比例，我们采用的还是和线程池参数类似的方法，先设置一个通用的值，之后从推荐值开始一点一点调整。

chunkSize和overlap指的是字符数量，并不是Token数量。

`chunk_size`一般设置512或者1024个Token，部分模型的Token数量是512 的限制，比如：bge-small-zh，百炼上的text-embeding-v3、v4都是8092个Token的大小。

>一个Token大概是在1.5 - 2 个汉字之间，在3 - 4个英文字符之间。如果是纯中文文本的话，大概初始值设置成500-1000左右的chunkSize，英文的话是2000-3000左右的chunkSize

overlap的话大概按照chunkSize的10%-20%比例。

- `chunk_size`太小，容易导致语义的碎片化，丢失关键上下文。（虽然说用了父子分片能够缓解这个现象，但是可能出现上下文太长的问题）
- `chunk_size`太大，会包含太多的无关信息，稀释核心的语义，降低检索的精准度，增加成本。
- `overlap`为0，极易出现在切分边界丢失信息，导致相邻的语义块断裂。

### 按照文档类型调整

![image-20260421235605828](images/LLMentor（4）智能客服/image-20260421235605828.png)

### 项目中的分段方式

