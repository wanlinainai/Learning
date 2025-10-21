# Tools

## Tool的元素

本质上是封装了特定功能的可调用模块，是Agent、Chain或LLM可以来与世界交流的接口。

**通常包含以下元素**

- **name**：工具名称
- **Description**：工具的功能描述
- 工具调用的JSON模式
- 调用的函数
- **return_direct**：是否将工具结果返回给用户

**使用步骤**

1. 将`name`、`description`、`JSON`作为上下文传给LLM
2. LLM接收到参数之后，根据Prompt推测出需要调用的工具，并且提供具体的调用参数信息
3. 用户需要根据返回的工具对对应的工具方法进行回调

> 如果Tools存在**精准选择**的模式，最终的效果会更好。

## 自定义工具

1. 使用@Tool装饰器（最简单）

默认使用函数名作为工具名称，可以通过`name_or_callable`进行覆盖。

使用函数的`文档字符串`来作为工具描述，函数必须提供文档字符串。

1. 使用StructuredTool.from_function类方法

允许更多的同步、异步规范。

### @tools

```python
from langchain.tools import tool


@tool
def add_number(a: int, b: int) -> int:
    """两个整数相加"""
    return a + b

print(f"name = {add_number.name}")
print(f"args = {add_number.args}")
print(f"description = {add_number.description}")
print(f"return_direct = {add_number.return_direct}")

res = add_number.invoke({"a": 10, "b": 20})
print(res)
```

结果：

```shell
name = add_number
args = {'a': {'title': 'A', 'type': 'integer'}, 'b': {'title': 'B', 'type': 'integer'}}
description = 两个整数相加
return_direct = False
30
```

修改其中参数：

```python
from langchain.tools import tool

@tool(name_or_callable="add_two_number", description="add two numbers to a result", return_direct=True)
def add_number(a: int, b: int) -> int:
    """整数之和"""
    return a + b

print(f"name = {add_number.name}")
print(f"args = {add_number.args}")
print(f"description = {add_number.description}")
print(f"return_direct = {add_number.return_direct}")

res = add_number.invoke({"a": 10, "b": 20})
print(res)
```

结果：

```shell
name = add_two_number   # 变化
args = {'a': {'title': 'A', 'type': 'integer'}, 'b': {'title': 'B', 'type': 'integer'}}
description = add two numbers to a result # 变化
return_direct = True # 变化（默认是False，就是返回自动给Agent进行处理，设置为True就是直接返回给用户）
30
```

修改args:

```python
from langchain.tools import tool
from pydantic import BaseModel, Field

class FieldInfo(BaseModel):
    a: int = Field(description="第一个参数")
    b: int = Field(description="第二个参数")

@tool(name_or_callable="add_two_number", description="add two numbers to a result", args_schema=FieldInfo, return_direct=True)
def add_number(a: int, b: int) -> int:
    """整数相加"""
    return a + b

print(f"name = {add_number.name}")
print(f"args = {add_number.args}")
print(f"description = {add_number.description}")
print(f"return_direct = {add_number.return_direct}")

res = add_number.invoke({"a": 10, "b": 20})
print(res)
```

结果：

```shell
name = add_two_number
args = {'a': {'description': '第一个参数', 'title': 'A', 'type': 'integer'}, 'b': {'description': '第二个参数', 'title': 'B', 'type': 'integer'}}
description = add two numbers to a result
return_direct = True
30
```

### StructuredTool的from_function()

提供了更多的可适配性

```python
from langchain_core.tools import StructuredTool

def search_function(query: str):
    return "Langchain"

search1 = StructuredTool.from_function(
    func=search_function,
    name="Search",
    description="useful for when you need to answer questions about current events"
)

print(f"name = {search1.name}")
print(f"description = {search1.description}")
print(f"args = {search1.args}")

search1.invoke("hello")
```

结果：

```shell
name = Search
description = useful for when you need to answer questions about current events
args = {'query': {'title': 'Query', 'type': 'string'}}
'Langchain'
```

```python
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

class FieldInfo(BaseModel):
    query: str = Field(description="检索的关键词")

def search_function(query: str):
    return "Langchain"

search1 = StructuredTool.from_function(
    func=search_function,
    name="Search",
    args_schema=FieldInfo,
    description="useful for when you need to answer questions about current events",
    return_direct=True
)

print(f"name = {search1.name}")
print(f"description = {search1.description}")
print(f"args = {search1.args}")
print(f"return_direct = {search1.return_direct}")

search1.invoke("hello")
```

结果：

```shell
name = Search
description = useful for when you need to answer questions about current events
args = {'query': {'description': '检索的关键词', 'title': 'Query', 'type': 'string'}}
return_direct = True
'Langchain'
```

## 通过大模型调用工具

```python
from langchain_community.tools import MoveFileTool
from langchain_core.messages import HumanMessage
from langchain_core.utils.function_calling import convert_to_openai_function
import os
import dotenv
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")
os.environ['OPENAI_BASE_URL'] = os.getenv("OPENAI_BASE_URL")

# 定义LLM模型
chat_model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 定义工具
tools = [MoveFileTool()]
# 工具转成openai函数，后续可将函数进行模型调用
functions = [convert_to_openai_function(t) for t in tools]
# 提供消息
messages = [HumanMessage(content="我是Windows11系统，我的文件目录是E:\\a.txt,将文件a移动到C:\\Users\\admin\\Desktop\\a.txt")]
# 模型使用函数
response = chat_model.invoke(
    input=messages,
    functions=functions,
)
print(response)
```

结果：

```shell
content='' additional_kwargs={'function_call': {'arguments': '{"source_path":"E:\\\\a.txt","destination_path":"C:\\\\Users\\\\admin\\\\Desktop\\\\a.txt"}', 'name': 'move_file'}, 'refusal': None} response_metadata={'token_usage': {'completion_tokens': 33, 'prompt_tokens': 97, 'total_tokens': 130, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4o-mini-2024-07-18', 'system_fingerprint': 'fp_efad92c60b', 'id': 'chatcmpl-CQlms2C5rzenwOI02UVn9iste4WII', 'service_tier': None, 'finish_reason': 'function_call', 'logprobs': None} id='run--74b3f62d-e77e-4d6a-8396-9bf5809c8c92-0' usage_metadata={'input_tokens': 97, 'output_tokens': 33, 'total_tokens': 130, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}
```

但是如果我们将模型调用中的Message设置成其他问题，比如：北京今天的天气怎么样？模型会拒绝回答。

```python
response = chat_model.invoke(
    input=[HumanMessage(content="今天北京的天气怎么样？")],
    functions=functions
)
```

结果：

```shell
content='抱歉，我无法提供实时天气信息。建议您查看天气预报网站或使用天气应用程序获取最新的天气情况。' additional_kwargs={'refusal': None} response_metadata={'token_usage': {'completion_tokens': 29, 'prompt_tokens': 75, 'total_tokens': 104, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4o-mini-2024-07-18', 'system_fingerprint': 'fp_efad92c60b', 'id': 'chatcmpl-CQlwD1XO2nrcRPPscQEfcQS4n0NfB', 'service_tier': None, 'finish_reason': 'stop', 'logprobs': None} id='run--253802a1-0ddc-4030-b5f7-b1f160af41bd-0' usage_metadata={'input_tokens': 75, 'output_tokens': 29, 'total_tokens': 104, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}
```

> 说明：
>
> **大模型决定调用工具**
>
> 如果大模型需要调用工具：`MoveFileTool`，返回的messages会包含：
>
> - `content`：模型选择调用工具，可能是空，也可能有值
> - `addtional_kwargs`：工具调用的详细信息
>
> ```shell
> {
>     'function_call': {
>         'arguments': '{"source_path":"E:\\\\a.txt","destination_path":"C:\\\\Users\\\\admin\\\\Desktop\\\\a.txt"}',
>         'name': 'move_file'
>     },
>     'refusal': None
> }
> ```
>
> 如果输入与工具无关，大模型不会调用工具。

OK，之后我们执行工具。

提前检查，是否需要调用工具：

```python
import json

if "function_call" in response.additional_kwargs:
    tool_name = response.additional_kwargs["function_call"]["name"]
    tool_args = json.loads((response.additional_kwargs["function_call"]["arguments"]))
    print(f"调用工具:{tool_name}，参数:{tool_args}")

else :
    print("模型回复：", response.content)
```

实际执行的工具：

```python
if "move_file" in response.additional_kwargs["function_call"]["name"]:
    tool = MoveFileTool()
    result = tool.run(tool_args) # 执行工具
    print(result)
```

结果：

```shell
调用工具:move_file，参数:{'source_path': 'E:\\a.txt', 'destination_path': 'C:\\Users\\admin\\Desktop\\a.txt'}
File moved successfully from E:\a.txt to C:\Users\admin\Desktop\a.txt.
```

查看C盘桌面是否存在a.txt呢？

![image-20251015111102701](Langchain使用之Tools/image-20251015111102701.png)

































