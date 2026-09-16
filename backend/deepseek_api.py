import os
from typing import Any, Literal

from openai import OpenAI
from openai.types import ReasoningEffort
from openai.types.chat import (
    ChatCompletionMessageParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
)

# API Key 从环境变量读取，不要在源码中写明文 Key
_deepseek_api_key = os.environ.get("DEEPSEEK_API_KEY")
# DeepSeek OpenAI 兼容接口地址
_base_url = "https://api.deepseek.com/v1"

# 指定调用的模型
_model = "deepseek-flash"

# 构造需要发送的上下文信息
_messages: list[ChatCompletionMessageParam] = [
    ChatCompletionSystemMessageParam(
        # system 用于设定模型身份和回答规则
        role="system",
        content="介绍一下你自己。",
    ),
    # ChatCompletionUserMessageParam(
    #     # user 表示用户本次提出的问题
    #     role="user",
    #     content="回答一下你是什么模型。",
    # ),
]

# 限制本次最多生成的 Token 数量
_max_tokens = 1024

# False 表示等待生成完毕后一次性返回
# Literal[False] 让 SDK 明确返回 ChatCompletion，避免被推断成 Stream
_stream: Literal[False] = False

# 思考强度："none", "minimal", "low", "medium", "high", "xhigh", "max"
_reasoning_effort: ReasoningEffort = "none"

# extra_body 用于传递 OpenAI SDK 未直接定义的 DeepSeek 扩展参数
_extra_body: dict[str, Any] = {
    "thinking": {
        # enabled 开启思考模式，disabled 关闭思考模式
        "type": "enabled",
    }
}

# 创建 DeepSeek 客户端
deepseek_client = OpenAI(
    api_key=_deepseek_api_key,
    base_url=_base_url,
)

# 向 DeepSeek 发送请求并等待非流式响应
completion = deepseek_client.chat.completions.create(
    model=_model,
    messages=_messages,
    max_tokens=_max_tokens,
    stream=_stream,
    reasoning_effort=_reasoning_effort,
    extra_body=_extra_body,
)

# 读取模型的最终回答
print(completion.choices[0].message.content)
# 打印 Token 消耗
usage = completion.usage
if usage:
    print("输入 Token：", usage.prompt_tokens)
    print("输出 Token：", usage.completion_tokens)
    print("总 Token：", usage.total_tokens)
