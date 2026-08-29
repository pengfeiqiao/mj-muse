# 客户端与 API 交接说明

本 Skill 只负责生成提示词组合，不负责调用服务。不同用户可能使用官方客户端、Discord、桌面工具、自动化工作流或第三方 API，因此不要假设域名、端点、鉴权方式和字段名称。

## 标准交接对象

把结果保持为以下中立结构：

```json
{
  "prompt": "final English visual prompt",
  "parameters": {
    "version": "v8.2",
    "aspectRatio": "16:9",
    "stylize": 300,
    "chaos": 0,
    "raw": false
  },
  "negativePrompt": "optional exclusions",
  "style": {
    "id": "style-id",
    "name": "风格名"
  }
}
```

## 交接规则

1. 用户自行决定客户端或 API，并自行配置密钥。
2. 调用方根据自己的文档映射字段，不在 Skill 内写死模型名、地址或请求体。
3. 客户端支持结构化参数时，`prompt` 中不重复添加同名 flags。
4. 客户端只接受命令文本时，可使用 `mj_style.py compose ... --format command` 生成单行组合。
5. 参考图 URL、上传方式、权重字段和安全策略均由调用方处理。
6. 未经用户明确要求，不提交网络请求，也不触发付费生成。

## Agent 行为

当用户只要求“写提示词”时，直接返回提示词组合。不要追问 API，也不要尝试选择渠道。只有用户明确要求“用我已配置的服务生成”时，才把组合结果交给当前环境中已经授权的工具。
