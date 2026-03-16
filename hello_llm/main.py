import os
from openai import OpenAI

try:
    client = OpenAI(
        api_key="sk-**************",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
    )

    completion = client.chat.completions.create(
        model="qwen-plus",
        messages=[
            {"role": "system", "content": "You are a dog"},
            {"role": "user", "content": "你是谁?"}
        ],
    )

    print(completion.choices[0].message.content)

except Exception as e:
    print(f"错误信息：{e}")