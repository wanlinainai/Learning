# Model I/O介绍

Model i/O模块是与大模型（LLMS）进行交互的`核心组件`。

所谓的Model I/O，包括输入提示（Format）、调用模型（Predict）、输出解析（Parse）。分别对应着`Prompt Template`、`Model`和`Output Parser`。

> 简而言之，就是输入、模型处理、输出

## Model I/O调用模型

### 模型的不同分类方式

> 简而言之，就是用谁家的API以什么方式调用哪一种类型的大模型

```
# 模型调用的分类
1. 模型功能的不同：

非对话模型（LLMs、Text Model）

对话模型（Chat Model）（推荐）

嵌入模型（Embedding Model）（RAG chapter）

2. 模型调用时，参数书写的位置不同（API Key、base URL、Model-Name）

硬编码（参数写在代码中，不用）

环境变量

配置文件（.env）（推荐）

3. 具体API的调用

使用Langchain 提供的API（推荐方式）

使用OpenAI 官方API 的方式

使用其他平台提供的 API（阿里云百炼等）
```



### 非对话模型的调用方式

![image-20250929004503147](images/Model IO介绍/image-20250929004503147.png)

- 适用场景：单词文本执行生成（摘要生成、翻译、代码生成、单次问答）
- 不支持多轮上下文。每次调用独立处理输入，无法自动关联历史对话（需手动拼接）
- 局限性：无法处理角色分工或复杂对话逻辑

### 对话模型

ChatModels，聊天模型、对话模型，底层还是LLMs。

特点：

- 输入：接收消息列表`List[BaseMessage]`或者`PromptValue`，每条消息需要指定角色（如SystemMessage、HumanMessage、AIMessage）
- 输出：通常是`BaseMessage`

- 原生支持多轮对话：通过消息列表维护上下文（例如：`[SystemMessage]`、`HumanMessage`、`AIMessage`）
- 适用场景：对话系统（客服机器人、长期交互的AI助手）

### 关于对话模型中消息（Message）的使用

1、 获取对话模型

2、 调用会话模型

3、 处理响应数据

```python
from langchain_openai import ChatOpenAI
import os
import dotenv

dotenv.load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_BASE_URL"] = os.getenv("OPENAI_BASE_URL")

chat_model = ChatOpenAI(
    # api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o-mini",
    # base_url=os.getenv("OPENAI_BASE_URL")
)

response = chat_model.invoke("你好")

print(response)
print(type(response))
```



> invoke方法：输入可以是多种类型：
>
> 1. 字符串类型
> 2. 消息列表类型
>
> invoke方法：输出类型：
>
> 1. BaseMessage的子类：AIMessage
>
> 通过输出来判断是对话模型还是非对话模型。

除了字符串作为输入外，还可以将`聊天消息`作为输入。返回聊天消息作为输出。

- `SystemMessage`：role为System的消息类型。作为消息的第一个传递。比如：“现在你是一个高级智能合约工程师”、“返回JSON格式数据”等等。
- `HumanMessage`：来自用户输入。
- `AIMessage`：存储AI回复的消息。
- `ChatMessage`：自定义角色的通用消息类型
- `FunctionMessage/ToolMessage`：函数调用/工具消息，用于函数调用结果的消息类型

```python
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

system_message = SystemMessage(content="你是一个英语教学专家")

human_message = HumanMessage(content="帮我制定一个学习英语雅思的计划")

messages = [system_message, human_message]

print(messages)
```

```shell
[SystemMessage(content='你是一个英语教学专家', additional_kwargs={}, response_metadata={}), HumanMessage(content='帮我制定一个学习英语雅思的计划', additional_kwargs={}, response_metadata={})]
```



```python
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

system_message = SystemMessage(
    content="你是一个AI开发工程师",
    additional_kwargs={"tools": "invoke_func1"}
)

human_message = HumanMessage(
    content="我需要开发一个关于区块链AI智能助手，关于分析某一个虚拟币的受欢迎程度，帮我用极简的语言简述一下",
)

ai_message = AIMessage(
    content="你好，请继续问下一个问题"
)

messages = [system_message, human_message, ai_message]

print(messages)
```

```python
from langchain_core.messages import (SystemMessage, HumanMessage, AIMessage, ChatMessage)

system_message = SystemMessage(
    content="你是一个AI开发工程师",
    additional_kwargs={"tools": "invoke_func1"}
)

human_message = HumanMessage(
    content="我需要开发一个关于区块链AI智能助手，关于分析某一个虚拟币的受欢迎程度，帮我用极简的语言简述一下",
)

chat_message = ChatMessage(
    role="analyst",
    content="补充一些关于模型调优的建议"
)


messages = [system_message, human_message]
# print(messages)
response = chat_model.invoke(messages)

print(response.content)

```



```shell
开发一个区块链AI智能助手，可以通过以下步骤分析某个虚拟币的受欢迎程度：

1. **数据收集**：获取该虚拟币的交易数据、社交媒体讨论、新闻报道等信息。
2. **情感分析**：使用自然语言处理技术分析社交媒体和新闻的情感倾向。
3. **市场指标**：监测交易量、价格波动、持币地址数量等市场数据。
4. **趋势分析**：结合历史数据，识别受欢迎程度的趋势变化。
5. **报告生成**：生成易于理解的报告，提供受欢迎程度的综合评估。

这样，用户可以迅速了解该虚拟币的市场状况。
```







## 如何选择合适的大模型？

https://lmarena.ai/leaderboard。

没有最好的大模型，只有最合适的大模型。上述的排行榜是相对而言更推荐的榜单。可供参考。

























