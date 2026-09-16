import os

from openai import OpenAI
from openai.types.chat import (
    ChatCompletionMessageParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
)

_moonshot_api_key = os.environ.get("MOONSHOT_API_KEY")
_base_url = "https://api.moonshot.cn/v1"

messages: list[ChatCompletionMessageParam] = [
    ChatCompletionSystemMessageParam(
        role="system",
        content="你是 Kimi，由 Moonshot AI 提供的人工智能助手。",
    ),
    ChatCompletionUserMessageParam(
        role="user",
        content="你好，我叫李雷，1+1等于多少？",
    ),
]

kmi_client = OpenAI(
    api_key=_moonshot_api_key,
    base_url=_base_url,
)

completion = kmi_client.chat.completions.create(
    model="kimi-k2.6",
    messages=messages,
    stream=False,
)

# 读取模型的最终回答
print(completion.choices[0].message.content)
# 打印 Token 消耗
usage = completion.usage
if usage:
    print("输入 Token：", usage.prompt_tokens)
    print("输出 Token：", usage.completion_tokens)
    print("总 Token：", usage.total_tokens)
