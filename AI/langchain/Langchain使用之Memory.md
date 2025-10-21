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

### ConversationChain（过期API，使用RunnableWithMessageHistory代替）

ConversationChain是对`ConversationBufferMemory`和`LLMChain`的封装。

```python
from langchain.chains.conversation.base import ConversationChain
from langchain.chains import LLMChain
from langchain_core.prompts.prompt import PromptTemplate

llm = ChatOpenAI(model="gpt-4o-mini")

template = """
以下是人类与AI之间的友好对话描述。AI表现得很健谈，并提供了大量来自其上下文的
具体细节。如果AI不知道问题的答案，它会真诚地表示不知道
当前对话：{history}
Human: {input}
AI: ....
"""

prompt = PromptTemplate.from_template(template)

chain = ConversationChain(llm=llm, prompt=prompt, verbose=True)

chain.invoke({"input": "你好，你的名字是小智"})
```

输出：

```shell
C:\Users\admin\AppData\Local\Temp\ipykernel_44456\3379283954.py:17: LangChainDeprecationWarning: The class `ConversationChain` was deprecated in LangChain 0.2.7 and will be removed in 1.0. Use :class:`~langchain_core.runnables.history.RunnableWithMessageHistory` instead.
  chain = ConversationChain(llm=llm, prompt=prompt, verbose=True)
C:\Users\admin\.conda\envs\pyth311\Lib\site-packages\pydantic\main.py:253: LangChainDeprecationWarning: Please see the migration guide at: https://python.langchain.com/docs/versions/migrating_memory/
  validated_self = self.__pydantic_validator__.validate_python(data, self_instance=self)


> Entering new ConversationChain chain...
Prompt after formatting:

以下是人类与AI之间的友好对话描述。AI表现得很健谈，并提供了大量来自其上下文的
具体细节。如果AI不知道问题的答案，它会真诚地表示不知道
当前对话：
Human: 你好，你的名字是小智
AI: ....


> Finished chain.
{'input': '你好，你的名字是小智',
 'history': '',
 'response': 'AI: 你好！我叫小智，很高兴见到你！有什么我可以帮助你的吗？'}
```

```python
chain.invoke({"input": "你叫什么？"})
```

输出：

```shell


> Entering new ConversationChain chain...
Prompt after formatting:

以下是人类与AI之间的友好对话描述。AI表现得很健谈，并提供了大量来自其上下文的
具体细节。如果AI不知道问题的答案，它会真诚地表示不知道
当前对话：Human: 你好，你的名字是小智
AI: AI: 你好！我叫小智，很高兴见到你！有什么我可以帮助你的吗？
Human: 你叫什么？
AI: AI: 我叫小智！这是我为自己取的名字。你有什么想聊的吗？
Human: 你叫什么？
AI: ....


> Finished chain.
{'input': '你叫什么？',
 'history': 'Human: 你好，你的名字是小智\nAI: AI: 你好！我叫小智，很高兴见到你！有什么我可以帮助你的吗？\nHuman: 你叫什么？\nAI: AI: 我叫小智！这是我为自己取的名字。你有什么想聊的吗？',
 'response': 'AI: 我叫小智！很高兴和你聊天。之前我提到过我的名字，你还有其他想问的问题吗？'}
```

省略了LLMChain和Memory。也可以得到相同的结果。

**使用内置默认的提示词模版**

```python
llm = ChatOpenAI(model="gpt-4o-mini")

conv_chain = ConversationChain(llm=llm)

result_1 = conv_chain.invoke(input="校长有2只猫咪")

result_2 = conv_chain.invoke(input="小白有3只猫咪")

result_3 = conv_chain.invoke(input="两个人加起来有多少只猫?")

print(result_3)
```

输出：

```shell
{'input': '两个人加起来有多少只猫?', 'history': 'Human: 校长有2只猫咪\nAI: 哦，真的呀！校长的猫咪是什么品种的呢？它们是长毛猫还是短毛猫？猫咪的名字是什么？我很好奇校长是如何照顾这些猫咪的，是自己养还是有专人打理？猫咪是怎么跟校长互动的呀？它们喜欢玩什么玩具？\nHuman: 小白有3只猫咪\nAI: 哇，小白也有3只猫咪啊！她的猫咪都是哪些品种呢？是同样的品种还是有不同的呢？它们的性格如何？小白有没有给它们起名字？我很好奇她是怎么照顾这3只猫咪的，是自己喂食还是请了帮手？这3只猫咪之间关系如何呢？它们喜欢一起玩还是有些更独立？', 'response': '校长有2只猫咪，小白有3只猫咪，所以两个人加起来一共有5只猫咪！如果你想知道更多关于猫咪的信息或者它们的趣事，随时可以问我哦！'}
```

### ConversationBufferWindowMemory

ConversationBufferMemory可以无限的将历史消息对话填充到History中，但是这会导致很多问题：

1. 内存十分大
2. Token消耗大

由此推出了Top K的Memory。

- 适合长文本对话
- 支持return_messages参数控制
  - return_messages = True。消息列表
  - return_messages = False。纯字符串

```python
from langchain.memory import ConversationBufferWindowMemory

memory = ConversationBufferWindowMemory(k=2, return_messages=True)

memory.save_context({"input": "你好"}, {"output": "你好啊"})
memory.save_context({"input": "你是谁？"}, {"output": "我是小智"})
memory.save_context({"input": "请问 1 + 1 = ？"}, {"output": "等于3"})

print(memory.load_memory_variables({}))
```

结果：

```shell
{'history': [HumanMessage(content='你是谁？', additional_kwargs={}, response_metadata={}), AIMessage(content='我是小智', additional_kwargs={}, response_metadata={}), HumanMessage(content='请问 1 + 1 = ？', additional_kwargs={}, response_metadata={}), AIMessage(content='等于3', additional_kwargs={}, response_metadata={})]}
```

```python
from langchain.chains import LLMChain
from langchain_core.prompts.prompt import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

llm = ChatOpenAI(model="gpt-4o-mini")

template = """
以下是人类与AI之间的友好对话描述。AI表现得很健谈，并提供了大量来自其上下文的
具体细节。如果AI不知道问题的答案，它会真诚地表示不知道
当前对话：{history}
Human: {question}
AI: ....
"""
# Prompt模版
prompt_template = PromptTemplate.from_template(template)
memory = ConversationBufferWindowMemory(k=3, return_messages=False)

conversation_with_summary = LLMChain(
    llm=llm,
    prompt=prompt_template,
    memory=memory,
    verbose=True
)

res1 = conversation_with_summary.invoke({"question": "你好，我是孙悟空"})
print(res1)

res2 = conversation_with_summary.invoke({"question": "我有两个师弟：猪无能和沙悟净"})
print(res2)

res3 = conversation_with_summary.invoke({"question": "我今年参加了高考，成功考上了TOP 985院校"})
print(res3)

res4 = conversation_with_summary.invoke({"question": "我是谁？"})
print(res4)
```

结果：

```shell


> Entering new LLMChain chain...
Prompt after formatting:

以下是人类与AI之间的友好对话描述。AI表现得很健谈，并提供了大量来自其上下文的
具体细节。如果AI不知道问题的答案，它会真诚地表示不知道
当前对话：
Human: 你好，我是孙悟空
AI: ....


> Finished chain.
{'question': '你好，我是孙悟空', 'history': '', 'text': 'AI: 你好，孙悟空！很高兴见到你。你是《西游记》中的英雄，拥有强大的法术和72变的能力。你还有那根如意金箍棒，可以随意变大变小。最近在西天取经的旅途中有什么新的冒险吗？'}


> Entering new LLMChain chain...
Prompt after formatting:

以下是人类与AI之间的友好对话描述。AI表现得很健谈，并提供了大量来自其上下文的
具体细节。如果AI不知道问题的答案，它会真诚地表示不知道
当前对话：Human: 你好，我是孙悟空
AI: AI: 你好，孙悟空！很高兴见到你。你是《西游记》中的英雄，拥有强大的法术和72变的能力。你还有那根如意金箍棒，可以随意变大变小。最近在西天取经的旅途中有什么新的冒险吗？
Human: 我有两个师弟：猪无能和沙悟净
AI: ....


> Finished chain.
{'question': '我有两个师弟：猪无能和沙悟净', 'history': 'Human: 你好，我是孙悟空\nAI: AI: 你好，孙悟空！很高兴见到你。你是《西游记》中的英雄，拥有强大的法术和72变的能力。你还有那根如意金箍棒，可以随意变大变小。最近在西天取经的旅途中有什么新的冒险吗？', 'text': 'AI: 是的，你的两个师弟都是《西游记》中的重要角色！猪无能，也就是猪八戒，性格憨厚可爱，爱吃懒做，但在关键时刻也能展现出勇气和智慧。他那把八尺钉耙可是个厉害的武器呢。至于沙悟净，他是一个忠诚踏实的人，虽然默默无闻，但在团队中起着非常重要的作用。你们三人一路上经历了很多挑战和考验，最近有遇到什么有趣或危险的事情吗？'}


> Entering new LLMChain chain...
Prompt after formatting:

以下是人类与AI之间的友好对话描述。AI表现得很健谈，并提供了大量来自其上下文的
具体细节。如果AI不知道问题的答案，它会真诚地表示不知道
当前对话：Human: 你好，我是孙悟空
AI: AI: 你好，孙悟空！很高兴见到你。你是《西游记》中的英雄，拥有强大的法术和72变的能力。你还有那根如意金箍棒，可以随意变大变小。最近在西天取经的旅途中有什么新的冒险吗？
Human: 我有两个师弟：猪无能和沙悟净
AI: AI: 是的，你的两个师弟都是《西游记》中的重要角色！猪无能，也就是猪八戒，性格憨厚可爱，爱吃懒做，但在关键时刻也能展现出勇气和智慧。他那把八尺钉耙可是个厉害的武器呢。至于沙悟净，他是一个忠诚踏实的人，虽然默默无闻，但在团队中起着非常重要的作用。你们三人一路上经历了很多挑战和考验，最近有遇到什么有趣或危险的事情吗？
Human: 我今年参加了高考，成功考上了TOP 985院校
AI: ....


> Finished chain.
{'question': '我今年参加了高考，成功考上了TOP 985院校', 'history': 'Human: 你好，我是孙悟空\nAI: AI: 你好，孙悟空！很高兴见到你。你是《西游记》中的英雄，拥有强大的法术和72变的能力。你还有那根如意金箍棒，可以随意变大变小。最近在西天取经的旅途中有什么新的冒险吗？\nHuman: 我有两个师弟：猪无能和沙悟净\nAI: AI: 是的，你的两个师弟都是《西游记》中的重要角色！猪无能，也就是猪八戒，性格憨厚可爱，爱吃懒做，但在关键时刻也能展现出勇气和智慧。他那把八尺钉耙可是个厉害的武器呢。至于沙悟净，他是一个忠诚踏实的人，虽然默默无闻，但在团队中起着非常重要的作用。你们三人一路上经历了很多挑战和考验，最近有遇到什么有趣或危险的事情吗？', 'text': 'AI: 哇，真是太棒了，孙悟空！高考是一项重要的挑战，能够考上985院校意味着你在学业上付出了很多努力和汗水。你可能会在校园里遇到许多新的朋友和有趣的课程。你打算学习什么专业呢？或者在大学生活中你有什么特别期待的事情吗？'}


> Entering new LLMChain chain...
Prompt after formatting:

以下是人类与AI之间的友好对话描述。AI表现得很健谈，并提供了大量来自其上下文的
具体细节。如果AI不知道问题的答案，它会真诚地表示不知道
当前对话：Human: 你好，我是孙悟空
AI: AI: 你好，孙悟空！很高兴见到你。你是《西游记》中的英雄，拥有强大的法术和72变的能力。你还有那根如意金箍棒，可以随意变大变小。最近在西天取经的旅途中有什么新的冒险吗？
Human: 我有两个师弟：猪无能和沙悟净
AI: AI: 是的，你的两个师弟都是《西游记》中的重要角色！猪无能，也就是猪八戒，性格憨厚可爱，爱吃懒做，但在关键时刻也能展现出勇气和智慧。他那把八尺钉耙可是个厉害的武器呢。至于沙悟净，他是一个忠诚踏实的人，虽然默默无闻，但在团队中起着非常重要的作用。你们三人一路上经历了很多挑战和考验，最近有遇到什么有趣或危险的事情吗？
Human: 我今年参加了高考，成功考上了TOP 985院校
AI: AI: 哇，真是太棒了，孙悟空！高考是一项重要的挑战，能够考上985院校意味着你在学业上付出了很多努力和汗水。你可能会在校园里遇到许多新的朋友和有趣的课程。你打算学习什么专业呢？或者在大学生活中你有什么特别期待的事情吗？
Human: 我是谁？
AI: ....


> Finished chain.
{'question': '我是谁？', 'history': 'Human: 你好，我是孙悟空\nAI: AI: 你好，孙悟空！很高兴见到你。你是《西游记》中的英雄，拥有强大的法术和72变的能力。你还有那根如意金箍棒，可以随意变大变小。最近在西天取经的旅途中有什么新的冒险吗？\nHuman: 我有两个师弟：猪无能和沙悟净\nAI: AI: 是的，你的两个师弟都是《西游记》中的重要角色！猪无能，也就是猪八戒，性格憨厚可爱，爱吃懒做，但在关键时刻也能展现出勇气和智慧。他那把八尺钉耙可是个厉害的武器呢。至于沙悟净，他是一个忠诚踏实的人，虽然默默无闻，但在团队中起着非常重要的作用。你们三人一路上经历了很多挑战和考验，最近有遇到什么有趣或危险的事情吗？\nHuman: 我今年参加了高考，成功考上了TOP 985院校\nAI: AI: 哇，真是太棒了，孙悟空！高考是一项重要的挑战，能够考上985院校意味着你在学业上付出了很多努力和汗水。你可能会在校园里遇到许多新的朋友和有趣的课程。你打算学习什么专业呢？或者在大学生活中你有什么特别期待的事情吗？', 'text': 'AI: 你是孙悟空，一个充满传奇色彩的角色，来自中国古典小说《西游记》，你有着强大的法术和变幻能力，是一个勇敢且智慧的英雄。不过，除了那位著名的角色，你可能还有其他身份，比如学生、朋友等。你想让我知道更多关于你的事情吗？'}
```

### ConversationTokenBufferMemory

基于Token数量控制的对话记忆机制，超过的话就会将最早的消息删除，保留与最近交流相对应的字符数量

- Token的精准控制
- 原始对话保留

```python
from langchain.memory import ConversationTokenBufferMemory
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")

memory = ConversationTokenBufferMemory(
    llm=llm,
    max_token_limit=5 # 设置最大的Token限制
)

memory.save_context({"input": "你好"}, {"output": "你好啊"})
memory.save_context({"input": "北京的天气怎么样？"}, {"output": "天气晴朗"})

# 查看当前记忆
print(memory.load_memory_variables({}))
```

结果：

```shell
{'history': ''}
```

调整max_token_limit大小为50.

```python
from langchain.memory import ConversationTokenBufferMemory
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")

memory = ConversationTokenBufferMemory(
    llm=llm,
    max_token_limit=50 # 设置最大的Token限制
)

memory.save_context({"input": "你好"}, {"output": "你好啊"})
memory.save_context({"input": "北京的天气怎么样？"}, {"output": "天气晴朗"})

# 查看当前记忆
print(memory.load_memory_variables({}))
```

结果：

```shell
{'history': 'Human: 你好\nAI: 你好啊\nHuman: 北京的天气怎么样？\nAI: 天气晴朗'}
```

### ConversationSummaryMemory

智能压缩对话历史的记忆机制，通过LLM自动将对话内容精简摘要。不存储原始文本。

- 摘要生成
- 动态更新
- 上下文优化

```python
from langchain.memory import ConversationSummaryMemory

llm = ChatOpenAI(model="gpt-4o-mini")

# 实例化
memory = ConversationSummaryMemory(
    llm=llm
)

memory.save_context({"input": "你好"}, {"output": "你好啊"})
memory.save_context({"input": "北极有什么？"}, {"output": "北极有火烈鸟"})
memory.save_context({"input": "我上一个问题是什么？"}, {"output": "你好，北极有什么？"})

print(memory.load_memory_variables({}))
```

结果：

```shell
{'history': 'The human greets the AI in Chinese, asking "Hello?" The AI responds with a greeting in return. The human then asks what is found in the Arctic, and the AI responds that there are flamingos in the Arctic. The human later inquires about their previous question, to which the AI reiterates that the human\'s last question was about what is found in the Arctic.'}
```

如果实例化Memory之前已经存在历史消息，可以使用：from_messages()方法

```python
from langchain.memory import ChatMessageHistory

llm = ChatOpenAI(model="gpt-4o-mini")

# 模拟历史消息记录
history = ChatMessageHistory()
history.add_user_message("你好，你是哪个？")
history.add_ai_message("你好，我是小智")

memory = ConversationSummaryMemory.from_messages(
    llm=llm,
    chat_memory=history
)

print(memory.load_memory_variables({}))

memory.save_context(inputs={"human": "我的名字是小白"},outputs={"AI": "很不高兴认识你，小黑"})

print(memory.load_memory_variables({}))

print(memory.chat_memory.messages)
```

结果：

```shell
{'history': 'The human greets the AI and asks who it is. The AI responds that it is named Xiao Zhi.'}
{'history': 'The human greets the AI and asks who it is. The AI responds that it is named Xiao Zhi. The human shares their name as Xiao Bai, and the AI expresses that it is not pleased to meet Xiao Hei.'}
[HumanMessage(content='你好，你是哪个？', additional_kwargs={}, response_metadata={}), AIMessage(content='你好，我是小智', additional_kwargs={}, response_metadata={}), HumanMessage(content='我的名字是小白', additional_kwargs={}, response_metadata={}), AIMessage(content='很不高兴认识你，小黑', additional_kwargs={}, response_metadata={})]
```

### ConversationSummaryBufferMemory

是一种混合记忆机制。结合了`ConversationBufferMemory`和`ConversationSummaryMemory`的优点，保留最近的对话内容的同时，能够对较早的对话进行概括。

- 保留最近N条的原始对话信息，确保最近交互的完整上下文
- 摘要较早的信息，超出缓冲区的进行概括压缩
- 平衡细节和效率：既不会丢失关键细节，又可以处理长对话

```python
from langchain.memory import ConversationSummaryBufferMemory
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")

memory = ConversationSummaryBufferMemory(
    llm=llm,
    max_token_limit=30,
    return_messages=True
)

memory.save_context({"input": '你好。我的名字是小陈谷'}, {"output": "很不高兴认识你，小程"})
memory.save_context({"input": "李白是哪个朝代的诗人"}, {"output": "李白是唐朝诗人"})
memory.save_context({"input": "唐宋八大家里有苏轼吗？"}, {"output": "有的兄弟"})

print(memory.load_memory_variables({}))

print(memory.chat_memory.messages)
```

结果：

```shell
{'history': [SystemMessage(content='The human introduces themselves as 小陈谷. The AI expresses that it is not pleased to meet 小陈谷. The human asks about the poet 李白, and the AI responds that 李白 is a poet from the Tang Dynasty.', additional_kwargs={}, response_metadata={}), HumanMessage(content='唐宋八大家里有苏轼吗？', additional_kwargs={}, response_metadata={}), AIMessage(content='有的兄弟', additional_kwargs={}, response_metadata={})]}
[HumanMessage(content='唐宋八大家里有苏轼吗？', additional_kwargs={}, response_metadata={}), AIMessage(content='有的兄弟', additional_kwargs={}, response_metadata={})]
```

```python
from langchain.memory import ConversationSummaryBufferMemory
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")

memory = ConversationSummaryBufferMemory(
    llm=llm,
    max_token_limit=90,
    return_messages=True
)

memory.save_context({"input": '你好。我的名字是小陈谷'}, {"output": "很不高兴认识你，小程"})
memory.save_context({"input": "李白是哪个朝代的诗人"}, {"output": "李白是唐朝诗人"})
memory.save_context({"input": "唐宋八大家里有苏轼吗？"}, {"output": "有的兄弟"})

print(memory.load_memory_variables({}))

print(memory.chat_memory.messages)
```

结果：

```shell
{'history': [HumanMessage(content='你好。我的名字是小陈谷', additional_kwargs={}, response_metadata={}), AIMessage(content='很不高兴认识你，小程', additional_kwargs={}, response_metadata={}), HumanMessage(content='李白是哪个朝代的诗人', additional_kwargs={}, response_metadata={}), AIMessage(content='李白是唐朝诗人', additional_kwargs={}, response_metadata={}), HumanMessage(content='唐宋八大家里有苏轼吗？', additional_kwargs={}, response_metadata={}), AIMessage(content='有的兄弟', additional_kwargs={}, response_metadata={})]}
[HumanMessage(content='你好。我的名字是小陈谷', additional_kwargs={}, response_metadata={}), AIMessage(content='很不高兴认识你，小程', additional_kwargs={}, response_metadata={}), HumanMessage(content='李白是哪个朝代的诗人', additional_kwargs={}, response_metadata={}), AIMessage(content='李白是唐朝诗人', additional_kwargs={}, response_metadata={}), HumanMessage(content='唐宋八大家里有苏轼吗？', additional_kwargs={}, response_metadata={}), AIMessage(content='有的兄弟', additional_kwargs={}, response_metadata={})]
```

**模拟客服对话**

```python
from langchain.memory import ConversationSummaryBufferMemory
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains.llm import LLMChain

llm = ChatOpenAI(
    model="gpt-4o-mini",
    max_tokens=500
)

# 模版
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是电商客服助手，用中文友好回复用户问题。保持专业但亲切的语气。"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])
# 记忆
memory = ConversationSummaryBufferMemory(
    llm=llm,
    max_token_limit=400,
    memory_key="chat_history",
    return_messages=True
)
# 对话链
chain = LLMChain(
    llm=llm,
    prompt=prompt,
    memory=memory,
)
# 多轮对话内容
dialogue = [
    "你好，我想查询订单12345的状态",
    "这个订单是上周五下的",
    "我现在急着用，能加急处理吗",
    "等等，我可能记错订单号了，应该是12346",
    "对了，你们退货政策是怎样的"
]
# 执行对话
for user_input in range(len(dialogue)):
    response = chain.invoke({"input": dialogue[user_input]})
    print(f"用户：{dialogue[user_input]}")
    print(f"回答：{response['text']}\n")
# 查看记忆状态
print("\n=======当前记忆状态========")
print(memory.load_memory_variables({}))
```

结果：

```shell
用户：你好，我想查询订单12345的状态
回答：您好！感谢您联系我。关于订单12345的状态，我需要您提供一下相关信息，例如下单的邮箱或者手机号，以便我为您查询。谢谢！

用户：这个订单是上周五下的
回答：感谢您提供的信息！请稍等片刻，我来帮您查询一下订单12345的状态。查询完毕，我会尽快回复您。谢谢您的耐心等待！

用户：我现在急着用，能加急处理吗
回答：我理解您的紧急需求，非常抱歉给您带来不便。不过，订单处理的具体方式通常由我们的物流系统决定，我建议您可以拨打客服热线以寻求更快速的加急处理方案。请让我知道是否需要我提供客服热线的联系方式，或是其他我可以帮助您的地方。谢谢您的理解！

用户：等等，我可能记错订单号了，应该是12346
回答：没问题！感谢您更正订单号。请稍等片刻，我会尽快查询订单12346的状态。稍后将尽快回复您！谢谢您的耐心。

用户：对了，你们退货政策是怎样的
回答：我们的退货政策如下：

1. **退货期限**：通常在收到商品后7天内可以申请退货。
2. **商品状态**：退货商品必须保持未使用状态，且保留原包装和配件。
3. **申请方式**：您可以通过我们的官方网站或客服热线申请退货。提交申请后，我们会进行审核。
4. **运费**：如果是因商品质量问题导致的退货，我们将承担运费；若是因为个人原因，返回运费通常由您承担。

如有其他具体问题，欢迎随时询问！希望能帮到您！


=======当前记忆状态========
{'chat_history': [SystemMessage(content='The human asks about the status of order 12345.', additional_kwargs={}, response_metadata={}), AIMessage(content='您好！感谢您联系我。关于订单12345的状态，我需要您提供一下相关信息，例如下单的邮箱或者手机号，以便我为您查询。谢谢！', additional_kwargs={}, response_metadata={}), HumanMessage(content='这个订单是上周五下的', additional_kwargs={}, response_metadata={}), AIMessage(content='感谢您提供的信息！请稍等片刻，我来帮您查询一下订单12345的状态。查询完毕，我会尽快回复您。谢谢您的耐心等待！', additional_kwargs={}, response_metadata={}), HumanMessage(content='我现在急着用，能加急处理吗', additional_kwargs={}, response_metadata={}), AIMessage(content='我理解您的紧急需求，非常抱歉给您带来不便。不过，订单处理的具体方式通常由我们的物流系统决定，我建议您可以拨打客服热线以寻求更快速的加急处理方案。请让我知道是否需要我提供客服热线的联系方式，或是其他我可以帮助您的地方。谢谢您的理解！', additional_kwargs={}, response_metadata={}), HumanMessage(content='等等，我可能记错订单号了，应该是12346', additional_kwargs={}, response_metadata={}), AIMessage(content='没问题！感谢您更正订单号。请稍等片刻，我会尽快查询订单12346的状态。稍后将尽快回复您！谢谢您的耐心。', additional_kwargs={}, response_metadata={}), HumanMessage(content='对了，你们退货政策是怎样的', additional_kwargs={}, response_metadata={}), AIMessage(content='我们的退货政策如下：\n\n1. **退货期限**：通常在收到商品后7天内可以申请退货。\n2. **商品状态**：退货商品必须保持未使用状态，且保留原包装和配件。\n3. **申请方式**：您可以通过我们的官方网站或客服热线申请退货。提交申请后，我们会进行审核。\n4. **运费**：如果是因商品质量问题导致的退货，我们将承担运费；若是因为个人原因，返回运费通常由您承担。\n\n如有其他具体问题，欢迎随时询问！希望能帮到您！', additional_kwargs={}, response_metadata={})]}
```

如果将缓冲区Token限制缩小，最终的结果会是概括总结的内容。



















