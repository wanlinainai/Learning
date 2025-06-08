# Ai 超级智能体

## 项目介绍

### 大纲-项目优势

掌握知识:

- AI 应用平台的使用
- 接入AI大模型
- AI开发框架（SpringAI + LangChain4j）
- AI大模型本地部署
- Prompt工程和优化技巧
- 多模态特性
- SpringAI 核心特性：自定义拦截器、上下文持久化、结构化输出
- RAG知识库和向量数据库
- Tool Calling 工具调用
- MCP模型上下文协议和服务开发
- AI智能体Manus原理和自主开发
- AI服务化和Serverless部署

除此之外，还有其他的优势：

- AI云平台和编程双端实战，不仅仅会用AI服务，还要会自己写。
- 基于官方文档讲解最新的AI技术，细致入微，手撕文档和源码。
- 分享大量的AI扩展知识和编程技巧，掌握最佳实践

### 项目功能梳理

我们开发一个AI恋爱智能应用、一个拥有自主规划能力的超级智能体，以及一系列的工具Tools和MCP服务。

具体的需求如下：

- AI恋爱大师应用：用户在恋爱过程中难免会遇到各种各样的问题，我们可以让AI为用户提供贴心、友爱、有用的情感以及其他指导。支持多轮对话、对话记忆持久化、RAG知识库检索、工具调用、MCP服务调用。
- AI超级智能体：可以根据用户的需求，自主推理和行动、直到完成目标。
- 提供给AI的工具：联网搜索、文件操作、网页抓取、资源下载、终端操作、PDF生成。
- AI MCP服务：可以从特定的网站搜索。

![image-20250429225605195](images/Ai 超级智能体/image-20250429225605195.png)

### 技术选型

项目以SpringAI开发框架为核心，涉及到多种主流的AI客户端和工具库的使用。

- java21 + SpringBoot 3框架
- RAG知识库
- PGvector向量数据库
- Tool Calling工具调用
- MCP 模型上下文协议
- React Agent智能体的构建
- ServerLess计算服务
- AI 大模型开发平台百炼
- Cursor AI代码生成 + MCP 
- 第三方接口：如SearchAPI/Pexels API（后者是一个免费的图片素材网，原图素材）
- Ollama大模型部署
- Kryo高性能序列化
- Jsoup网页抓取
- iText PDF生成
- Knife4J 接口文档

### 架构图

![image-20250429230432194](images/Ai 超级智能体/image-20250429230432194.png)

## AI 大模型接入

### 大模型概念

#### 什么是AI大模型？

AI大模型指的是具有超大规模参数（通常是十亿到数万亿）的深度学习模型。通过对大模型数据的训练，能够理解、生成人类语言，处理图像、音频等多种模态数据。

大模型的强大之处在于他的**涌现能力**，随着模型参数数量和训练数据集的增加，模型会展现出训练过程中未明确赋予的新能力，比如逻辑推理、代码编写、多步骤问题解决等。

![image-20250607003057975](images/Ai 超级智能体/image-20250607003057975.png)

大模型百花齐放，举一些例子：

OpenAI

- GPT-4o（多模态）
- GPT-4（文本 + 图像）
- GPT-3.5（处理文本）

Anthropic

- Claude 3、4系列（Opus，Sonnet，Haiku，由强到弱）

Google

- Gemini Ultra/Pro/Nano（支持多模态）

Meta

- Llama 3（开源，70B和8B参数版本）
- Llama 2（开源，多种参数规模）

国内

- 百度文心一言（LJ）
- 阿里通义千问
- 字节豆包
- 科大讯飞星火

#### AI大模型分类

1. 按模态分类
   - 单模态模型：只能处理单一类型的数据，如纯文本
   - 多模态模型：可处理多种类型的信息
2. 开源性分类
   - **闭源模型**：不公开模型权重和训练方法
   - 代表：GPT、Claude、Gemini
   - 特点：通常是使用API访问，付费使用
   - **开源模型**：公开模型权重，允许下载和自行部署
   - 代表：Llama系列、Mistral、Falcon
   - 可以本地部署、自由调整，但是通常能逊色于闭源的模型
3. 按规模分类
   - **超大规模（千亿到数万亿）**
   - 代表：GPT-4
   - 特点：能力强大，但是需要大量的计算资源
   - **中小规模模型（几十亿到几百亿）**
   - 代表：Llama 3（70B）、Mistral（7B）
   - 特点：可在普通硬件上运行，适合特定任务的精调
4. 按用途分类

	- **通用模型**：能处理广泛任务
	- 代表：GPT-4、Claude 3、Gemini
	- **特定领域模型：**针对于特定领域进行优化
	- 医疗：Med-PaLM 2
	- 代码：CodeLlama、StarCoder
	- 科学：Galactica

#### 对比不同的模型选择

可参考Langchain4J:https://docs.langchain4j.dev/integrations/language-models/

Spring AI 大模型的对比文档：https://docs.spring.io/spring-ai/reference/api/chat/comparison.html

### 接入AI大模型

#### 使用大模型的两种途径

实际开发过程中，我们主要有2种途径来使用大模型，**云服务和自部署**各有优缺。

**云服务**

直接使用云厂商在云端已经部署好的大模型服务，无需自己考虑基础设施。

**自部署**

开发者自己在本地或或私有云环境部署开源的大模型，特点是：

- 完全控制数据流，更高的数据隐私保障
- 根据特定需求进行微调模型和定制模型
- 无网络延迟，适合对响应速度有着严格要求的场景
- 一次性成本太高，需要专业的技术团队维护
- 适合企业级应用和对数据安全有严格要求的场景

#### 接入大模型的3种方式

**1、AI应用平台接入**

通过云服务商提供的AI应用平台来使用AI大模型

以

[阿里云百炼]: https://bailian.console.aliyun.com/#/home	"阿里云百炼"

为例，这是一站式的大模型开发以及应用构建平台，他提供了从模型微调到应用构建的全流程支持。

不论是专业的开发人员还是业务人员都可以通过简单的界面操作，在5MIN内开发一款大模型应用。或者在几个小时内训练出专属的模型。

![image-20250607113227780](Ai 超级智能体/image-20250607113227780.png)

可能在使用这个产品的时候，会遇到另一个产品，DashScope（模型服务灵积），灵积是一个API调用的服务，之后的开发工作绝大多数会与灵积打交道。

利用aliyun百炼我们可以轻松的搭建AI大模型和构建AI应用。

1）创建自己的AI应用，支持智能体、工作流和智能体编排应用。

没有2）。

**2、AI软件客户端接入**

除了平台之外，还可以通过AI软件客户端来使用大模型能力，推荐两个应用：

1）Cherry Studio：一款集多模型对话、知识库管理、AI绘画、翻译等功能于一体的全能AI助手平台。Cherry Studio提供高度自定义的设计、强大的扩展能力和有好的用户体验。

2）Cursor：AI编程必备工具。在本项目中也会采用Cursor生成前端项目代码。

**3、程序接入**

调用大模型分成2种方式：

1. 直接调用大模型的API，比如直接调用Deepseek（更加原生）
2. 调用大模型平台创建的应用或者智能体（更方便）

第一种方式，使用特定平台提供的SDK或API，参考平台的文档来进行接入；也可以使用AI开发框架，比如Spring AI、SpringAI Alibaba、LangChain4J等自主选择大模型进行调用，可以灵活切换使用的大模型几乎不需要修改代码。

```yaml
spring: 
   ai: 
      dashscope:
          api-key: ${AI_DASHSCOPE_API_KEY}
          chat: 
          	options:
          		model: deepseek-r1
```

第二种方式，一般只能使用特定平台的SDK和API，参考平台介入文档来使用。

如果是个人的小项目，第二种方式肯能会更方便，因为把大多数应用构建的操作都放在了云端可视化平台而不是通过编程来实现；但是如果是企业项目的话，更推荐第一种方式，直接用Spring AI 等开发框架调用AI 大模型。

### 后端项目初始化

#### 环境准备

安装的JDK必须是17或21，不能用其他版本，因为项目使用的是SpringBoot3和Spring AI开发框架

推荐使用21版本，有虚拟线程这个王炸的功能。

##### pom.xml

基础的依赖：

```xml
<dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>

        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <version>1.18.36</version>
            <optional>true</optional>
        </dependency>

        <dependency>
            <groupId>cn.hutool</groupId>
            <artifactId>hutool-all</artifactId>
            <version>5.8.37</version>
        </dependency>

        <dependency>
            <groupId>com.github.xiaoymin</groupId>
            <artifactId>knife4j-openapi3-jakarta-spring-boot-starter</artifactId>
            <version>4.4.0</version>
        </dependency>

        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
```

#### 程序调用AI 大模型

实际开发过程中，有很多种方式可以用来调用AI大模型。以下是4种主流的接入方式，并通过示例代码展示如何在项目中使用交互。

1. SDK接入：使用官方提供的SDK，查看文档即可
2. HTTP接入：通过REST API 直接发送HTTP 请求调用模型
3. Spring AI：基于Spring的生态，更加方便的接入大模型
4. LangChain4J：专注于构建LLM应用的Java框架，提供丰富的AI调用组件

本文选用阿里云百炼平台进行构建。

##### 1、SDK接入

###### 1）按照官方文档安装SDK：https://help.aliyun.com/zh/model-studio/install-sdk/

在选择SDK的时候需要注意Maven版本。

pom.xml文件中添加依赖：

```xml
     <dependency>
            <groupId>com.alibaba</groupId>
            <artifactId>dashscope-sdk-java</artifactId>
            <version>2.18.2</version>
        </dependency>
```

###### 2）先在百炼平台申请一个API Key

###### 3） 项目中新建`demo.invoke`包，集中存放调用AI大模型的实例代码

具体的方式可以参考文档：https://help.aliyun.com/zh/model-studio/use-qwen-by-calling-api#ab9194e9a55dk

![image-20250608222116870](images/Ai 超级智能体/image-20250608222116870.png)

测试中，为了安全，我们将API Key保存在接口类中。

```java
public interface TestApiKey {

    String API_KEY = "";
}
```

使用SDK 调用模型的完整示例代码

```java

public class SdkAiInvoke {

    public static GenerationResult callWithMessage() throws ApiException, NoApiKeyException, InputRequiredException {
        Generation gen = new Generation();
        Message systemMsg = Message.builder()
                .role(Role.SYSTEM.getValue())
                .content("You are a helpful assistant.")
                .build();
        Message userMsg = Message.builder()
                .role(Role.USER.getValue())
                .content("你是谁？")
                .build();
        GenerationParam param = GenerationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                .apiKey(TestApiKey.API_KEY)
                // 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
                .model("qwen-plus")
                .messages(Arrays.asList(systemMsg, userMsg))
                .resultFormat(GenerationParam.ResultFormat.MESSAGE)
                .build();
        return gen.call(param);
    }

    public static void main(String[] args) {
        try {
            GenerationResult result = callWithMessage();
            System.out.println(JsonUtils.toJson(result));
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            // 使用日志框架记录异常信息
            System.err.println("An error occurred while calling the generation service: " + e.getMessage());
        }
        System.exit(0);
    }
}
```

###### 4）运行项目，成功看到AI的回复

![image-20250608222328609](images/Ai 超级智能体/image-20250608222328609.png)

#### HTTP接入

有一些模型并没有提供SDK接入的方式，那么如果执着使用的话，只能通过HTTP请求了。

依旧参考文档：

![image-20250608222620696](images/Ai 超级智能体/image-20250608222620696.png)

可以将上述发送请求的代码换成对应的java、GoLang等代码，如果觉得浪费时间，直接使用AI生成，提示Prompt:

```shell
将上述请求转换为 hutool 工具类的请求代码
```

生成代码如下：

```java
public class HttpAiInvoke {
    public static void main(String[] args) {
        // 替换为你的实际 API 密钥
        String url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation";

        // 设置请求头
        Map<String, String> headers = new HashMap<>();
        headers.put("Authorization", "Bearer " + TestApiKey.API_KEY);
        headers.put("Content-Type", "application/json");

        // 设置请求体
        JSONObject requestBody = new JSONObject();
        requestBody.put("model", "qwen-plus");

        JSONObject input = new JSONObject();
        JSONObject[] messages = new JSONObject[2];

        JSONObject systemMessage = new JSONObject();
        systemMessage.put("role", "system");
        systemMessage.put("content", "You are a helpful assistant.");
        messages[0] = systemMessage;

        JSONObject userMessage = new JSONObject();
        userMessage.put("role", "user");
        userMessage.put("content", "你是谁？");
        messages[1] = userMessage;

        input.put("messages", messages);
        requestBody.put("input", input);

        JSONObject parameters = new JSONObject();
        parameters.put("result_format", "message");
        requestBody.put("parameters", parameters);

        // 发送请求
        HttpResponse response = HttpRequest.post(url)
                .addHeaders(headers)
                .body(requestBody.toString())
                .execute();

        // 处理响应
        if (response.isOk()) {
            System.out.println("请求成功，响应内容：");
            System.out.println(response.body());
        } else {
            System.out.println("请求失败，状态码：" + response.getStatus());
            System.out.println("响应内容：" + response.body());
        }
    }
}
```

#### Spring AI

Spring AI是Spring生态系统的新成员，旨在简化AI功能与Spring应用的集成。SpringAI通过提供统一接口、支持集成多种AI服务提供商和模型类型、各种AI开发常用特性（RAG知识库、Tools工具调用和MCP模型上文协议），简化了应用开发代码，使得开发者能够专注于业务逻辑，提高了开发效率。

Spring AI默认没有支持国内的模型，更多的是支持兼容OpenAI API 的大模型的集成，可以参考官方的模型对比。如果要使用阿里系的大模型，建议直接使用阿里自主封装的Spring AI Alibaba框架（https://java2ai.com/docs/1.0.0-M6.1/overview/?spm=4347728f.6476bf87.0.0.a3c1556bpqZcox）。

1） 引入依赖

```xml
    <dependency>
            <groupId>com.alibaba.cloud.ai</groupId>
            <artifactId>spring-ai-alibaba-starter</artifactId>
            <version>1.0.0-M6.1</version>
        </dependency>

    <repositories>
        <repository>
            <id>spring-milestones</id>
            <name>Spring Milestones</name>
            <url>https://repo.spring.io/milestone</url>
            <snapshots>
                <enabled>false</enabled>
            </snapshots>
        </repository>
    </repositories>
```

2）编写配置类：

application-local.yml

```yaml
spring:
  application:
    name: spring-ai-alibaba-qwq-chat-client-example
  ai:
    dashscope:
      api-key: ********
      chat:
        options:
          model: qwen-plus
```

3）编写实例代码，注意要注入`dashscopeChatModel`：

```java
@Component
public class SpringAiAiInvoke implements CommandLineRunner {
    @Resource
    private ChatModel dashscopeChatModel;
    @Override
    public void run(String... args) throws Exception {
        AssistantMessage output = dashscopeChatModel.call(new Prompt("你好，我是林彪，请帮我写一周关于6月4号的七言绝句"))
                .getResult()
                .getOutput();
        System.out.println(output.getText());
    }
}
```

上述代码实现了`CommandLineRunner`接口，我们启动Spring Boot项目时，会自动注入大模型ChatModel依赖，并单词执行该类的run方法，达到测试的效果。

![image-20250608224723624](images/Ai 超级智能体/image-20250608224723624.png)

上述代码中我们是通过使用ChatModel的方式调用大模型，适合于简单的对话场景，除了这种方式还有ChatClient方式，提供更多的高级功能（对话记忆），适合负责场景，在后续的AI应用开发章节会有详细介绍。

#### LangChain4j

和Spring AI的作用一致，langchain4j是没有支持阿里系的大模型的，只能使用社区版本的大模型包。

要接入阿里云灵积模型，参考https://docs.langchain4j.dev/integrations/language-models/dashscope/

1）首先引入依赖

```xml
<!-- https://mvnrepository.com/artifact/dev.langchain4j/langchain4j-community-dashscope -->
<dependency>
    <groupId>dev.langchain4j</groupId>
    <artifactId>langchain4j-community-dashscope</artifactId>
    <version>1.0.0-beta2</version>
</dependency>
```

2）参考文档来编写实例对话代码，创建了一个ChatModel并调用

```java
public class LangChainAiInvoke {

    public static void main(String[] args) {
        ChatLanguageModel qwenModel = QwenChatModel.builder()
                .apiKey(TestApiKey.API_KEY)
                .modelName("qwen-max")
                .build();
        String answer = qwenModel.chat("你好");
        System.out.println(answer);
    }
}
```

#### 总结

推荐使用Spring AI，一方面是属于Spring生态，另一个方面是简单易用，利于学习。

#### 扩展

如果需要进行本地部署的话，使用ollama进行处理。

可以直接参考ollama官网进行下载安装

```shell
ollama run deepseek-r1:1.5b
```

后端中引入依赖：

```xml
        <dependency>
            <groupId>org.springframework.ai</groupId>
            <artifactId>spring-ai-ollama-spring-boot-starter</artifactId>
            <version>1.0.0-M6</version>
        </dependency>

<repositories>
   <repository>
            <id>spring-milestones</id>
            <name>Spring Milestones</name>
            <url>https://repo.spring.io/milestone</url>
            <snapshots>
                <enabled>false</enabled>
            </snapshots>
        </repository>
  </repositories>
```

配置文件：

```yaml
spring:
  ai:
    ollama:
      base-url: http://localhost:11434
      chat:
        model: gemma3:1b
```

新建一个invoke类

```java
@Component
public class OllamaAiInvoke implements CommandLineRunner {

    @Resource
    private ChatModel ollamaChatModel;
    @Override
    public void run(String... args) throws Exception {
        AssistantMessage output = ollamaChatModel.call(new Prompt("你好，我是李白，请帮我生成一段诗歌，必须是七言绝句"))
                .getResult()
                .getOutput();
        System.out.println(output.getText());
    }
}
```

启动成功之后即可。











