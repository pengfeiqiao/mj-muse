# Midjourney 提示词方法

## 1. 先锁事实

在改写前提取并保留：

- 主体及数量
- 身份与外观不可变项
- 动作和人物关系
- 道具与产品结构
- 场景和空间位置
- 构图、比例和输出用途
- 必须出现或禁止出现的内容

风格只能改变表达方式，不能改变这些事实。用户只说“更高级”时，不得因此新增角色、道具、文字或剧情。

## 2. 选择视觉机制

先按目的搜索风格，而不是按抽象形容词搜索：

```bash
python3 scripts/mj_style.py search "真实皮肤 直闪 人像"
python3 scripts/mj_style.py search "东方 金属 珠玉 暗背景"
python3 scripts/mj_style.py search "未来城市 生态 山谷"
```

优先选择一个风格。确实需要混合时，只借用另一个风格中的单一机制，例如“粉彩对称构图 + 真实产品材质”，不要把两个完整模板拼在一起。

## 3. 决定句首

- 写实、电影、人物、产品：主体与动作置首。
- 水墨、剪纸、刺绣、矢量、版画、黏土、像素等媒介：媒介置首。

媒介置首示例：

```text
traditional Chinese ink wash painting on xuan paper, a lone swordswoman crossing a reed marsh, broad dry-brush mountains, restrained mineral-red seal accents, large negative space
```

## 4. 写成可见画面

推荐顺序：

```text
subject and action, environment and spatial relationship, composition and camera, lighting and color, material or medium, finish and exclusions
```

每一块只保留能改变画面的词。与其写 `cinematic, beautiful, epic`，不如写 `28mm low-angle frame, foreground rubble, hard noon backlight, a human figure used as a scale cue`。

## 5. 使用参考图

先给每张参考图分工：

1. 身份或产品参考：主体必须保持。
2. 场景或构图参考：保留空间关系，不复制无关人物。
3. 风格参考：只取色彩、材质、光线和介质。

当主体保护优先时，降低 stylize 和 chaos，不让风格参考覆盖身份或结构。

## 6. 输出格式

普通输出：

```text
Style: raw-flash-intimacy
Prompt: close editorial portrait of ...
Parameters: version=v8.2, aspect_ratio=4:5, stylize=140, chaos=0, raw=true
Exclusions: plastic skin, excessive retouching, extra people
```

如果用户要可直接粘贴的命令，再输出拼好 flags 的单行文本。若交给结构化客户端，则参数与正文分开，不要重复写 flags。

## 7. 复核

提交前检查：

- 人数、身份、动作、关系和结构是否与用户一致。
- 是否出现用户没要求的对白、文字、道具或情节。
- 媒介词是否放在正确位置。
- 主风格是否只有一个。
- 参数是否与当前版本和用户自行配置的客户端兼容。
- 负面约束是否针对真实风险，而不是堆砌通用禁词。
