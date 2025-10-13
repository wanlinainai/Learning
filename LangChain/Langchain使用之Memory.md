# Langchain使用之Memory

## Memory概述

Memory是Langchain中用于多轮对话中保存和管理上下文信息的组件。实现上下文感知的能力。大语言模型本身没有记忆。

### 如果不使用Memory模块的话，如何实现上下文记忆能力？

> 通过messages变量，不断地将历史的对话信息追加到对话列表中即可实现。很早之前做毕业设计的时候用到的上下文能力就是存储在Redis中的。每一次用户的对话都是一个信息，将这个信息追加到JSON格式存储到Redis中。每一次向AI发起提问的时候都是携带了之前的数据的。
>
> 我们在Langchain中也是如此。

```python
import os
import dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

os.environ["OPENAI_BASE_URL"] = os.getenv("OPENAI_BASE_URL")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# 创建模型实例
llm = ChatOpenAI(model="gpt-4o-mini")

def chat_with_model(answer):
    # 提示词模版
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "你是一个人工智能助手"),
        ("human", "{question}")
    ])

    while True:
        chain = prompt_template | llm
        response = chain.invoke({"question": answer})

        print(f"模型回复：{response.content}")

        user_input = input("你还有什么问题吗？（输入'退出'时结束会话）")

        # 退出
        if user_input == "退出":
            break

        prompt_template.messages.append(AIMessage(content=response.content))
        prompt_template.messages.append(HumanMessage(content=user_input))

chat_with_model("你好，很不高兴认识你")
```



输出：

模型回复：你好！虽然你不高兴认识我，但我在这里帮助你。如果有什么事情想要聊或需要帮助，请告诉我！
<p style="color: red">问题：李白是谁?</p>
模型回复：李白（701年－762年），字太白，号青莲居士，唐代著名的诗人，誉称“诗仙”。他以豪放、奔放的个性和丰富的想象力闻名于世，作品多描绘自然景色、豪情壮志及对人生的感悟。李白的诗歌风格独特，擅长运用夸张和对比，常常表现出强烈的个性和深刻的情感。他的代表作包括《将进酒》、《庐山谣》和《月下独酌》等。李白的诗作对后世影响深远，是中国文学史上重要的人物之一。
<p style="color: red">问题：他有什么著作？</p>
模型回复：李白的著作主要为诗歌，他的作品汇编成集，最著名的是《李白集》。其中收录了他的绝大部分诗作。以下是一些李白的著名作品：


1. **《将进酒》**：这首诗表达了李白对人生的感慨，传达了豪放的饮酒情怀和对自由的追求。
2. **《庐山谣》**：描绘了庐山的壮丽景色，表现了诗人与自然的深厚感情。
3. **《月下独酌》**：这首诗反映了李白孤独的心情，借助明月抒发对生活的思考。
4. **《夜泊牛津》**：描写了夜晚泊船时的情景，展现了诗人对故乡的思念。
5. **《早发白帝城》**：描绘了清晨的壮丽景色，表达了李白心中对旅行的渴望。

李白的诗歌以其独特的风格、丰富的情感和深刻的思想，被后人广泛传颂，成为中国文学的重要组成部分。
<p style="color: red">问题：我之前问的人是谁？</p>
模型回复：你刚才提问的诗人是李白。他是中国唐代著名的诗人，以其豪放的个性和丰富的诗作著称。如果你有更多关于李白或其他诗人的问题，欢迎继续询问！

## 基础Memory模块的使用

设计Memory模块：

- 保留一个聊天消息列表
- 只返回最近交互的K条消息
- 返回过去K条消息的简介摘要
- 从存储的消息中提取实体，并且只返回有关当前运行中引用的实体的信息

### ChatMessageHistory（基础）

是其他记忆组件底层存储工具。

**存储和管理对话消息**的基础类，直接操作消息对象（HumanMessage、AIMessage）其他记忆组件的底层存储工具。

还有一个别名：`InMemoryChatMessageHistory`；导包时使用：`**langchain_core.chat_history.InMemoryChatMessageHistory**`

是一个存储器，与策略无关。

- 记忆存储

```python
from langchain.memory import ChatMessageHistory

# 实例化
history = ChatMessageHistory()

# 添加相关的消息存储
history.add_user_message("你好")
history.add_ai_message("很不高兴认识你")

# 打印存储的消息
print(history.messages)
```



输出：

```shell
[HumanMessage(content='你好', additional_kwargs={}, response_metadata={}), AIMessage(content='很不高兴认识你', additional_kwargs={}, response_metadata={})]
```

- 对接大模型

```python
from langchain.memory import ChatMessageHistory

history = ChatMessageHistory()

history.add_user_message("你好")
history.add_ai_message("很不高兴认识你")
history.add_user_message("帮我计算一下：1 + 1 * 8 = ？")

response = llm.invoke(history.messages)

print(response.content)
```

输出：

```shell
根据运算的优先级，乘法要先于加法。所以计算过程是：

1 + (1 * 8) = 1 + 8 = 9

所以，1 + 1 * 8 = 9。
```



### ConversationBufferMemory

- 返回存储的字符串信息

```python
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory()

# inputs对应的就是用户消息，outputs对应的就是AI消息
memory.save_context(inputs={"input": "你好"}, outputs={"output": "很不高兴认识你"})
memory.save_context(inputs={"input": "请帮我计算一下8 * 8 - 1 = ？"}, outputs={"output": "63"})

# 返回的字典结构的Key = history
print(memory.load_memory_variables({}))
```

输出：

```shell
{'history': 'Human: 你好\nAI: 很不高兴认识你\nHuman: 请帮我计算一下8 * 8 - 1 = ？\nAI: 63'}
```

- 以消息列表的形式返回存储消息

```python
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory()

# inputs对应的就是用户消息，outputs对应的就是AI消息
memory.save_context(inputs={"input": "你好"}, outputs={"output": "很不高兴认识你"})
memory.save_context(inputs={"input": "请帮我计算一下8 * 8 - 1 = ？"}, outputs={"output": "63"})

# 返回的字典结构的Key = history
print(memory.load_memory_variables({}))

print("\n")

# 原始消息列表
print(memory.chat_memory.messages)
```

输出：

```shell
{'history': 'Human: 你好\nAI: 很不高兴认识你\nHuman: 请帮我计算一下8 * 8 - 1 = ？\nAI: 63'}


[HumanMessage(content='你好', additional_kwargs={}, response_metadata={}), AIMessage(content='很不高兴认识你', additional_kwargs={}, response_metadata={}), HumanMessage(content='请帮我计算一下8 * 8 - 1 = ？', additional_kwargs={}, response_metadata={}), AIMessage(content='63', additional_kwargs={}, response_metadata={})]
```

- 提示词模版的使用（PromptTemplate）

```python
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain.chains.llm import LLMChain

llm = ChatOpenAI(model="gpt-4o-mini")
prompt = PromptTemplate.from_template(
    template="""
    你可以和人类对话
    当前对话历史：{history}
    人类问题：{question}
    回复：
    """
)

memory = ConversationBufferMemory()
# memory = ConversationBufferMemory(memory_key="chat_history") #显式设置history的名称，修改之后使用chat_history代替history

chain = LLMChain(llm=llm, prompt=prompt, memory=memory)

response = chain.invoke({"question": "你好，我叫小红"})

print(response)
```

输出：

```shell
{'question': '你好，我是谁？', 'history': 'Human: 你好，我叫小红\nAI: 你好，小红！很高兴和你聊天。你今天过得怎么样？', 'text': '你好，小红！你刚刚告诉我你叫小红。有什么我可以帮助你的吗？'}
```

> 如果要将Memory中的history自定义名称，在设置ConversationBufferMemory(memory_key="custom_history")即可。便可以在Template中设置自定义名称。

- 使用ChatPromptTemplate和return_messages

```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

llm = ChatOpenAI(model="gpt-4o-mini")

# 创建Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个与人类对话的机器人"),
    MessagesPlaceholder("history"),
    ("human", "问题：{question}")
])

# 创建Memory
memory = ConversationBufferMemory(return_messages=True)

# 创建LLMChain
llm_chain = LLMChain(prompt=prompt, llm=llm, memory=memory)

res1 = llm_chain.invoke({"question": "中国首都在哪里？"})

print(res1, end="\n\n")
```

输出

```shell
{'question': '中国首都在哪里？', 'history': [HumanMessage(content='中国首都在哪里？', additional_kwargs={}, response_metadata={}), AIMessage(content='中国的首都是北京。', additional_kwargs={}, response_metadata={})], 'text': '中国的首都是北京。'}
```



```python
res2 = llm_chain.invoke({"question": "我刚才问的什么问题？"})
print(res2)
```

输出

```shell
{'question': '我刚才问的什么问题？', 'history': [HumanMessage(content='中国首都在哪里？', additional_kwargs={}, response_metadata={}), AIMessage(content='中国的首都是北京。', additional_kwargs={}, response_metadata={}), HumanMessage(content='我刚才问的什么问题？', additional_kwargs={}, response_metadata={}), AIMessage(content='你刚才问的问题是“中国首都在哪里？”', additional_kwargs={}, response_metadata={})], 'text': '你刚才问的问题是“中国首都在哪里？”'}
```

> 可以发现，使用ChatPromptTemplate会将history 显式的第一次加载出来。使用Prompt不会。

**二者对比**

| 特性         | PromptTemplate | ChatPromptTemplate            |
| ------------ | -------------- | ----------------------------- |
| 历史存储时机 | 执行后存储     | 执行前用户输入 + 执行存储输入 |
| 首次调用显示 | 只显示问题     | 显示完整问题                  |
| 内部消息类型 | 拼接字符串     | List[BaseMessage]             |

> Langchain为了`保障对话一致性`做的刻意设计
>
> 1. 用户提问之后，系统应该立即记住该问题
> 2. AI回答之后，该响应立即加入对话上下文
> 3. 返回给客户端的结果反应最新状态





















