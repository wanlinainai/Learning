# Agent

## ReAct Agent的实现方式





## Plan And Execute

ReAct智能体采用：“思考 --> 行动 --> 观察”的循环模式，利用了思维链的提示，每一步只做一个行动选择。虽然对于简单的任务有效，但是存在问题：

- 低效率：串行决策导致任务执行缓慢，无法并行
- 短时规划：每一次仅仅考虑下一步，缺乏全局的视角，容易陷入次优路径
- 难以调试和审计：决策逻辑分散到多个LLM调用中，缺乏清晰的任务结构

Planner：规划器，调用LLM生成一个多步骤计划来完成一个大型的任务。

Executor：执行器，接收用户查询和计划中的一个步骤，并调用一个或者多个工具来完成这个任务。

**方案一：**

借助Langchain的实现方式：

1. 借助LLM来Plan规划，这一步不需要工具调用，也不需要记忆，其实严格意义上并不是一个智能体，只是一个LLM的调用。
2. 根据上一步规划的内容，通过React Agent来执行。
3. 根据执行的结果，在借助LLM判断是否需要rePlan重新规划，这一步也不需要记忆和工具调用，只是一个LLM调用。

**方案二：**

个人思考出来的一种方式：

1. 借助LLM来做规划，LLM结构化的输出具体每一步需要调用工具，以及入参是什么？
2. 根据上一步规划的内容，循环每一步做工具调用
3. 把工具调用的结果进行汇总，给到LLM做总结以及重新规划

**方案三：**

这种方案是多智能体的方案，三个角色都可以单独作为一个Agent来执行任务。

1. planner做规划，如果需要用到工具就直接调用。
2. executor根据上一步的规划内容，做每一个步骤的执行，如果用到工具调用工具。
3. replanner基于上一步的记过做判断以及重新规划，如果需要使用工具，直接调用工具。

除了上述的几种最基础的方案的话还有ReWoo和LLMCompiler，这是两种进化之后的方案，在原始的Plan And Executor做了关键的改进。

### ReWoo和LLMCompiler

ReWoo是一种允许Planner在生成计划的时候定义可引用的中间变量，实现任务之间的数据传递，不需要每一步调用LLM观察结果。

也就是下一步执行的工具需要参考上一个执行的工具的结果，依赖一个中间变量。

LLMCompiler解决的就是如果没有任务依赖的话也需要串行执行，浪费时间。为了解决这个问题，有人提出了LLMCompiler，将计划表示为有向无环图，流式解析 + 动态调度。实现最大的并行度。

## Agent 常用架构：Human in the Loop

Human in the Loop指的是在AI系统中自动决策或者执行的过程中，引入人类用户作为”必要参与者“，在关键节点对AI的行为和结果记性审查、确认和修改，而不是让模型自动完成端到端的执行。

- 高风险应用场景：
  - 写文件、删文件、改文件
  - 执行SQL相关
  - 调用外部系统接口
- 合规和审计要求
  - 关键操作必须有人类确认
  - 决策过程可回溯、可审计
- 模型不确定比较高

### 开箱即用HITL

Spring AI Alibaba已经存在了对Human In the Loop的支持，类：`HumanInTheLoopHook`来实现。

整个流程分成了三个阶段：

- 配置中断：在创建Agent的时候，配置那一些工具需要人工审批。
- 响应中断：在调用Agent运行逻辑，如果触发人工中断，返回中断元数据。
- 恢复执行：将人工决策反馈回传给Agent，并继续执行ReAct逻辑。

配置阶段，HumanInTheLoop明确表明工具需要人工审批，从而将”是否允许执行该工具“的决策权从模型侧上移到框架层，避免模型直接调用行为。

```java
// 配置检查点保存器（人工介入需要检查点来处理中断）
MemorySaver memorySaver = new MemorySaver();

// 创建人工介入Hook
HumanInTheLoopHook humanInTheLoopHook = HumanInTheLoopHook.builder() 
  .approvalOn("write_file", ToolConfig.builder() 
      .description("文件写入操作需要审批") 
      .build()) 
  .approvalOn("execute_sql", ToolConfig.builder() 
      .description("SQL执行操作需要审批") 
      .build()) 
  .build(); 

// 创建Agent
ReactAgent agent = ReactAgent.builder()
  .name("approval_agent")
  .model(chatModel)
  .tools(writeFileTool, executeSqlTool, readDataTool)
  .hooks(List.of(humanInTheLoopHook)) 
  .saver(memorySaver) 
  .build();
```

响应中断阶段，Agent正常进行推理，当模型生成了对受控工具的调用请求之后，框架在工具真正执行之前触发中断，返回`InterruptionMetadata`。此时Agent并没有失败，而是以一种”可恢复的中断状态“安全退出，将待执行的工具信息完整暴露给外部系统。

```java
String threadId = "user-session-123"; 
RunnableConfig config = RunnableConfig.builder() 
  .threadId(threadId) 
  .build(); 

// 运行图直到触发中断
Optional<NodeOutput> result = agent.invokeAndGetOutput( 
  "删除数据库中的旧记录",
  config
);

// 检查是否返回了中断
if (result.isPresent() && result.get() instanceof InterruptionMetadata) { 
  InterruptionMetadata interruptionMetadata = (InterruptionMetadata) result.get(); 

  // 中断包含需要审查的工具反馈
  List<InterruptionMetadata.ToolFeedback> toolFeedbacks = 
      interruptionMetadata.toolFeedbacks(); 

  for (InterruptionMetadata.ToolFeedback feedback : toolFeedbacks) {
      System.out.println("工具: " + feedback.getName());
      System.out.println("参数: " + feedback.getArguments());
      System.out.println("描述: " + feedback.getDescription());
  }

  // 示例输出:
  // 工具: execute_sql
  // 参数: {"query": "DELETE FROM records WHERE created_at < NOW() - INTERVAL '30 days';"}
  // 描述: SQL执行操作需要审批
}
```

在恢复执行阶段，外部系统基于中断信息构造人工反馈（批准、修改或修改），并通过相同的`threadId`将反馈重新注入Agent，Agent利用之前保存的执行状态继续执行，在人工决策约束之下后续的工具调用和推理流程，最终产生完整结果。

```java
List<InterruptionMetadata.ToolFeedback> toolFeedbacks =
              interruptionMetadata.toolFeedbacks();


InterruptionMetadata.Builder feedbackBuilder = InterruptionMetadata.builder()
              .nodeId(interruptionMetadata.node())
              .state(interruptionMetadata.state());

toolFeedbacks.forEach(toolFeedback -> {
              InterruptionMetadata.ToolFeedback approvedFeedback =
                  InterruptionMetadata.ToolFeedback.builder(toolFeedback)
                      .result(InterruptionMetadata.ToolFeedback.FeedbackResult.APPROVED)
                      .build();
              feedbackBuilder.addToolFeedback(approvedFeedback);
          });

InterruptionMetadata approvalMetadata = feedbackBuilder.build();


RunnableConfig resumeConfig = RunnableConfig.builder()
              .threadId(threadId)
              .addMetadata(RunnableConfig.HUMAN_FEEDBACK_METADATA_KEY, approvalMetadata)
              .build();

Optional<NodeOutput> finalResult = agent.invokeAndGetOutput("", resumeConfig);

if (finalResult.isPresent()) {
              System.out.println("执行完成");
              System.out.println("最终结果: " + finalResult.get());
}
```

整个过程中，HITL并没有改变模型推理方式，而是通过执行拦截、状态保存和恢复机制实现对Agent行为的强控制。

参考代码：HumanInTheLoopTest

## 多智能体（Multi Agent）

多智能体是由多个Agent组成的系统，这一些智能体能够感知环境、做出决策、与其他智能体交互，并协同或竞争以完成特定任务。

### 常见的协作模式

#### 子智能体模式

最主要的就是一个主智能体将其他子智能体视为工具，需要的时候调用。控制器管理编排，作为工具的子Agent执行特定的任务并返回结果。

主智能体决定调用哪一个子Agent，提供什么输入，以及如何组合结果。子Agent是无状态的，他们和用户直接交互，所有的对话和记忆都由代理维护。提供了上下文隔离：每一个子代理在他们自己的上下文窗口工作，防止主对话的上下文膨胀。

Langchain中的实现：

```python
from langchain.tools import tool
from langchain.agents import create_agent

# Create a subagent
subagent = create_agent(model="anthropic:claude-sonnet-4-20250514", tools=[...])

# Wrap it as a tool
@tool("research", description="Research a topic and return findings")
def call_research_agent(query: str):
    result = subagent.invoke({"messages": [{"role": "user", "content": query}]})
    return result["messages"][-1].content

# Main agent with subagent as a tool
main_agent = create_agent(model="anthropic:claude-sonnet-4-20250514", tools=[call_research_agent])
```

Spring AI Alibaba实现：

```java
// 创建子Agent
ReactAgent writerAgent = ReactAgent.builder()
.name("writer_agent")
.model(chatModel)
.description("可以写文章")
.tolls(...)
.instruction("你是一个知名的作家，擅长写作和创作。请根据用户的提问进行回答。")
.build();

// 创建主Agent，将子Agent作为工具
ReactAgent blogAgent = ReactAgent.builder()
.name("blog_agent")
.model(chatModel)
.instruction("根据用户给定的主题写一篇文章。使用写作工具来完成任务。")
.tools(AgentTool.getFunctionToolCallback(writerAgent))
.build();

// 使用
Optional<OverAllState> result = blogAgent.invoke("帮我写一个100字左右的散文");
```

#### HandOff

接管/交接，

核心思想是：**一个当前”智能体“在处理用户请求的时候，如果发现自己无法或不适合继续处理，他会主动将任务”交接“（hand off）给另一个更专业的智能体，并将控制权转移过去。**

#### Chat Group

群聊模式指的是：一组具有不同的专业角色的智能体（Agents）

- 所有参与者订阅同一个”Topic“（主题），形成一个共享的消息通道。
- 智能体按照顺序轮流发言，同一时间只有一个智能体在工作。
- 整个流程由一个特殊的”**群聊管理器**“控制，负责决定下一个该谁发言。

#### 自定义工作流

## 使用AutoGen构建一个代码生成器















