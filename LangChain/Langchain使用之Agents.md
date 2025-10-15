# Langchain使用之Agents

## Agent使用

### Agent、AgentExcutor的创建

|      | 创建Agent                                                    | 创建AgentExecutor           |
| ---- | ------------------------------------------------------------ | --------------------------- |
|      | AgentType指定                                                | initalize_agent()           |
|      | create_xxx_agent()<br />比如create_react_agent()、create_tool_calling_agent() | 调用AgentExecutor()构造方法 |

### Agent类型

Langchain中的Agent类型就是提供不同的“问题解决姿势”的。

API说明：https://python.langchain.com/v0.1/docs/modules/agents/agent_types/

Agents核心有两个模式：

- Function Call模式
- ReAct模式

#### Function_call模式

- 基于`结构化函数调用`(如OpenAI Function Calling)
- 直接生成工具调用参数（JSON格式）
- 效率更高，适合工具明确的场景

典型AgentType：

```python
# 1
AgentType.OPENAI_FUNCTIONS

# 2
AgentType.OPENAI_MULTI_FUNCTIONS
```

工作流程：

1. 找到Search工具：{"tool": "Search", "args": {"query": "Langchain最新版本"}}
2. 执行Search工具
3. 找到具体工具
4. 执行工具

#### ReAct模式

- 基于**文本推理**的链式思考（Reasoning + Acting），具有反思和自我纠错能力
  - 推理（Reasoning）：分析当前状态，决定下一步行动
  - 行动（Acting）：调用工具并返回结果
- 通过**自然语言描述决策过程**
- 适合需要明确推理步骤的场景。例如智能客服、问答系统、任务执行等

```python
#第1种：零样本推理(可以在没有预先训练的情况下尝试解决新的问题)
AgentType.ZERO_SHOT_REACT_DESCRIPTION
#第2种：无记忆对话
AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION
#第3种：带记忆对话
AgentType.CONVERSATIONAL_REACT_DESCRIPTION
```

工作流程：

```shell
问题：我想要查询xxx
思考：我需要先搜索最新信息 → 行动：调用Search工具 → 观察：获得3个结果 →
思考：需要抓取第一个链接 → 行动：调用scrape_website工具...→ 观察：获得工具结果
最后：获取结果
```

##### Agent两种类型对比

|   特性   |      Function Call模式      |      ReAct模式       |
| :------: | :-------------------------: | :------------------: |
| 底层机制 |       结构化函数调用        |     自然语言推理     |
| 输出格式 |       JSON/结构化数据       |       自由文本       |
| 适合场景 |      需要高效工具调用       |   需要解释决策过程   |
| 典型延迟 |     较低（参数化调用）      | 较高（生成完成文本） |
| LLM要求  | 需要支持函数调用（GPT - 4） |     通用模型即可     |

## Agent工具的使用

### 传统方式

#### 案例一：单工具使用

- 需求：今天北京天气怎么样？
- 使用Tavily搜索工具    [链接](https://www.tavily.com/)
  - Tavily搜索API是一个专门为人工智能Agent构建的搜索引擎，提供实时、准确和真实的结果。
  - Langchain中有一个内置工具，可以轻松使用`Tavily搜索引擎`作为工具。
  - TAVILY_API_KEY申请：https://app.tavily.com/home，注册账号获取API

**ReAct模式**



```python
from langchain.agents import AgentType, initialize_agent
from langchain_openai import ChatOpenAI
import os

import dotenv
from langchain_community.tools import TavilySearchResults

dotenv.load_dotenv()
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")
# 获取Tavily工具实例
search = TavilySearchResults(max_results=3)

# 获取LLM
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_BASE_URL"] = os.getenv("OPENAI_BASE_URL")
llm = ChatOpenAI(model="gpt-4o-mini")
# 创建Agent
agent = AgentType.ZERO_SHOT_REACT_DESCRIPTION
# 获取AgentExecutor
agent_executor = initialize_agent(
    tools=[search],
    llm=llm,
    agent=agent,
    verbose=True
)
# 通过AgentExecutor调用invoke()
result = agent_executor.invoke("查询青岛今天的天气情况")

print(result)
```

结果：

```shell
> Entering new AgentExecutor chain...
I need to find the current weather conditions in Qingdao for today.  
Action: tavily_search_results_json  
> Entering new AgentExecutor chain...
I need to find the current weather conditions in Qingdao for today.  
Action: tavily_search_results_json  
Action Input: 青岛今天的天气情况  
Observation: [......]
Thought:I have gathered multiple sources regarding the weather in Qingdao today. 

From the results, the current weather details are as follows:
- **Temperature**: Approximately 12.2°C to 20.8°C throughout the day.
- **Precipitation**: No significant rainfall.
- **Wind**: Northeast winds ranging from 5.2 m/s to 10.7 m/s.
- **Air Pressure**: Around 1016.1 hPa to 1029.1 hPa.

Older forecasts mention a maximum temperature reaching around 26°C with a low humidity level. 

Thought: I now know the final answer.
Final Answer: Qingdao's weather today is mostly clear with temperatures ranging from about 12.2°C to 26°C, no significant rainfall, and northeast winds.

> Finished chain.
{'input': '查询青岛今天的天气情况', 'output': "Qingdao's weather today is mostly clear with temperatures ranging from about 12.2°C to 26°C, no significant rainfall, and northeast winds."}
```

**使用Function Call**

```python
from langchain.agents import AgentType, initialize_agent
from langchain_openai import ChatOpenAI
import os

import dotenv
from langchain_community.tools import TavilySearchResults
from langchain_core.tools import StructuredTool, Tool

dotenv.load_dotenv()
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")
# 获取Tavily工具实例
search = TavilySearchResults(max_results=3)

# 获取LLM
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_BASE_URL"] = os.getenv("OPENAI_BASE_URL")
llm = ChatOpenAI(model="gpt-4o-mini")
# 创建Agent
agent = AgentType.OPENAI_FUNCTIONS
# 获取AgentExecutor
agent_executor = initialize_agent(
    tools=[search],
    llm=llm,
    agent=agent,
    verbose=True
)
# 通过AgentExecutor调用invoke()
result = agent_executor.invoke("查询青岛今天的天气情况")

print(result)
```

结果：

```shell
> Entering new AgentExecutor chain...

Invoking: `tavily_search_results_json` with `{'query': '青岛今天的天气情况'}`


> Entering new AgentExecutor chain...

Invoking: `tavily_search_results_json` with `{'query': '青岛今天的天气情况'}`


> Entering new AgentExecutor chain...

Invoking: `tavily_search_results_json` with `{'query': '青岛今天的天气情况'}`

今天青岛的天气情况如下：

- **气温**：白天最高约 26℃，夜间最低约 17℃
- **天气状况**：白天多云，预计将有小雨
- **风速**：风速在 3-4 级，主要来自东风
- **降水量**：今天预计降水量小
- **空气质量**：空气质量指数（AQI）较低，适合户外活动

更多详细天气信息可以参考 [中国天气网青岛天气预报](https://www.weather.com.cn/weather/101120201.shtml) 或 [中国气象局青岛天气预报](https://weather.cma.cn/web/weather/54857)。

> Finished chain.
{'input': '查询青岛今天的天气情况', 'output': '今天青岛的天气情况如下：\n\n- **气温**：白天最高约 26℃，夜间最低约 17℃\n- **天气状况**：白天多云，预计将有小雨\n- **风速**：风速在 3-4 级，主要来自东风\n- **降水量**：今天预计降水量小\n- **空气质量**：空气质量指数（AQI）较低，适合户外活动\n\n更多详细天气信息可以参考 [中国天气网青岛天气预报](https://www.weather.com.cn/weather/101120201.shtml) 或 [中国气象局青岛天气预报](https://weather.cma.cn/web/weather/54857)。'}
```

#### 多工具使用

- 需求：
  - 计算特斯拉当前股价是多少？
  - 相较于去年上涨了多少？

**ReAct 模式**

```python
from langchain.agents import AgentType, initialize_agent
from langchain_openai import ChatOpenAI
from langchain_experimental. utilities. python import PythonREPL
import os

import dotenv
from langchain_community.tools import TavilySearchResults

dotenv.load_dotenv()
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")
# 获取Tavily工具实例
search = TavilySearchResults(max_results=3)

# 搜索工具
search_tool = Tool(
    name="Search",
    func=search.run,
    description="用于检索互联网上的知识、信息"
)

# 定义计算工具
python_repl = PythonREPL()

calc_tool = Tool(
    name="Calculator",
    func=python_repl.run,
    description="用于执行数学计算，例如计算百分比计算"
)

# 定义LLM
llm = ChatOpenAI(
    model_name="gpt-4o-mini",
    temperature=0,
)

agent_executor = initialize_agent(
    tools=[search_tool, calc_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

query = "特斯拉当前股价是多少？相较于去年来说上涨了多少？"
result = agent_executor.invoke(query)
print(f"查询结果：{result}")
```

结果：

```shell
> Entering new AgentExecutor chain...
我需要查找特斯拉当前的股价以及去年的股价，以便计算它的涨幅。首先，我将搜索特斯拉的当前股价。  
Action: Search  
> Entering new AgentExecutor chain...
我需要查找特斯拉当前的股价以及去年的股价，以便计算它的涨幅。首先，我将搜索特斯拉的当前股价。  
Action: Search  
Action Input: "特斯拉当前股价"  
Observation:[]
Thought:
我没有找到特斯拉去年的确切股价，但根据一些信息，特斯拉的52周最低价为212.11美元。为了计算涨幅，我将假设去年的股价为212.11美元。  
Action: Calculator  
Action Input: "(435.54 - 212.11) / 212.11 * 100"  
Observation: 
我没有找到特斯拉去年的确切股价，但根据一些信息，特斯拉的52周最低价为212.11美元。为了计算涨幅，我将假设去年的股价为212.11美元。  
Action: Calculator  
Action Input: "(435.54 - 212.11) / 212.11 * 100"  
Observation: 
Thought:我已经计算出特斯拉股价的涨幅。  
Final Answer: 特斯拉当前股价为435.54美元，相较于去年的股价212.11美元，上涨了约105.63%。

> Finished chain.
查询结果：{'input': '特斯拉当前股价是多少？相较于去年来说上涨了多少？', 'output': '特斯拉当前股价为435.54美元，相较于去年的股价212.11美元，上涨了约105.63%。'}
```



**Function call 模式**

```python
from langchain.agents import AgentType, initialize_agent
from langchain_openai import ChatOpenAI
from langchain_experimental. utilities. python import PythonREPL
import os

import dotenv
from langchain_community.tools import TavilySearchResults

dotenv.load_dotenv()
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")
# 获取Tavily工具实例
search = TavilySearchResults(max_results=3)

# 搜索工具
search_tool = Tool(
    name="Search",
    func=search.run,
    description="用于检索互联网上的知识、信息"
)

# 定义计算工具
python_repl = PythonREPL()

calc_tool = Tool(
    name="Calculator",
    func=python_repl.run,
    description="用于执行数学计算，例如计算百分比计算"
)

# 定义LLM
llm = ChatOpenAI(
    model_name="gpt-4o-mini",
    temperature=0,
)

agent_executor = initialize_agent(
    tools=[search_tool, calc_tool],
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True
)

query = "特斯拉当前股价是多少？相较于去年来说上涨了多少？"
result = agent_executor.invoke(query)
print(f"查询结果：{result}")
```

结果：

```shell
Entering new AgentExecutor chain...

Invoking: `Search` with `特斯拉当前股价`


> Entering new AgentExecutor chain...

Invoking: `Search` with `特斯拉当前股价`


> Entering new AgentExecutor chain...

Invoking: `Search` with `特斯拉当前股价`

当前特斯拉（Tesla, TSLA）的股价为 **435.54 美元**。根据过去一年的数据，特斯拉的股价在52周内的最低点为 **212.11 美元**，因此相较于去年的最低点，当前股价上涨了：

\[
\text{上涨幅度} = \frac{435.54 - 212.11}{212.11} \times 100\%
\]

计算得出上涨幅度为：

\[
\text{上涨幅度} \approx 105.6\%
\]

因此，特斯拉的股价相较于去年的最低点上涨了约 **105.6%**。

> Finished chain.
查询结果：{'input': '特斯拉当前股价是多少？相较于去年来说上涨了多少？', 'output': '当前特斯拉（Tesla, TSLA）的股价为 **435.54 美元**。根据过去一年的数据，特斯拉的股价在52周内的最低点为 **212.11 美元**，因此相较于去年的最低点，当前股价上涨了：\n\n\\[\n\\text{上涨幅度} = \\frac{435.54 - 212.11}{212.11} \\times 100\\%\n\\]\n\n计算得出上涨幅度为：\n\n\\[\n\\text{上涨幅度} \\approx 105.6\\%\n\\]\n\n因此，特斯拉的股价相较于去年的最低点上涨了约 **105.6%**。'}
```

### 通用方式







































































