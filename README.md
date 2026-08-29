# MJ Muse

MJ Muse 是一套独立、可移植的 Midjourney 提示词 Agent Skill。它把鲲鹏中的提示词方法、参数策略和风格库整理为可供 Codex、Claude Code、Cursor 及其他支持 Agent Skills 的工具使用的公开仓库。

## 内容

- 60 个经过生产出图校准的风格预设
- 24 个按视觉机制整理的导演校准预设
- V8.2 / V8.1 / Niji 的参数与兼容规则
- 主体事实锁、参考图分工、媒介置首和防止过度扩写的提示词方法
- 零依赖的风格搜索与提示词组合脚本

Skill 是纯提示词组合器，不包含网络请求、API Key、中转站、鉴权、路由或计费逻辑，也不会自行触发付费生成。`client-integration.md` 仅说明如何把提示词结果交给用户自行配置的客户端或 API。

## 安装

克隆仓库：

```bash
git clone https://github.com/pengfeiqiao/mj-muse.git
```

Codex：

```bash
cp -R mj-muse/mj-muse ~/.codex/skills/
```

Claude Code 或其他支持 Agent Skills 的工具：将 `mj-muse` Skill 文件夹复制到该工具的 Skills 目录。若工具没有 Skills 目录，让 Agent 直接读取其中的 `SKILL.md` 也可以使用。

## 使用

对 Agent 说：

```text
使用 $mj-muse，把“雨夜古城里的年轻剑客”改写为真实电影感的 Midjourney 提示词。
```

搜索风格：

```bash
python3 mj-muse/scripts/mj_style.py search "东方 珠玉 暗背景"
```

查看风格：

```bash
python3 mj-muse/scripts/mj_style.py show ceremonial-jewelry
```

生成结构化提示词与参数：

```bash
python3 mj-muse/scripts/mj_style.py compose mecha-ruin "a lunar rover" --aspect-ratio 16:9
```

## 设计原则

风格不能改写事实。主体、数量、身份、动作、关系、产品结构、构图和文字要求都先锁定，再叠加视觉机制。风格库使用可观察的镜头、光线、材质、媒介和构图语言，不要求模仿在世艺术家或受保护 IP。

## License

MIT
