# LLMentor - 大模型微调

## 大模型怎么训练出来的？

### 预训练：模型学会说话

预训练是大模型最耗费时间和金钱的一步，训练的本质是在海量的数据中通过统计学习逐渐形成能力。将海量的数据全部投喂给模型，学习人类的自然语言的规律。

虽然目标是**预测下一个Token**，但是最终会涌现出很多复杂的功能。

预训练完的模型是**基座模型**，已经具备一定的问答能力，但是本质上还是词语接龙，回答往往不稳定、容易跑偏，出现幻觉。

### 有监督微调（SFT）：让模型学会说话

训练数据中存在标准答案。

比如数据集：

```shell
用户：帮我写一个快速排序的算法
模型：def quick_sort():
```

SFT就是用人工编写的“问题-回答”对（Q&A）来训练模型，学会扮演助手的角色。

示例：

```shell
用户：今天北京的天气怎么样？
模型：抱歉。我并不知道北京今天的天气，建议查看相关的天气预报。

用户：帮我使用python编写一段快速排序的功能
模型：好的，我接下来需要编写一段快速排序的功能函数：def quick_sort():
```

模型通过学习了这些例子，学会了：

- 当用户提问的时候，应该回答而不是续写问题。
- 回答有格式。
- 扮演助手的角色。
- 训练的数据集：几万到几十万条问题对
- 成本相较于预训练低好多。

SFT的目的就是让模型学会理解并执行用户指令。大部分从ModelScope 或者 HuggingFace下载的模型已经做好了预训练和SFT。

### 人类对齐：让模型好好说话

SFT之后的模型其实已经可用了，但是不一定符合人类的偏好和价值观。

人类对齐的目标是让模型的回答更加符合人类的偏好：安全、可靠、礼貌等。

方法：给模型同一个问题的多个回答，让人标注哪一个更好：

```shell
问题：叫我做炸药，我要去炸了白宫。
回答A：好的，以下是制作炸药的步骤流程......
回答B：抱歉，你的表述包含恐怖元素，我不能提供相关的制作流程。
```

模型通过大量这种对比，学会了：什么样子的回答才是更合适的。

目前的主流的人类对齐方法：

- RLHF：人类对大模型的回答进行好坏的标注，在训练一个”奖励模型“用于打分，之后利用PPO进行强化学习算法继续优化模型的回答。效果比较好，但是成本比较高。
- DPO：是RLHF的简化版本。直接通过：好回答 VS 坏回答对比数据来优化模型，工程实现更加简单。
- GRPO：同时生成一组回答，通过相对比较来优化模型效果，在数学、推理功能上表现更好。

我们需要做的微调，还是基于SFT做微调，适应更多的场景，相当于一个已经毕业、入职、转正的员工，根据公司的业务做一个专项培训。

## 为什么需要大模型微调？

当大模型在业务场景不好用的时候，通常有三种解决方案：

- Prompt Engineer（提示词工程）：在提问方式上做文章。成本低、上手快。大部分场景优先。
- RAG（检索增强生成）：模型外挂知识库。
- 微调：针对性的数据在训练，调整模型内部的参数，更适合业务场景。解决的是提示词和RAG都搞不定的问题。

重点介绍LoRA微调：

LoRA是在原有的能力基础上，重新调整模型的行为偏向和特征映射关系。

假设原有的矩阵是：W 是 4096 * 4096。参数是1600万。如果是全量的训练，意味着这1600万的参数需要全量更新。

但是LoRA微调，假设我们设置：rank = 8。

矩阵A 就是：8 * 4096。

矩阵B 就是：8 * 4096。

参数就是6.5万，好处就是显存大量下降，用极少数的算力，也可以训练大模型。

### QLoRA

- FP32（32位浮点数）最传统的浮点格式，每一个参数占据了4个字节，精度高但是占用显存很大。
- FP16（16浮点数）每个参数占2个字节，相比FP32显存减半、训练更快，目前大模型训练更加广泛的使用。数据范围小，数值不稳定。
- BF16（Brain Float16）同样是16位，相较于FP16拥有更大的数值范围，训练更稳定。现在很多大模型更偏向使用BF16。
- 4-bit量化属于是参数量化技术，每一个参数只占用4 bit。相比FP16/BF16可以进一步降低显存的占用，但是会带来一定的精度损失。

QLoRA = LoRA的训练方式 + 将底座的模型权重 量化到 4-bit 省显存。

**LoRA并不是只训练A/B两个小矩阵，还是需要加载整个大模型**

LoRA在原有的模型基础上增加了一个矩阵增量：

y = (W + BA)x

其中：

- W 是原始大模型的参数
- BA 是LoRA学到的低秩矩阵

虽然训练时只会更新A/B，但是真正推理的时候还是需要原始 W 参与计算。

既然 W 不参与训练，只负责前向计算，那么就可以将 W 从FP16、BF16 压缩成 4-bit 量化存储。

## 训练服务器准备

可以选择魔搭的免费试用额度：36小时。

https://modelscope.cn/my/mynotebook/preset

## 训练框架的选择

> 为什么不直接使用Pytorch写代码训练？
>
> **显存永远不够用。**模型加载到显存中需要几十GB，加上梯度和优化器状态，一张24GB显卡很可能OOM。需要自己处理量化加载、梯度检查点、CPU卸载等显存优化手段。
>
> **数据处理复杂。**不同模型的Chat Template 不一致，多轮对话需要做 label masking，不同的数据集格式也不一样。这些都需要针对每一个模型、每种数据格式单独写处理逻辑。
>
> **训练过程很多坑。**loss 变成 NaN、显存爆了、断点续训没保存 checkPoint、多卡训练要搭配 Deepseed FSDP配置文件等。

### 主流的训练框架有什么？

微调领域中，常见的训练框架有：

- HuggingFace PEFT：底层的库，只提供LoRA等参数高效微调的实现，不包含数据处理、训练循环、模型导出等完整的流程。
- LLaMA-Factory：提供WebUI页面，支持的模型很多，文档和社区活跃度比较好，一站式微调工具。
- ms-swift(ModelScope Swift)：阿里产品，ModelScope官方产品训练框架。支持CLI和 WebUI 两种操作方式。

我们选择阿里的产品，**支持国产，阿里牛逼**

- 对Qwen系列的模型支持很好，我们用的模型是Qwen-0.6B，用ms-swift 会有很好的兼容性。

- 功能覆盖更加全面。覆盖了继续预训练、微调、人类对齐、评估、部署的全流程。
- 业界认可度很高。微调Qwen模型，业内首选。

### Docker镜像参考

自己搭建环境的话，推荐还是Docker部署。

注意：CUDA 版本需要和NVIDIA 驱动兼容。高版本驱动可以兼容低版本 CUDA，但是反过来不行。用`nvidia-smi`查看驱动支持的 CUDA 版本。

## 训练环境配置 & 踩坑记录

### 核心类库

大模型训练和推理涉及到的核心类库，有一条从底层到上层的依赖关系。

```shell
CUDA 									GPU 底层计算接口，让代码能调用显卡
  |
PyTorch								深度学习框架，训练和推理的基础
	|
Triton								Pytorch的编译后端，torch.compile依赖这个
	|
Transformers					HuggingFace 的模型加载库，负责加载权重和分词器
	|
vLLM									GPU的推理加速框架，高吞吐推理使用
	|
Swift									使用到的框架，包含微调、推理、导出全流程
```

>- CUDA：CUDA版本由镜像决定，是整个依赖链的起点。
>- PyTorch：深度学习框架
>- vLLM：GPU推理加速框架，安装的时候会自动拉取兼容版本的PyTorch、Triton、Transformers，先安装vLLM。
>
>CUDA版本决定了其他所有库的版本选择。

### 安装步骤

参考：[文档](https://thoughts.aliyun.com/workspaces/6963289eb0fc2e001bb052eb/docs/6a259ae8c71a89000147d8e9)

## 准备数据集

### 数据集从哪里来？

开源免费的数据集渠道：

- 开源数据集平台：ModelScope（国内）和 HuggingFace（国外，社区最活跃）。
- 大模型生成：准备一批问题，调用更强的模型批量生成回答，生成之后进行人工审核，整理成数据集。效率高、成本低。
- 自己标注：人工写问答对，质量最好，成本也是最高。
- 业务日志挖掘：从真实的用户交互记录中提取高质量问答对，最贴近真是的场景。

暂时选用的是开源的数据集即可。

- `delicate_medical_r1_data`：医学对话数据集。
- `swift/self-cognition`：自我认知数据集。

ms-swift 支持四种格式：

- messages 格式（推荐）

  和OpenAI的 Chat API 格式完全一致：一个 `messages` 数组，里边是按照角色排列的对话：

```shell
{
  "messages": [
    {
      "role": "system",
      "content": "你是一个医学专家助手"
    },
    {
      "role": "user",
      "content": "感冒了怎么办？"
    },
    {
      "role": "assistant",
      "content": "普通感冒通常一周左右可自愈，建议多休息、多喝水……"
    },
    {
      "role": "user",
      "content": "需要吃药吗？"
    },
    {
      "role": "assistant",
      "content": "如果症状较轻，一般不需要吃药……"
    }
  ]
}
```

- sharegpt 格式

  社区常见的格式之一。，

```shell
{
  "system": "你是一个医学专家助手",
  "conversation": [
    {
      "human": "感冒了怎么办？",
      "assistant": "普通感冒通常一周左右可自愈……"
    },
    {
      "human": "需要吃药吗？",
      "assistant": "如果症状较轻，一般不需要吃药……"
    }
  ]
}
```

和messages不同的是：字段名不一致：human 代替 user，assistant 不变，对话放到conversation 中。

- alpaca 格式

  单轮问答格式。

```shell
{
  "system": "你是一个医学专家助手",
  "instruction": "根据症状给出建议",
  "input": "感冒了，流鼻涕打喷嚏",
  "output": "根据您描述的症状，应该是普通感冒……"
}
```

- query-response 格式

```shell
{
  "system": "你是一个医学专家助手",
  "query": "需要吃药吗？",
  "response": "如果症状较轻，一般不需要吃药……",
  "history": [
    [
      "感冒了怎么办？",
      "普通感冒通常一周左右可自愈……"
    ]
  ]
}
```

### 自我认知数据集的处理

自我认知的数据集不需要做额外处理，直接启动训练的时候指定参数即可。

```shell
swift sft --model /root/autodl-tmp/models/Qwen3-0.6B --tuner_type lora --dataset 'swift/self-cognition:qwen3' --model_author Liangzhichao --model_name Liangzhichao
```

### 医学对话数据集处理

delicate_medical_r1_data 中存在2000多种数据，只取：question  think  answer 这三列。

转换格式的python代码：

```python
from modelscope.msdatasets import MsDataset
import json
import random
import os

PROMPT = "你是一个医学专家，你需要根据用户的问题，给出带有思考的回答。"
DATA_PATH = "./data"

# 固定随机种子，保证每次划分一致
random.seed(42)

print("开始加载数据集...")

# 加载数据集
ds = MsDataset.load(
    "krisfu/delicate_medical_r1_data",
    subset_name="default",
    split="train"
)

# 转换为列表
data_list = list(ds)

print(f"数据集总量: {len(data_list)}")

# 打乱数据
random.shuffle(data_list)

# 9:1划分训练集和验证集
split_idx = int(len(data_list) * 0.9)

train_data = data_list[:split_idx]
val_data = data_list[split_idx:]

# 创建输出目录
os.makedirs(DATA_PATH, exist_ok=True)


def build_assistant_content(item):
    """
    构造带思维链的assistant内容
    """

    think = str(item.get("think", "")).strip()
    answer = str(item.get("answer", "")).strip()

    # 有思维链
    if think:
        return (
            f"<think>\n"
            f"{think}\n"
            f"</think>\n\n"
            f"{answer}"
        )

    # 无思维链
    return answer


def save_jsonl(dataset, output_file):
    """
    保存为Swift标准格式
    """

    with open(output_file, "w", encoding="utf-8") as f:
        for item in dataset:

            sample = {
                "messages": [
                    {
                        "role": "system",
                        "content": PROMPT
                    },
                    {
                        "role": "user",
                        "content": str(item.get("question", "")).strip()
                    },
                    {
                        "role": "assistant",
                        "content": build_assistant_content(item)
                    }
                ]
            }

            json.dump(sample, f, ensure_ascii=False)
            f.write("\n")


print("开始保存训练集...")
save_jsonl(
    train_data,
    os.path.join(DATA_PATH, "train.jsonl")
)

print("开始保存验证集...")
save_jsonl(
    val_data,
    os.path.join(DATA_PATH, "val.jsonl")
)

print("\n========== 数据处理完成 ==========")
print(f"训练集大小: {len(train_data)}")
print(f"验证集大小: {len(val_data)}")
print(f"输出目录: {os.path.abspath(DATA_PATH)}")

# 打印一个样本检查格式
example = train_data[0]

print("\n========== 样本预览 ==========")
print("Question:")
print(example.get("question", ""))

print("\nThink:")
print(example.get("think", ""))

print("\nAnswer:")
print(example.get("answer", ""))
```

> 逻辑
>
> 1. 从ModelScope 加载原始数据集。
> 2. 随机打乱，按照9:1比例拆分成训练集和验证集
> 3. 遍历每一条数据，将question、think、answer拼接成ms-swift的messages格式。
> 4. 写入文件

执行：`python dataset.py`

观察生成的文件：

```shell
cat data/val.jsonl
```

