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

