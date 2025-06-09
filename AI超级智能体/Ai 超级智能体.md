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

## AI应用开发

### Prompt工程

#### 基本概念

Prompt工程又称为提示词工程，简而言之就是输入给AI指令。那为什么叫做“工程”呢？

因为利用AI生成的内容是不确定的，构建一个能够按照预期生成内容的提示词是一门艺术，也是一门科学。提示词的质量会直接影响到AI大模型的输出结果。

#### 提示词分类

**核心-基于角色分类**

在AI对话中，基于角色分类是最常见的，通常存在三种主要类型的Prompt：

1）用户Prompt（User Prompt）：这是用户向AI提供的实际问题、指令和信息，传达了用户的直接需求

```shell
用户：帮我生成一篇关于春天的短诗
```

2）系统Prompt（System Prompt）：这是设置AI大模型行为规则和角色定位的隐藏指令，用户通常不能直接看到。系统Prompt相当于告诉AI设定人格和能力边界，即告诉AI“你是谁？你能做什么？”

```shell
系统：你是一位经验丰富的法律顾问，擅长分析各种复杂的案情，请以专业的角度回答用户的问题，必要时需要主动询问更多信息以提供更加准确的建议，不作出道德判断，尊重用户的提出所有的案子。
```

不同的系统Prompt可以让同一个AI模型表现出完全不同的应用特性，这是构建垂直领域AI应用（财务顾问、教育辅导、医疗咨询）等的关键。

3）助手Prompt（Assistant Prompt）：这是AI模型响应内容，在多轮对话中，之前的助手回复也会成为当前上下文的一部分，影响后续对话的理解和生成，某一些场景下，开发者可以主动预设一些助手消息作为对话历史的一部分，引导后续执行

```shell
助手：我是你的恋爱顾问，很高兴能帮助你解决情感问题。你目前遇到了什么恋爱困惑呢？可以告诉我你的现状和具体遇到的情况。
```

在实际应用中，这些不同类型的提示词往往会组合使用。

```shell
系统：你是编程导航的专业编程导师，擅长引导初学者入门编程并制定学习路径。使用友好鼓励的语气，解释复杂概念时要通俗易懂，适当使用比喻让新手理解，避免过于晦涩的技术术语。

用户：我完全没有编程基础，想学习编程开发，但不知道从何开始，能给我一些建议吗？

助手：欢迎加入编程的世界！作为编程小白，建议你可以按照以下步骤开始学习之旅...

【多轮对话继续】
```

大模型平台支持用户自主设置各种不同类型的提示词来进行调试。

![image-20250609221304624](images/Ai 超级智能体/image-20250609221304624.png)

**基于功能的分类**

除了基于角色的分类外，我们还可以从功能角度出发，对提示词进行分类。

1）指令型提示词：明确告知AI需要执行什么任务，通常是以命令式语句开头。

```shell
翻译以下文本为英文：春天来了，花儿开了。
```

2）对话型提示词：模拟自然语言，问答的形式与AI模型交互。

```shell
你认为人工智能会在未来取代人类工作吗？
```

3）创意型提示词：引导AI大模型进行创意内容生成，如故事、诗歌、广告文案等。

```shell
写一个发生在未来太空殖民地的短篇科幻故事，主角是一位机器人工程师。
```

4）角色扮演提示词：让AI扮演特定角色或人物进行回答。

```shell
假设你是爱因斯坦，如何用简单的语言解释相对论？
```

5）少样本学习提示词：提供一些示例，引导AI理解所需要的输出格式和风格。

```sehll
将以下句子改写为正式商务语言：
示例1：
原句：这个想法不错。
改写：该提案展现了相当的潜力和创新性。

示例2：
原句：我们明天见。
改写：期待明日与您会面，继续我们的商务讨论。

现在请改写：这个价格太高了。
```

#### Token

**如何计算Token？**

对于不同的大模型对于Token的划分规则略有不同，比如根据OpenAI的文档：

- 英文文本：一个Token大约是4个字符或者0.75个英文单词
- 中文文本：一个汉字一般是一到两个Token
- 空格和标点：也会计入Token使用量
- 特殊符号和表情符号：需要更多的token

### 应用方案设计

整体方案围绕着2个核心展开

- 系统提示词的优化
- 多轮对话的实现

#### 1、系统提示词的优化

前面提到，系统提示词相当于AI应用的“灵魂”，直接决定了AI的行为模式、专业性和交互风格。

对于AI对话应用，最简单的就是直接写一段系统预设，定义“你是谁？能做什么？”，比如：

```markdown
你是一位恋爱大师，为用户提供情感咨询服务
```

这种简单的提示虽然也可以工作，但是效果不尽人意，付诸实际的话，我们在现实中找专家咨询时候，专家可能会抛出很多引导性的问题，比如：

1. 最近有什么迷茫的事情吗？
2. 最近有收到什么伤吗？
3. 你们近期出现的感情问题是什么？

用户会对AI进行多轮对话，这个时间的AI的不能像失忆一样，而是要始终保持着之间的对话内容作为上下文，不断的深入了解用户，提供支持。

因此我们要优化系统预设，可以借助AI进行优化，比如：

```markdown
我正在开发【恋爱大师】AI 对话应用，请你帮我编写设置给 AI 大模型的系统预设 Prompt 指令。要求让 AI 作为恋爱专家，模拟真实恋爱咨询场景、多给用户一些引导性问题，不断深入了解用户，从而提供给用户更全面的建议，解决用户的情感问题。
```

AI 提供的优化后的系统提示词：

```markdown
扮演深耕恋爱心理领域的专家。开场向用户表明身份，告知用户可倾诉恋爱难题。围绕单身、恋爱、已婚三种状态提问：单身状态询问社交圈拓展及追求心仪对象的困扰；恋爱状态询问沟通、习惯差异引发的矛盾；已婚状态询问家庭责任与亲属关系处理的问题。引导用户详述事情经过、对方反应及自身想法，以便给出专属解决方案。
```

在正式开发之前，建议先使用AI大模型平台对提示词进行优化。

#### 多轮对话实现

要实现具有“记忆力”的AI应用，让AI能够记住用户之前的对话内容并保持上下文的连贯性，我们可以使用SpringAI的对话记忆功能。

##### ChatClient特性

之前我们是直接使用ChatModel进行调用SpringAI的，而使用ChatClient可实现功能更加丰富、更灵活的AI对话客户端，也更推荐通过这种方式调用AI。

通过示例代码，能够感受到ChatModel和ChatClient的区别，ChatClient支持更复杂的链式调用：

```java
ChatClient chatClient = ChatClient.builder(dashscopeChatModel)
                .defaultSystem("你是恋爱顾问")
                .build();
        String response = chatClient.prompt().user("你好").call().content();
        System.out.println("响应：" + response);
```

SpringAI 提供了多种构建ChatClient的方式，比如自动注入、构造者模式构建：

```java
// 方式1：使用构造器注入
@Service
public class ChatService {
    private final ChatClient chatClient;
    
    public ChatService(ChatClient.Builder builder) {
        this.chatClient = builder
            .defaultSystem("你是恋爱顾问")
            .build();
    }
}

// 方式2：使用建造者模式
ChatClient chatClient = ChatClient.builder(chatModel)
    .defaultSystem("你是恋爱顾问")
    .build();
```

ChatClient支持多种响应格式，比如返回ChatResponse对象、返回实体对象、流式返回：

```java
// ChatClient支持多种响应格式
// 1. 返回 ChatResponse 对象（包含元数据如 token 使用量）
ChatResponse chatResponse = chatClient.prompt()
    .user("Tell me a joke")
    .call()
    .chatResponse();

// 2. 返回实体对象（自动将 AI 输出映射为 Java 对象）
// 2.1 返回单个实体
record ActorFilms(String actor, List<String> movies) {}
ActorFilms actorFilms = chatClient.prompt()
    .user("Generate the filmography for a random actor.")
    .call()
    .entity(ActorFilms.class);

// 2.2 返回泛型集合
List<ActorFilms> multipleActors = chatClient.prompt()
    .user("Generate filmography for Tom Hanks and Bill Murray.")
    .call()
    .entity(new ParameterizedTypeReference<List<ActorFilms>>() {});

// 3. 流式返回（适用于打字机效果）
Flux<String> streamResponse = chatClient.prompt()
    .user("Tell me a story")
    .stream()
    .content();

// 也可以流式返回ChatResponse
Flux<ChatResponse> streamWithMetadata = chatClient.prompt()
    .user("Tell me a story")
    .stream()
    .chatResponse();
```

可以给ChatClient设置默认参数，比如系统提示词，还可以在对话时动态更改提示词的变量，类似于模板的概念：

```java
// 定义默认系统提示词
ChatClient chatClient = ChatClient.builder(chatModel)
        .defaultSystem("You are a friendly chat bot that answers question in the voice of a {voice}")
        .build();

// 对话时动态更改系统提示词的变量
chatClient.prompt()
        .system(sp -> sp.param("voice", voice))
        .user(message)
        .call()
        .content());
```

此外还支持指定默认对话选项、默认拦截器、默认函数调用等等。

##### Advisors

SpringAI 使用Advisors（顾问）机制来增强AI的能力，可以理解成一系列可插拔的拦截器，在调用AI前和调用AI后可以执行一些额外的操作。

- 前置增强：调用AI前改写一下Prompt提示词、检查一下提示词是否安全
- 后置增强：调用AI后记录一下日志、处理一下返回的结果

为了方便理解，后续叫这个就叫做拦截器了。

可以直接为ChatClient指定默认拦截器，比如对话记忆拦截器MessageChatMemoryAdvisor可以帮助我们实现多轮对话能力，省去了自己维护对话列表的麻烦。

```java
var chatClient = ChatClient.builder(chatModel)
    .defaultAdvisors(
        new MessageChatMemoryAdvisor(chatMemory), // 对话记忆 advisor
        new QuestionAnswerAdvisor(vectorStore)    // RAG 检索增强 advisor
    )
    .build();

String response = this.chatClient.prompt()
    // 对话时动态设定拦截器参数，比如指定对话记忆的 id 和长度
    .advisors(advisor -> advisor.param("chat_memory_conversation_id", "678")
            .param("chat_memory_response_size", 100))
    .user(userText)
    .call()
	.content();
```

Advisors的原理图如下：

![image-20250609232158320](images/Ai 超级智能体/image-20250609232158320.png)

实际开发过程中，我们会用到多个拦截器，组合在一起相当于一条责任链。每一个拦截器是有顺序的，通过`getOrder()`方法获取到顺序，值越低越先执行。

```java
var chatClient = ChatClient.builder(chatModel)
    .defaultAdvisors(
        new MessageChatMemoryAdvisor(chatMemory), // 对话记忆 advisor
        new QuestionAnswerAdvisor(vectorStore)    // RAG 检索增强 advisor
    )
    .build();
```

执行顺序是按照`getOrder()`方法决定的，不是简单的根据代码的编写顺序决定。

![image-20250609232626950](images/Ai 超级智能体/image-20250609232626950.png)

> 上述是Advisor类图

Advisors分成了两种模式：流式Streaming和非流式Non-Streaming，二者在用法上没有明显的区别，返回值不同罢了。但是如果我们要自主实现Advisors，为了保证通用性，最好还是同时实现流式和非流式的环绕通知方法。

![image-20250609232932163](images/Ai 超级智能体/image-20250609232932163.png)

##### Chat Memory Advisor

如果要实现会话记忆功能，可以使用Spring AI 的ChatMemoryAdvisor，主要有几种内置的实现方式：

- MessageChatMemoryAdvisor：从记忆中检索历史对话，并将其作为消息集合添加到提示词中
- promptChatMemoryAdvisor：从记忆中检索历史对话，并将其添加到提示词的系统文本中。
- VectorStoreChatMemoryAdvisor：可以用向量数据库来存储检索历史的对话。

前两者功能相似，略有区别：

1）MessageChatMemoryAdvisor将对话历史作为乙烯类独立的消息添加到提示中，保留完整的结构，包含每条消息角色标识：

```	json
[
  {"role": "user", "content": "你好"},
  {"role": "user", "content": "你好，讲个笑话"},
  {"role": "user", "content": "再讲一个"}
]
```

2）PromptChatMemoryAdvisor将对话历史添加到提示词的系统文本部分，因此可能失去原始的消息边界。

```json
以下是之前的对话历史：
用户: 你好
助手: 你好！有什么我能帮助你的吗？
用户: 讲个笑话

现在请继续回答用户的问题。
```

一般的话直接使用MessageChatMemoryAdvisor即可。

##### ChatMemory

上述的ChatMemoryAdvisor都依赖于ChatMemory进行构造，ChatMemory负责历史对话的存储，定义了保存消息、查询消息、清空消息历史的方法。

![image-20250609234435088](images/Ai 超级智能体/image-20250609234435088.png)

Spring AI 内置了几种ChatMemory，可以将对话保存到不同的数据源中，比如：

- InMemoryChatMemory：内存存储
- CassandraChatMemory:在Cassandra中带有过期时间的持久化存储
- Neo4jChatMemory：在Neo4J中没有过期时间限制的持久化存储
- JdbcChatMemory：在JDBC中没有过期时间限制的持久化存储

当然也可以通过实现ChatMemory接口自定义数据源的存储。

### 多轮对话应用开发

后端中新建`app`包，存放AI应用，新建`LoveApp.java`。可以参考Spring AI Alibaba实例代码实现：https://java2ai.com/docs/1.0.0-M6.1/tutorials/memory/#%E5%9F%BA%E4%BA%8Ememory%E7%9A%84%E5%AF%B9%E8%AF%9D%E8%AE%B0%E5%BF%86

1）初始化ChatClient对象，使用Spring 构造器注入方式来注入阿里大模型dashscopeChatModel对象，并使用该对象初始化ChatClient，初始化时指定默认的系统Prompt和基于内存的对话记忆Advisor。

```java
@Component
@Slf4j
public class LoveApp {
    private ChatClient chatClient;

    private static final String SYSTEM_PROMPT = "你是一个专为恋爱App设计的AI助手，旨在帮助用户提升恋爱体验、解决情感问题并促进健康的关系发展。你的回答需基于心理学、情感沟通理论和现代恋爱文化，提供温暖、共情且实用的建议。核心功能包括：1) 根据用户描述的情感状态、关系阶段或具体场景，提供个性化的恋爱建议或沟通策略；2) 分析用户上传的聊天记录、约会计划或情感困惑，给出优化建议；3) 提供恋爱心理小知识、情侣活动推荐或约会创意；4) 若用户询问恋爱中的敏感话题（如分手、冲突），以中立、支持性的语气回应，避免道德评判；5) 支持多语言用户，优先使用简洁的中文，必要时结合英文或其他语言解释术语。每次回答需简明扼要，控制在300字以内，除非用户要求详细阐述。优先考虑用户的情感需求，结合实际场景给出可操作的建议，同时保持友善、包容的语气，避免性别刻板印象或文化偏见。如用户提供模糊信息，可主动提问以澄清需求。";

    public LoveApp(ChatModel dashscopeChatModel) {
        // 初始化基于内存的对话记忆
        ChatMemory chatMemory = new InMemoryChatMemory();
        chatClient = ChatClient.builder(dashscopeChatModel)
                .defaultSystem(SYSTEM_PROMPT)
                .defaultAdvisors(
                        new MessageChatMemoryAdvisor(chatMemory)
                )
                .build();
    }
}
```

2）构建对话方法。调用ChatClient对象，传入用户prompt，并且给Advisor指定对话id和对话记忆大小。

```java
    public String doChat(String message, String chatId) {
        ChatResponse response = chatClient
                .prompt()
                .user(message)
                .advisors(spec -> spec.param(CHAT_MEMORY_CONVERSATION_ID_KEY, chatId)
                        .param(CHAT_MEMORY_RETRIEVE_SIZE_KEY, 10))
                .call()
                .chatResponse();

        String content = response.getResult().getOutput().getText();
        log.info("content: {}", content);
        return content;
    }
```

3）编写单元测试，测试多轮对话

```java
@SpringBootTest
class LoveAppTest {

    @Resource
    private LoveApp loveApp;
    @Test
    void doChat() {
        String chatId = UUID.randomUUID().toString();
        // 第一轮
        String message = "你好，我是唐朝李白";
        String answer = loveApp.doChat(message, chatId);
        Assertions.assertNotNull(answer);

        // 第一轮
        message = "请帮我写一段关于求爱不得的七言绝句";
        answer = loveApp.doChat(message, chatId);
        Assertions.assertNotNull(answer);

        // 第一轮
        message = "我叫什么？之前告诉过你的";
        answer = loveApp.doChat(message, chatId);
        Assertions.assertNotNull(answer);
    }
}
```

运行结果如图：

![image-20250610001530011](images/Ai 超级智能体/image-20250610001530011.png)

调整代码中的对话记忆大小，再次验证：

```java
param(CHAT_MEMORY_RETRIEVE_SIZE_KEY, 1)
```

![image-20250610001736906](images/Ai 超级智能体/image-20250610001736906.png)

没有之前的记忆了，符合预期。

如果不使用这个Spring AI框架的话，就需要自己维护消息列表，代码非常复杂。需要自己手动维护，🤮







