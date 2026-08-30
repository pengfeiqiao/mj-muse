---
name: shotlab-mj
description: 为 ShotLab 的 Midjourney 模型生成不超过 1000 字符的视觉提示词，并提供 84 种风格、参数策略、事实锁与参考图分工。
---

# ShotLab MJ

这是供 ShotLab 和其他只能读取单个 Markdown 文件的 Agent 使用的完整版本。它是纯提示词组合器，不包含网络请求、API Key、固定端点、鉴权、路由或付费生成逻辑。

## 最高优先级约束

ShotLab 的 Midjourney 输入存在 **1000 个 Unicode 字符硬上限**。任何准备交给模型的单条完整提交文本都必须先通过长度检查；超过 1000 字符时不得提交，也不得机械截断，必须在保留事实锁的前提下重写压缩。这个约束优先于风格丰富度、示例完整度和其他所有提示词规则。

- 常规目标：完整提交文本控制在 **550–750 字符**，为后续参数和客户端差异预留余量。
- 同一输入框还要拼接参数或参考图 URL 时：正文通常控制在 **400–600 字符**，并按实际 URL 长度继续缩短。
- 多套方案逐条独立计数，不允许用“平均长度”代替逐条校验。
- 无法可靠计数时，完整提交文本按 **不超过 600 字符**处理，不要贴近 1000 字符边界。
- 1000 是拒绝阈值，不是推荐目标。最终文本应尽量短而有效。

## 核心任务

把用户的画面需求改写为精确、可见、可执行的 Midjourney 英文提示词。风格只能改变表达方式，不得擅自改变主体、数量、身份、动作、关系、产品结构、空间位置、画幅或必需文字。

## 标准工作流

1. **建立事实锁**：提取主体、数量、身份、动作、空间关系、场景、构图、用途、比例和禁止项。除非用户明确要求，否则这些事实不可改变。
2. **选择一个主风格**：从文末 84 种风格中选择最匹配的一种。确需混合时，只借用第二种风格中的一个具体机制，不拼接两个完整模板。
3. **套用模板**：用用户主题替换 `{subject}`。如果模板没有 `{subject}`，把用户主题放在模板前。
4. **组织提示词**：主体身份与动作 → 环境与空间关系 → 构图与镜头 → 光线与色彩 → 材质或媒介 → 成片质感与排除项。
5. **执行长度闸门**：先组装最终会提交的完整字符串，再计数；不得超过 1000 个字符。常规目标为 550–750 个字符，同栏含参数或 URL 时进一步缩短。
6. **给出参数**：默认 V8.2、stylize 300、chaos 0、raw 关闭。风格预设可覆盖默认值，用户明确指定的参数优先级最高。
7. **复核事实**：确认没有新增人物、对白、道具、品牌、符号、文字、动作或人物关系。

## 提示词纪律

- 使用具体可见的镜头、光线、材质、构图和媒介机制，不堆叠 `masterpiece`、`best quality`、`stunning` 等空泛词。
- 摄影、电影、人物和产品画面以主体与动作开头。水墨、剪纸、刺绣、矢量、版画、黏土、像素等媒介型画面以媒介开头。
- 不模仿在世艺术家或受保护 IP；把参考转译为对称、配色、镜头、笔触、材质、制作工艺和光线。
- 不承诺精确文字渲染。必须准确显示文字时，建议使用文字能力更强的模型或后期合成。
- 默认不用于多镜故事板连续性；用户明确选择 Midjourney 做故事板时再使用。
- 用户只要求提示词时，只返回提示词，不讨论 API。

## ShotLab 1000 字符硬限制

- **硬上限**：传入 ShotLab Midjourney 模型的每条完整提示词必须不超过 1000 个 Unicode 字符。多张图或多套方案时，每条分别计数。
- **计数范围**：同一输入框内会提交给模型的正文、`--no` 排除项、版本、比例、stylize、chaos、raw、seed 等参数都计入；单独的结构化参数栏或独立参考图上传不计入正文。
- **安全目标**：完整提交文本优先控制在 550–750 字符；需要同栏拼接参数或参考图 URL 时，正文通常控制在 400–600 字符，并为实际参数与 URL 预留长度。
- **禁止机械截断**：不得直接截取前 1000 字符，因为这会切断人物关系、否定条件或参数。超限时必须重写并重新计数。
- **压缩顺序**：先删除空泛质量词和重复形容词 → 合并同义镜头、光线、材质描述 → 每类只保留一个最有效机制 → 删除非关键排除项 → 最后缩短风格修饰。主体、数量、身份、动作、空间关系、产品结构、必需文字与用户禁止项不得为了长度而删除。
- **风格库用法**：风格条目是选择与改写依据，绝不能把条目的“视觉机制、镜头语言、模板、风格补充”整段同时复制进最终提示词。
- **输出前校验**：组装正文、URL 与 flags 后再计算整条字符串的 Unicode 字符数；超过 1000 就继续压缩，直到通过。能使用本地工具时用字符串长度函数复核；没有计数工具时采用不超过 600 字符的保守版本。无法在不损害事实锁的情况下压缩时，先向用户说明冲突，不提交超长提示词。

### 强制提交闸门

每条提示词都必须独立执行以下流程：

1. 先完成事实锁与提示词改写。
2. 拼好实际要提交的正文、参考图 URL 和参数 flags。
3. 计算整条提交字符串的字符数。
4. 若长度大于 1000，按压缩顺序重写后重新计数。
5. 只有长度小于或等于 1000 时才允许输出为“可提交提示词”。

不要先输出超长版本再附一份短版；默认只交付已经通过闸门的版本。用户要求解释时，可以另行说明取舍，但解释文字不得混入提交字符串。

### 超限压缩模板

最终提示词只保留六类高信息密度内容，通常每类一句或一个短语：

1. 主体、数量、身份与关键动作。
2. 必要的空间关系和场景。
3. 一个主要构图与一个镜头机制。
4. 一个主要光线机制与核心配色。
5. 一个材质或媒介机制。
6. 少量真正影响结果的排除项与参数。

删除重复的风格名、同义形容词、解释性语言、创作过程描述和泛化质量词。不要把风格条目的视觉机制、镜头语言、模板和风格补充四段同时复制到最终提示词。

## 三种参数模式

| 模式 | 初始值 | 适用场景 |
| --- | --- | --- |
| 忠实 faithful | stylize 140, chaos 0, raw on | 人物身份、产品结构、纪实摄影、严格构图 |
| 平衡 balanced | stylize 300, chaos 0, raw off | 常规视觉开发、电影感、东方美学 |
| 探索 exploratory | stylize 300, chaos 25, raw off | 概念探索、构图发散、材料实验 |

### 参数调整

- 更真实、少 AI 感：raw 开启，stylize 80–160，chaos 0。
- 更艺术、更华丽：在预设基础上将 stylize 增加 100–150，通常不超过 500。
- 需要多个明显不同方向：chaos 20–30。chaos 不是画质增强。
- 保持主体与构图：chaos 0，stylize 不高于 150；客户端支持时固定 seed。
- 产品、UI、标志：stylize 0–80，chaos 0，明确产品结构与留白。
- 怪诞实验：仅在用户明确要求时使用 weird 100–300。
- V8.2 不沿用旧版 quality/q 参数。Niji 不与普通 `--v` 同时使用。
- 客户端支持结构化参数时，不在 prompt 中重复相同 flags；只接受命令文本时再拼接 flags。

## 参考图分工

1. **身份或产品参考**：保护人物身份、物体结构和不可变细节。
2. **场景或构图参考**：保留空间关系和构图，不复制无关人物。
3. **风格参考**：只提取色彩、材质、光线、镜头与媒介。

主体保护优先时，降低 stylize 和 chaos。提示词描述最终画面，不写“参考图片一”“把图片改成”等过程性语言，除非用户使用的客户端明确要求索引语法。

## 输出格式

```text
Style: 风格名称 (style-id)
Prompt: final English visual prompt (完整提交内容必须不超过 1000 字符，建议 550–750)
Parameters: version=v8.2, aspect_ratio=16:9, stylize=300, chaos=0, raw=false
Exclusions: only the exclusions relevant to this image
Length: N/1000
```

`Length` 统计实际会提交给模型的完整文本，不统计 `Style:` 等说明标签。用户要求可直接粘贴的命令时，才把参数编译为单行 flags，并对合并后的整行重新计数。只有 `Length <= 1000` 的结果才可标记为可提交。API 或客户端由用户自行配置；本文件只提供中立的提示词与参数结果。

## 提交前检查

- 人数、身份、动作、关系、产品结构与用户要求一致。
- 没有新增对白、文字、道具、剧情或品牌。
- 媒介词处于正确位置。
- 只有一个主风格。
- 参数与用户选择的版本和客户端兼容。
- 排除项针对真实风险，不堆砌通用禁词。
- 实际提交文本已经计数，长度不超过 1000 个字符，且没有用截断破坏语义。

## 完整风格库

使用时先按中文名称、ID、类别或视觉机制检索。`promptTemplate` 是主模板；将 `{subject}` 替换为已经锁定事实的用户主题。

### 1. 战损机甲 (`mecha-ruin`)

- **类别**：电影叙事
- **校准**：生产校准
- **视觉机制**：巨物机甲 × 废墟尺度 × 岁月侵蚀。剥落白漆、锈迹、油污、混凝土断壁，低角度仰拍制造压迫感，自然硬光下的真实材质。
- **镜头语言**：低角度仰拍 / 广角 / 浅景深前景遮挡 / 硬光
- **提示词模板**：a colossal battle-worn {subject} covered in rust and peeling paint, amid collapsed concrete ruins, dust and debris floating in the air, low angle shot, harsh midday sunlight, photorealistic weathered textures, cinematic film still
- **风格补充**：weathered textures, rust, battle damage, dust, ruins, photorealistic
- **创意模式**：平衡
- **推荐版本**：v8.2
- **推荐参数**：stylize=300, chaos=0, aspectRatio=2:3, referenceStrategy=prompt

### 2. 鎏金国风 (`gilded-oriental`)

- **类别**：东方美学
- **校准**：生产校准
- **视觉机制**：极繁东方宫廷美学。鎏金凤冠、红金刺绣、珠玉堆叠，暗背景 + 戏剧性明暗（chiaroscuro），hyper-detail 工艺感。
- **镜头语言**：特写/半身肖像 / 暗背景 / 戏剧性侧光
- **提示词模板**：{subject} wearing an ornate gilded phoenix headdress and red-gold embroidered hanfu, intricate jewelry and jade ornaments, dark background, dramatic chiaroscuro lighting, hyper-detailed, cinematic portrait
- **风格补充**：gilded, ornate, intricate jewelry, red and gold, hyper-detailed, dark background
- **创意模式**：平衡
- **推荐版本**：v8.2
- **推荐参数**：stylize=400, chaos=0, aspectRatio=9:16, referenceStrategy=prompt

### 3. 东方玄幻 (`oriental-fantasy`)

- **类别**：东方美学
- **校准**：生产校准
- **视觉机制**：仙侠史诗。云海之上的浮空宫殿、金色符文、白衣修士剪影，巨物比例与万丈霞光，ethereal 空灵光感。
- **镜头语言**：超广角大远景 / 人物剪影点景 / 逆光
- **提示词模板**：a lone figure in flowing white robes standing on a cliff before {subject}, a sea of clouds at sunset, glowing golden runes drifting in the air, epic scale, ethereal light, cinematic wide shot
- **风格补充**：sea of clouds, golden runes, epic scale, ethereal light, floating palace
- **创意模式**：平衡
- **推荐版本**：v8.2
- **推荐参数**：stylize=300, chaos=0, aspectRatio=16:9, referenceStrategy=prompt

### 4. 武侠雨夜 (`wuxia-rain`)

- **类别**：东方美学
- **校准**：生产校准
- **视觉机制**：武侠电影质感。雨夜庭院、灯笼暖光对蓝灰冷调、剑舞动作模糊、石板反光，写意与力量感并存。
- **镜头语言**：中全景动作 / 慢门动作模糊 / 暖冷对比光
- **提示词模板**：{subject} in a rain-soaked ancient Chinese courtyard at night, sword dance motion blur, warm lantern light against blue-grey tones, wet stone reflections, cinematic wuxia film still
- **风格补充**：rain, motion blur, lantern light, blue-grey palette, wet reflections, wuxia
- **创意模式**：平衡
- **推荐版本**：v8.2
- **推荐参数**：stylize=250, chaos=0, aspectRatio=16:9, referenceStrategy=prompt

### 5. 暗夜骑士 (`dark-knight`)

- **类别**：电影叙事
- **校准**：生产校准
- **视觉机制**：暗黑史诗。黑色繁复铠甲、单色红光辉光、红雾弥漫、巨像阴影，极端对比与戏剧性轮廓光。
- **镜头语言**：背影全景 / 极低饱和度+单色辉光 / 戏剧性 rim light
- **提示词模板**：{subject} in ornate black armor holding a glowing red energy sword, red mist swirling, shadowy ancient statues in the background, extreme contrast, dramatic rim lighting, dark fantasy film still
- **风格补充**：black armor, red glow, mist, high contrast, dark fantasy, rim light
- **创意模式**：平衡
- **推荐版本**：v8.2
- **推荐参数**：stylize=300, chaos=0, aspectRatio=9:16, referenceStrategy=prompt

### 6. 质感人像 (`raw-portrait`)

- **类别**：真实摄影
- **校准**：生产校准
- **视觉机制**：编辑类真实感人像。雀斑、毛孔、碎发等真实肌理，方向性柔光，胶片颗粒，拒绝磨皮 AI 感。必须 --style raw。
- **镜头语言**：特写 / 浅景深 / 窗光柔光
- **提示词模板**：close-up portrait of {subject}, freckles and windswept hair, intense gaze, natural skin texture, soft directional window light, editorial photography, shot on Kodak Portra 400
- **风格补充**：natural skin texture, freckles, editorial photography, Kodak Portra 400, film grain
- **创意模式**：忠实
- **推荐版本**：v8.2
- **推荐参数**：stylize=150, chaos=0, raw=true, aspectRatio=4:5, referenceStrategy=prompt

### 7. 沙漠史诗 (`desert-epic`)

- **类别**：电影叙事
- **校准**：生产校准
- **视觉机制**：沙丘式巨物美学。金色霾雾、巨型沙丘/巨物剪影、人物渺小如豆，单色调金色 palette，史诗尺度。
- **镜头语言**：21:9 超宽画幅 / 大远景 / 剪影点景
- **提示词模板**：two tiny figures on the ridge of a massive golden sand dune at dusk, {subject} emerging in the atmospheric haze, epic scale, golden monochrome palette, cinematic film still
- **风格补充**：golden haze, epic scale, tiny figures, atmospheric, monochrome gold, dune
- **创意模式**：平衡
- **推荐版本**：v8.2
- **推荐参数**：stylize=250, chaos=0, aspectRatio=21:9, referenceStrategy=prompt

### 8. 梦幻田园 (`dream-pastoral`)

- **类别**：电影叙事
- **校准**：生产校准
- **视觉机制**：梦境油画。发光花海、白马、巨月、雪山，印象派笔触与 ethereal 光感，现实与梦境交叠。
- **镜头语言**：广角风景 / 油画质感 / 月光逆光
- **提示词模板**：{subject} galloping through a luminous meadow of glowing white flowers, a crystal river winding through the valley, snow-capped mountains under a giant moon, dreamy oil painting, ethereal light, impressionist style
- **风格补充**：glowing flowers, giant moon, dreamy, oil painting, ethereal light, impressionist
- **创意模式**：平衡
- **推荐版本**：v8.2
- **推荐参数**：stylize=400, chaos=0, aspectRatio=16:9, referenceStrategy=prompt

### 9. 赛博霓虹 (`cyber-neon`)

- **类别**：电影叙事
- **校准**：生产校准
- **视觉机制**：赛博都市雨夜。霓虹广告牌、湿滑路面反射、青与品红撞色、透明雨伞剪影，孤独感都市氛围。
- **镜头语言**：竖屏街景 / 背影 / 霓虹反射前景
- **提示词模板**：{subject} walking through a rain-soaked neon-lit street at night, transparent umbrella, vivid reflections on wet pavement, towering cyberpunk billboards, teal and magenta palette, cinematic atmosphere
- **风格补充**：neon, rain, wet reflections, teal and magenta, cyberpunk, night street
- **创意模式**：平衡
- **推荐版本**：v8.2
- **推荐参数**：stylize=300, chaos=0, aspectRatio=9:16, referenceStrategy=prompt

### 10. 云海青春动画 (`anime-sky`)

- **类别**：插画动画
- **校准**：生产校准
- **视觉机制**：当代光影动画。积雨云夕阳、镜头光晕、高饱和渐变天空、日常物件的诗意，niji7 通道。
- **镜头语言**：广角天空占比 70% / 人物小剪影 / 镜头光晕
- **提示词模板**：{subject} watching a breathtaking sunset sky with towering cumulonimbus clouds, lens flare, vibrant colors, luminous contemporary anime film style anime illustration
- **风格补充**：cumulonimbus, sunset sky, lens flare, vibrant, luminous contemporary anime film style, anime
- **创意模式**：平衡
- **推荐版本**：niji7
- **推荐参数**：stylize=200, chaos=0, aspectRatio=16:9, referenceStrategy=prompt

### 11. 极简产品 (`minimal-product`)

- **类别**：商业设计
- **校准**：生产校准
- **视觉机制**：高级产品摄影。粗粝石座/几何台、柔和渐变背景、戏剧性侧光长影，less is more。低 stylize 保真。
- **镜头语言**：1:1 居中构图 / 影棚侧光 / 长阴影
- **提示词模板**：{subject} on a rough stone pedestal, soft beige gradient background, dramatic side lighting with long shadows, minimalist product photography, studio shot
- **风格补充**：minimalist, product photography, studio lighting, soft gradient, stone pedestal
- **创意模式**：平衡
- **推荐版本**：v8.2
- **推荐参数**：stylize=50, chaos=0, aspectRatio=1:1, referenceStrategy=prompt

### 12. 胶片街头 (`film-street`)

- **类别**：真实摄影
- **校准**：生产校准
- **视觉机制**：纪实胶片。雾中渔港、晨曦、劳作的人，Kodak Portra 400 暖调，人文纪实人文摄影。必须 --style raw。
- **镜头语言**：3:2 纪实构图 / 晨雾逆光 / 抓拍感
- **提示词模板**：{subject} at dawn in the mist, candid documentary photography, muted warm tones, Kodak Portra 400, humanist documentary photography
- **风格补充**：documentary, candid, misty, dawn light, Kodak Portra 400, muted warm tones
- **创意模式**：忠实
- **推荐版本**：v8.2
- **推荐参数**：stylize=150, chaos=0, raw=true, aspectRatio=3:2, referenceStrategy=prompt

### 13. 水墨丹青 (`ink-wash`)

- **类别**：东方美学
- **校准**：生产校准
- **视觉机制**：传统水墨。宣纸墨韵、大笔触、大面积留白，墨色浓淡 + 淡青点缀，写意山水渔舟。
- **镜头语言**：横构图大远景 / 留白构图 / 平面化
- **提示词模板**：traditional Chinese ink wash painting of {subject}, sumi-e, visible black ink brush strokes on xuan rice paper, ink bleed texture, generous negative space, minimal composition
- **风格补充**：ink wash, sumi-e, brush strokes, xuan paper, negative space
- **排除项**：photo, photorealistic, 3D, color photography
- **创意模式**：平衡
- **推荐版本**：v8.2
- **推荐参数**：stylize=400, chaos=0, aspectRatio=16:9, referenceStrategy=prompt

### 14. 敦煌飞天 (`dunhuang`)

- **类别**：东方美学
- **校准**：生产校准
- **视觉机制**：敦煌壁画。飞天飘带、矿物色（赭红/石绿/青金）、金箔、斑驳洞窟肌理，平面装饰线描。
- **镜头语言**：全身立像 / 平面装饰 / 斑驳肌理
- **提示词模板**：weathered Dunhuang fresco mural depicting {subject}, flat decorative line art, mineral pigments of ochre red, malachite green and lapis blue, gold leaf details, mottled cave wall texture, ancient mural craft
- **风格补充**：Dunhuang fresco, mineral pigments, gold leaf, weathered cave wall, flat decorative
- **排除项**：oil painting, realistic skin, photography
- **创意模式**：平衡
- **推荐版本**：v8.2
- **推荐参数**：stylize=400, chaos=0, aspectRatio=9:16, referenceStrategy=prompt

### 15. 赛博国潮 (`cyber-guochao`)

- **类别**：东方美学
- **校准**：生产校准
- **视觉机制**：赛博×国潮。霓虹中文招牌、现代汉服、红灯笼与全息锦鲤，东方夜市未来感。注意：画面文字可能出现伪汉字，正式出图建议 --no text 或后期修字。
- **镜头语言**：竖屏街景 / 霓虹打光 / 中近景
- **提示词模板**：{subject} under glowing neon signs, cyberpunk Chinese street, modern hanfu, red lanterns and holographic koi fish, guochao style, cinematic atmosphere
- **风格补充**：cyberpunk, guochao, neon, red lanterns, holographic koi, night street
- **创意模式**：平衡
- **推荐版本**：v8.2
- **推荐参数**：stylize=300, chaos=0, aspectRatio=9:16, referenceStrategy=prompt

### 16. 紫禁初雪 (`imperial-snow`)

- **类别**：东方美学
- **校准**：生产校准
- **视觉机制**：故宫雪景。红墙金瓦覆雪、护城河倒影、一点红伞人影，静谧冬日晨光。
- **镜头语言**：大远景对称 / 晨雾柔光 / 冷调暖点
- **提示词模板**：{subject} covered in fresh snow at dawn, red walls and golden glazed roofs, a lone figure with a red umbrella, serene winter atmosphere, cinematic photography
- **风格补充**：snow, red walls, golden roofs, serene, winter dawn, Forbidden City
- **创意模式**：平衡
- **推荐版本**：v8.2
- **推荐参数**：stylize=250, chaos=0, aspectRatio=16:9, referenceStrategy=prompt

### 17. 中国剪纸 (`paper-cut`)

- **类别**：东方美学
- **校准**：生产校准
- **视觉机制**：平面剪纸。单色红镂空剪影、蕾丝级细纹、白底，民间工艺的对称与吉祥题材。
- **镜头语言**：正面平铺 / 对称构图 / 无透视
- **提示词模板**：flat 2D traditional Chinese paper-cut art depicting {subject}, single-color red hollow-out silhouette, delicate lace-like cutout patterns on plain white background, folk paper cutting, symmetrical
- **风格补充**：paper-cut, red silhouette, hollow-out, folk art, flat 2D
- **排除项**：3D, shadow, gradient, realistic, paper sculpture, depth
- **创意模式**：平衡
- **推荐版本**：v8.2
- **推荐参数**：stylize=300, chaos=0, aspectRatio=1:1, referenceStrategy=prompt

### 18. 苏绣 (`su-embroidery`)

- **类别**：东方美学
- **校准**：生产校准
- **视觉机制**：苏绣工艺。丝线光泽、针脚走向清晰、素缎绣地，翠鸟荷花等雅致题材。
- **镜头语言**：微距特写 / 柔光 / 绸缎肌理
- **提示词模板**：{subject}, Suzhou embroidery art, silk threads with subtle sheen, intricate stitching texture, elegant Chinese textile art, macro detail
- **风格补充**：embroidery, silk threads, stitching texture, textile art, macro
- **创意模式**：平衡
- **推荐版本**：v8.2
- **推荐参数**：stylize=300, chaos=0, aspectRatio=1:1, referenceStrategy=prompt

### 19. 青花瓷 (`porcelain`)

- **类别**：东方美学
- **校准**：生产校准
- **视觉机制**：青花瓷。钴蓝缠枝龙纹、白瓷釉面、明代器型，博物馆级静物布光。低 stylize 保器型准确。
- **镜头语言**：静物正中构图 / 影棚柔光 / 灰底
- **提示词模板**：{subject}, blue and white porcelain, Ming dynasty qinghua style, cobalt blue patterns on white ceramic, soft studio lighting, elegant still life photography
- **风格补充**：blue and white porcelain, cobalt blue, qinghua, ceramic, still life
- **创意模式**：平衡
- **推荐版本**：v8.2
- **推荐参数**：stylize=150, chaos=0, aspectRatio=2:3, referenceStrategy=prompt

### 20. 太空歌剧 (`space-opera`)

- **类别**：电影叙事
- **校准**：生产校准
- **视觉机制**：太空史诗。巨舰、带环气态巨行星、宇航员剪影的尺度对比，星云光，21:9 宽画幅。
- **镜头语言**：21:9 超宽 / 巨物尺度对比 / 剪影
- **提示词模板**：{subject} drifting past a ringed gas giant, a tiny astronaut floating in the foreground, nebula light, epic space opera, cinematic wide shot
- **风格补充**：space opera, gas giant, nebula, epic scale, starship
- **创意模式**：平衡
- **推荐版本**：v8.2
- **推荐参数**：stylize=300, chaos=0, aspectRatio=21:9, referenceStrategy=prompt

### 21. 末日废土 (`post-apocalypse`)

- **类别**：电影叙事
- **校准**：生产校准
- **视觉机制**：末日重生。藤蔓吞没的摩天楼、旅人与狗、远处鹿群、晨雾，静谧而非血腥的废土。
- **镜头语言**：广角纵深 / 晨雾柔光 / 人与自然尺度对比
- **提示词模板**：{subject} walking through an overgrown abandoned city street, nature reclaiming skyscrapers, deer grazing in the distance, morning mist, cinematic film still
- **风格补充**：post-apocalyptic, overgrown ruins, nature reclaiming, morning mist
- **创意模式**：平衡
- **推荐版本**：v8.2
- **推荐参数**：stylize=250, chaos=0, aspectRatio=16:9, referenceStrategy=prompt

### 22. 黑色电影 (`noir`)

- **类别**：电影叙事
- **校准**：生产校准
- **视觉机制**：40 年代黑色电影。纯黑白、雨夜路灯、百叶窗条纹阴影、香烟烟雾，极端明暗对比。
- **镜头语言**：低调照明 / 高反差 / 阴影切割构图
- **提示词模板**：{subject} under a street lamp in the rain, venetian blind shadows, swirling cigarette smoke, black and white film noir, extreme contrast, 1940s atmosphere
- **风格补充**：film noir, black and white, venetian blind shadows, high contrast, rain
- **创意模式**：平衡
- **推荐版本**：v8.2
- **推荐参数**：stylize=250, chaos=0, aspectRatio=2:3, referenceStrategy=prompt

### 23. 粉彩对称叙事 (`pastel-symmetry`)

- **类别**：电影叙事
- **校准**：生产校准
- **视觉机制**：粉彩对称叙事。粉彩配色、完美对称、正面平拍、复古道具细节，童话般的秩序感。
- **镜头语言**：严格居中对称 / 正面平拍 / 粉彩
- **提示词模板**：{subject}, perfectly centered symmetrical composition, flat frontal view, pastel color palette, whimsical, retro details, pastel symmetrical storybook direction
- **风格补充**：symmetrical, pastel, flat frontal, whimsical, pastel symmetrical storybook direction
- **创意模式**：平衡
- **推荐版本**：v8.2
- **推荐参数**：stylize=300, chaos=0, aspectRatio=16:9, referenceStrategy=prompt
- **兼容别名**：wes-anderson

### 24. 深海幻境 (`underwater`)

- **类别**：电影叙事
- **校准**：生产校准
- **视觉机制**：水下梦境。白裙少女悬浮、发光水母群、穿透深蓝的光束、上升气泡，ethereal 空灵。
- **镜头语言**：竖屏全身 / 顶光光束 / 深蓝调
- **提示词模板**：{subject} floating underwater among glowing jellyfish, sun rays piercing the deep blue water, rising bubbles, ethereal dreamlike, cinematic
- **风格补充**：underwater, glowing jellyfish, light rays, bubbles, ethereal
- **创意模式**：平衡
- **推荐版本**：v8.2
- **推荐参数**：stylize=300, chaos=0, aspectRatio=9:16, referenceStrategy=prompt

### 25. 时尚大片 (`fashion-editorial`)

- **类别**：真实摄影
- **校准**：生产校准
- **视觉机制**：高级时尚 editorial。雕塑感礼服、极简混凝土空间、戏剧性光影切割，高级时尚杂志构图。
- **镜头语言**：全身/七分身 / 硬光阴影 / 负空间
- **提示词模板**：{subject} in an avant-garde sculptural gown posing in a minimalist concrete space, dramatic shadow play, high fashion editorial, high-fashion magazine photography
- **风格补充**：fashion editorial, avant-garde, sculptural gown, dramatic shadows, high-fashion magazine
- **创意模式**：平衡
- **推荐版本**：v8.2
- **推荐参数**：stylize=250, chaos=0, aspectRatio=2:3, referenceStrategy=prompt

### 26. 黄金时刻 (`golden-portrait`)

- **类别**：真实摄影
- **校准**：生产校准
- **视觉机制**：黄金时刻人文人像。暖金窗光、劳作的手、岁月肌理，photojournalism 真实感。必须 raw。
- **镜头语言**：近景 / 浅景深 / 侧逆暖光
- **提示词模板**：portrait of {subject}, golden hour window light, warm tones, shallow depth of field, photojournalism, weathered hands and textures
- **风格补充**：golden hour, warm tones, shallow depth of field, photojournalism
- **创意模式**：忠实
- **推荐版本**：v8.2
- **推荐参数**：stylize=150, chaos=0, raw=true, aspectRatio=4:5, referenceStrategy=prompt

### 27. 美食微距 (`food-macro`)

- **类别**：商业设计
- **校准**：生产校准
- **视觉机制**：米其林美食摄影。微距质感、暗调背景、冷雾/蒸汽、油润光泽。低 stylize 保食材真实。
- **镜头语言**：微距特写 / 暗调 / 侧光
- **提示词模板**：{subject}, macro food photography, dark moody background, glistening texture, wisps of mist, michelin star plating
- **风格补充**：macro food photography, dark background, glistening, michelin plating
- **创意模式**：平衡
- **推荐版本**：v8.2
- **推荐参数**：stylize=100, chaos=0, aspectRatio=1:1, referenceStrategy=prompt

### 28. 建筑光影 (`architecture-light`)

- **类别**：真实摄影
- **校准**：生产校准
- **视觉机制**：建筑摄影。清水混凝土、几何构成、一束光切割空间，锐利明暗。
- **镜头语言**：仰拍/俯拍几何 / 光束 / 极简
- **提示词模板**：{subject}, a beam of sunlight cutting through the space, geometric shadows, minimalist concrete architecture, architectural photography
- **风格补充**：architecture, concrete, light beam, geometric shadows, minimalist
- **创意模式**：平衡
- **推荐版本**：v8.2
- **推荐参数**：stylize=200, chaos=0, aspectRatio=2:3, referenceStrategy=prompt

### 29. 手绘田园动画 (`hand-painted-pastoral`)

- **类别**：插画动画
- **校准**：生产校准
- **视觉机制**：手绘田园动画背景。夏日积雨云、绿草坡、乡村与毛茸茸精灵，赛璐璐上色。niji7 通道。
- **镜头语言**：广角风景 / 人物点景 / 手绘质感
- **提示词模板**：{subject} on a grassy hill overlooking a rural village, towering summer clouds, lush greenery, hand-painted pastoral animation, hand-painted animation background
- **风格补充**：hand-painted pastoral animation, hand-painted, summer clouds, lush greenery, anime background
- **创意模式**：平衡
- **推荐版本**：niji7
- **推荐参数**：stylize=200, chaos=0, aspectRatio=16:9, referenceStrategy=prompt
- **兼容别名**：ghibli

### 30. 国潮插画 (`guochao-illustration`)

- **类别**：东方美学
- **校准**：生产校准
- **视觉机制**：国潮装饰插画。仙鹤、描金云纹、青山金浪，矿物色 + 金线，现代中式海报。
- **镜头语言**：平面装饰 / 描金线 / 横构图
- **提示词模板**：{subject}, Chinese guochao flat vector illustration, bold gold outline work, decorative swirling clouds, rich mineral color palette, modern Chinese decorative poster art
- **风格补充**：guochao, flat illustration, gold outlines, decorative clouds, mineral colors
- **排除项**：realistic, photography, japanese, mount fuji, ukiyo-e
- **创意模式**：平衡
- **推荐版本**：v8.2
- **推荐参数**：stylize=300, chaos=0, aspectRatio=16:9, referenceStrategy=prompt

### 31. 浮世绘 (`ukiyo-e`)

- **类别**：插画动画
- **校准**：生产校准
- **视觉机制**：浮世绘木版画。巨浪、富士山、粗轮廓线与平涂色块，葛饰北斋风。落款文字可能为伪字，可 --no text。
- **镜头语言**：平面构图 / 粗轮廓 / 平涂
- **提示词模板**：{subject}, Japanese ukiyo-e woodblock print, Hokusai style, bold outlines and flat color areas
- **风格补充**：ukiyo-e, woodblock print, Hokusai style, bold outlines, flat colors
- **创意模式**：平衡
- **推荐版本**：v8.2
- **推荐参数**：stylize=300, chaos=0, aspectRatio=3:2, referenceStrategy=prompt

### 32. 像素艺术 (`pixel-art`)

- **类别**：插画动画
- **校准**：生产校准
- **视觉机制**：16-bit 像素。有限调色板 + 抖动、雨夜小店暖窗，复古游戏画面感。
- **镜头语言**：横版场景 / 像素颗粒 / 有限调色板
- **提示词模板**：{subject}, pixel art, 16-bit retro game style, warm glowing windows, detailed pixel sprites
- **风格补充**：pixel art, 16-bit, retro game, limited palette, dithering
- **创意模式**：平衡
- **推荐版本**：v8.2
- **推荐参数**：stylize=200, chaos=0, aspectRatio=16:9, referenceStrategy=prompt

### 33. 水彩童话 (`watercolor`)

- **类别**：插画动画
- **校准**：生产校准
- **视觉机制**：水彩绘本。柔和晕染、蘑菇与狐狸的童话叙事，温暖故事书质感。
- **镜头语言**：中景叙事 / 柔和晕染 / 暖色
- **提示词模板**：whimsical watercolor storybook illustration of {subject}, translucent pigment blooms, soft color washes, visible paper texture
- **风格补充**：watercolor, soft washes, whimsical, storybook illustration
- **创意模式**：平衡
- **推荐版本**：v8.2
- **推荐参数**：stylize=300, chaos=0, aspectRatio=2:3, referenceStrategy=prompt

### 34. 双重曝光 (`double-exposure`)

- **类别**：实验创意
- **校准**：生产校准
- **视觉机制**：双重曝光艺术。人物轮廓与森林/飞鸟融合，虚实交叠，fine art 摄影。
- **镜头语言**：肖像轮廓 / 融合叠加 / 高调背景
- **提示词模板**：double exposure portrait of {subject} merged with a misty pine forest and flying birds, silhouette blend, ethereal, fine art photography
- **风格补充**：double exposure, silhouette blend, ethereal, fine art
- **创意模式**：忠实
- **推荐版本**：v8.2
- **推荐参数**：stylize=250, chaos=0, raw=true, aspectRatio=2:3, referenceStrategy=prompt

### 35. 微缩世界 (`miniature`)

- **类别**：实验创意
- **校准**：生产校准
- **视觉机制**：移轴微缩。桌面小人国、夜市灯笼、浅景深 diorama 效果，玩具感。
- **镜头语言**：移轴俯拍 / 极浅景深 / 暖光斑
- **提示词模板**：a miniature diorama of {subject}, tilt-shift photography, tiny glowing lanterns, shallow depth of field, warm bokeh
- **风格补充**：miniature, tilt-shift, diorama, shallow depth of field, bokeh
- **创意模式**：平衡
- **推荐版本**：v8.2
- **推荐参数**：stylize=250, chaos=0, aspectRatio=16:9, referenceStrategy=prompt

### 36. 黏土动画 (`claymation`)

- **类别**：插画动画
- **校准**：生产校准
- **视觉机制**：黏土定格动画。手工黏土颗粒、哑光质感、可爱角色，手工定格幽默。
- **镜头语言**：中景 / 影棚柔光 / 手工质感
- **提示词模板**：handcrafted claymation stop-motion scene of {subject}, visible clay fingerprints, matte miniature set, soft studio lighting, playful physical performance
- **风格补充**：claymation, stop motion, clay texture, handmade, playful handcrafted stop-motion
- **创意模式**：平衡
- **推荐版本**：v8.2
- **推荐参数**：stylize=250, chaos=0, aspectRatio=16:9, referenceStrategy=prompt

### 37. 唐风仕女 (`tang-beauty`)

- **类别**：东方美学
- **校准**：生产校准
- **视觉机制**：盛唐仕女。高髻花钿、丝绸襦裙、团扇、朱砂金配色，丰腴华贵的唐人审美。
- **镜头语言**：半身肖像 / 暖调 / 华贵细节
- **提示词模板**：{subject}, Tang dynasty court style, elaborate high bun and floral forehead ornament, flowing silk ruqun, rich vermilion and gold palette, classical Chinese aesthetics, cinematic portrait
- **风格补充**：Tang dynasty, silk ruqun, vermilion and gold, floral ornament, classical Chinese
- **创意模式**：平衡
- **推荐版本**：v8.2
- **推荐参数**：stylize=300, chaos=0, aspectRatio=9:16, referenceStrategy=prompt

### 38. 宋代极简 (`song-minimal`)

- **类别**：东方美学
- **校准**：生产校准
- **视觉机制**：宋代美学。青瓷、梅枝、大量留白、雅致低饱和，简至极处即是美。
- **镜头语言**：静物一隅 / 大面积留白 / 柔光
- **提示词模板**：{subject}, Song dynasty minimalist aesthetics, celadon and plum blossom, muted elegant tones, vast negative space, refined simplicity, oriental zen
- **风格补充**：Song dynasty, minimalist, celadon, negative space, zen
- **创意模式**：平衡
- **推荐版本**：v8.2
- **推荐参数**：stylize=350, chaos=0, aspectRatio=3:2, referenceStrategy=prompt

### 39. 皮影戏 (`shadow-puppet`)

- **类别**：东方美学
- **校准**：生产校准
- **视觉机制**：中国皮影。半透明染色皮革镂空人偶、白色幕布暖背光、关节杆控，民间戏台。
- **镜头语言**：侧面平拍 / 幕布背光 / 剪影
- **提示词模板**：{subject}, traditional Chinese shadow puppetry, flat 2D articulated leather puppets with intricate cut-out patterns, silhouettes projected onto a glowing white linen screen, warm amber backlight shining through translucent dyed leather, folk art
- **风格补充**：shadow puppetry, translucent leather, cut-out patterns, linen screen, backlight
- **排除项**：3d render, cinematic, dark background, smoke, battlefield, photorealistic
- **创意模式**：平衡
- **推荐版本**：v8.2
- **推荐参数**：stylize=300, chaos=0, aspectRatio=16:9, referenceStrategy=prompt

### 40. 景泰蓝 (`cloisonne`)

- **类别**：东方美学
- **校准**：生产校准
- **视觉机制**：景泰蓝工艺。铜胎掐丝珐琅、宝蓝釉地配金线、缠枝莲纹，宫廷奢华。
- **镜头语言**：静物微距 / 釉面光泽 / 暗底
- **提示词模板**：{subject}, cloisonne enamel, imperial blue and gold, copper wire inlay, intricate lotus scroll patterns, luxurious Chinese craftsmanship, macro detail, museum photography
- **风格补充**：cloisonne, enamel, imperial blue and gold, copper inlay, museum
- **创意模式**：平衡
- **推荐版本**：v8.2
- **推荐参数**：stylize=250, chaos=0, aspectRatio=1:1, referenceStrategy=prompt

### 41. 玉雕 (`jade-carving`)

- **类别**：东方美学
- **校准**：生产校准
- **视觉机制**：和田玉雕。半透明玉质、镂空雕龙、内敛莹光，博物馆静物。
- **镜头语言**：静物特写 / 暗背景衬光 / 透光
- **提示词模板**：{subject}, translucent white jade carving, Hetian jade, soft inner glow, intricate openwork carving, elegant museum still life, dark background
- **风格补充**：jade carving, translucent, Hetian jade, openwork, museum still life
- **创意模式**：平衡
- **推荐版本**：v8.2
- **推荐参数**：stylize=200, chaos=0, aspectRatio=1:1, referenceStrategy=prompt

### 42. 水墨武侠 (`ink-wuxia`)

- **类别**：东方美学
- **校准**：生产校准
- **视觉机制**：泼墨武侠。飞白笔触、竹林对决、红色印章点缀，黑白张力中的动感爆发。
- **镜头语言**：动态瞬间 / 泼墨飞白 / 留白
- **提示词模板**：{subject}, expressive Chinese ink splash painting, dynamic black brushstrokes with red accent seals, dramatic motion, wuxia ink art
- **风格补充**：ink splash, brushstrokes, wuxia, red seal, dynamic
- **创意模式**：平衡
- **推荐版本**：v8.2
- **推荐参数**：stylize=400, chaos=0, aspectRatio=16:9, referenceStrategy=prompt

### 43. 唐宫夜宴 (`tang-banquet`)

- **类别**：东方美学
- **校准**：生产校准
- **视觉机制**：盛唐夜宴。水袖舞者、烛火金器、朱红大殿，富丽堂皇的宫廷气象。
- **镜头语言**：广角群像 / 烛光暖调 / 纵深
- **提示词模板**：{subject}, grand Tang dynasty palace night banquet, dancers in flowing silk, candles and golden vessels, rich vermilion hall, cinematic wide shot, opulent atmosphere
- **风格补充**：Tang dynasty, palace banquet, dancers, candlelight, vermilion, opulent
- **创意模式**：平衡
- **推荐版本**：v8.2
- **推荐参数**：stylize=300, chaos=0, aspectRatio=16:9, referenceStrategy=prompt

### 44. 禅意茶室 (`zen-tea`)

- **类别**：东方美学
- **校准**：生产校准
- **视觉机制**：侘寂茶室。粗陶壶、蒸汽、竹影映窗，晨光中的静寂。
- **镜头语言**：静物近景 / 柔光 / 低饱和
- **提示词模板**：{subject}, rustic tea room, clay teapot with steam rising, bamboo shadows on shoji screen, wabi-sabi zen atmosphere, soft morning light, tranquil still life
- **风格补充**：zen, tea room, wabi-sabi, bamboo shadows, morning light
- **创意模式**：平衡
- **推荐版本**：v8.2
- **推荐参数**：stylize=250, chaos=0, aspectRatio=3:2, referenceStrategy=prompt

### 45. 西部荒野 (`western`)

- **类别**：电影叙事
- **校准**：生产校准
- **视觉机制**：西部片。纪念碑谷台地、骑马牛仔剪影、巨大橙色落日、尘土，变形宽银幕。
- **镜头语言**：21:9 超宽 / 大远景剪影 / 暖橙
- **提示词模板**：{subject} silhouetted against a massive orange sunset, Monument Valley mesas, dust in the air, epic western film still, anamorphic widescreen
- **风格补充**：western, Monument Valley, cowboy silhouette, sunset, anamorphic
- **创意模式**：平衡
- **推荐版本**：v8.2
- **推荐参数**：stylize=250, chaos=0, aspectRatio=21:9, referenceStrategy=prompt

### 46. 史诗战争 (`war-epic`)

- **类别**：电影叙事
- **校准**：生产校准
- **视觉机制**：古代史诗战争。千军万马、战旗箭雨、黎明烽火，宏大场面调度。
- **镜头语言**：21:9 超宽全景 / 俯拍 / 烟尘
- **提示词模板**：{subject} on a vast battlefield at dawn, thousands of ancient soldiers, war banners and arrows in the sky, dust and fire, epic historical war film, cinematic wide shot
- **风格补充**：epic war, battlefield, banners, arrows, dawn, cinematic
- **创意模式**：平衡
- **推荐版本**：v8.2
- **推荐参数**：stylize=300, chaos=0, aspectRatio=21:9, referenceStrategy=prompt

### 47. 蒸汽朋克 (`steampunk`)

- **类别**：电影叙事
- **校准**：生产校准
- **视觉机制**：蒸汽朋克工坊。黄铜齿轮、蒸汽管道、护目镜皮围裙发明家，爱迪生灯泡暖光。
- **镜头语言**：中景环境人像 / 暖光 / 繁复机械细节
- **提示词模板**：{subject} in a cluttered workshop full of brass gears and steam pipes, goggles and leather apron, warm Edison bulb light, intricate mechanical details, steampunk
- **风格补充**：steampunk, brass gears, steam pipes, Edison bulbs, workshop
- **创意模式**：平衡
- **推荐版本**：v8.2
- **推荐参数**：stylize=300, chaos=0, aspectRatio=2:3, referenceStrategy=prompt

### 48. 极光秘境 (`aurora`)

- **类别**：真实摄影
- **校准**：生产校准
- **视觉机制**：极地极光。绿紫光帘、雪松林、孤独小屋暖窗、星空长曝。
- **镜头语言**：广角夜景 / 长曝 / 冷暖对比
- **提示词模板**：{subject} under a spectacular green and purple aurora borealis, snow-covered pine forest, starry sky, long exposure night photography, serene arctic wilderness
- **风格补充**：aurora borealis, starry sky, snow, long exposure, night
- **创意模式**：平衡
- **推荐版本**：v8.2
- **推荐参数**：stylize=250, chaos=0, aspectRatio=16:9, referenceStrategy=prompt

### 49. 水晶洞穴 (`crystal-cave`)

- **类别**：电影叙事
- **校准**：生产校准
- **视觉机制**：水晶巨洞。紫水晶簇折射光、探险者火把、神秘纵深，奇幻史诗。
- **镜头语言**：广角纵深 / 点光源对比 / 巨物尺度
- **提示词模板**：{subject} entering a colossal cave of giant glowing amethyst crystals, light refracting through crystal facets, mystical atmosphere, epic scale
- **风格补充**：crystal cave, amethyst, light refraction, glowing, epic scale
- **创意模式**：平衡
- **推荐版本**：v8.2
- **推荐参数**：stylize=350, chaos=0, aspectRatio=16:9, referenceStrategy=prompt

### 50. 夜景人像 (`night-portrait`)

- **类别**：真实摄影
- **校准**：生产校准
- **视觉机制**：夜景霓虹人像。85mm 浅景深、霓虹招牌光斑、面部锐利，都市氛围。必须 raw。
- **镜头语言**：85mm 特写 / 大光圈光斑 / 霓虹补光
- **提示词模板**：portrait of {subject} lit by neon shop signs at night, bokeh city lights background, cinematic night photography, 85mm lens, shallow depth of field
- **风格补充**：night portrait, neon, bokeh, 85mm, cinematic
- **创意模式**：忠实
- **推荐版本**：v8.2
- **推荐参数**：stylize=200, chaos=0, raw=true, aspectRatio=2:3, referenceStrategy=prompt

### 51. 运动瞬间 (`sports-action`)

- **类别**：真实摄影
- **校准**：生产校准
- **视觉机制**：高速运动摄影。起跑爆发、颗粒飞溅、凝固瞬间，体育场戏剧性灯光。必须 raw。
- **镜头语言**：低角度 / 高速快门 / 动感颗粒
- **提示词模板**：{subject}, frozen motion with flying particles, dramatic stadium lighting, professional sports photography, high shutter speed
- **风格补充**：sports photography, frozen motion, stadium lighting, high shutter speed
- **创意模式**：忠实
- **推荐版本**：v8.2
- **推荐参数**：stylize=150, chaos=0, raw=true, aspectRatio=16:9, referenceStrategy=prompt

### 52. 野生动物 (`wildlife`)

- **类别**：真实摄影
- **校准**：生产校准
- **视觉机制**：野生动物摄影。雪豹岩壁黄昏、长焦压缩、金色轮廓光，国家地理级。必须 raw。
- **镜头语言**：长焦特写 / 轮廓光 / 浅景深
- **提示词模板**：{subject}, telephoto wildlife photography, natural-history editorial, golden rim light, shallow depth of field
- **风格补充**：wildlife, telephoto, natural-history editorial, rim light
- **创意模式**：忠实
- **推荐版本**：v8.2
- **推荐参数**：stylize=150, chaos=0, raw=true, aspectRatio=3:2, referenceStrategy=prompt

### 53. 航拍大地 (`aerial-land`)

- **类别**：真实摄影
- **校准**：生产校准
- **视觉机制**：航拍风光。梯田曲线、晨雾流动、日出金光、人兽点景，无人机视角。
- **镜头语言**：俯视航拍 / 曲线构成 / 晨雾
- **提示词模板**：aerial view of {subject} at sunrise, mist flowing between the curves, drone photography, layered green and gold
- **风格补充**：aerial, drone photography, sunrise, mist, terraced fields
- **创意模式**：平衡
- **推荐版本**：v8.2
- **推荐参数**：stylize=250, chaos=0, aspectRatio=16:9, referenceStrategy=prompt

### 54. 古典花卉 (`still-flower`)

- **类别**：插画动画
- **校准**：生产校准
- **视觉机制**：荷兰黄金时代静物油画。暗背景花卉、花瓣水珠、戏剧性侧光、油画肌理。
- **镜头语言**：静物正中 / 暗背景 / 侧光
- **提示词模板**：{subject}, dark moody still life, Dutch Golden Age painting style, water droplets on petals, dramatic side light, oil painting texture
- **风格补充**：floral still life, Dutch Golden Age, dark background, oil painting
- **创意模式**：平衡
- **推荐版本**：v8.2
- **推荐参数**：stylize=250, chaos=0, aspectRatio=2:3, referenceStrategy=prompt

### 55. 扁平矢量 (`flat-vector`)

- **类别**：插画动画
- **校准**：生产校准
- **视觉机制**：扁平矢量插画。大胆几何色块、暖渐变、极简线条，几何编辑插画优雅。媒介词必须置首。
- **镜头语言**：平面构成 / 色块渐变 / 无阴影
- **提示词模板**：flat vector illustration of {subject}, 2D flat design, bold geometric shapes, flat color blocks with warm gradient palette, minimalist clean lines, no shading, vector art, with bold geometric editorial elegance
- **风格补充**：flat vector, geometric shapes, gradient, minimalist, bold geometric editorial style
- **排除项**：photorealistic, 3d render, cinematic lighting, realistic texture, photograph
- **创意模式**：平衡
- **推荐版本**：v8.2
- **推荐参数**：stylize=250, chaos=0, aspectRatio=16:9, referenceStrategy=prompt

### 56. 儿童绘本 (`children-book`)

- **类别**：插画动画
- **校准**：生产校准
- **视觉机制**：儿童绘本。水粉厚涂、可爱动物角色、温暖叙事场景，柔和治愈。
- **镜头语言**：中景叙事 / 水粉肌理 / 暖色
- **提示词模板**：hand-painted children book gouache illustration of {subject}, warm simple shapes, tactile paper, gentle storybook staging
- **风格补充**：children book, gouache, whimsical, warm, storybook
- **创意模式**：平衡
- **推荐版本**：v8.2
- **推荐参数**：stylize=300, chaos=0, aspectRatio=4:3, referenceStrategy=prompt

### 57. 极简线稿 (`line-art`)

- **类别**：插画动画
- **校准**：生产校准
- **视觉机制**：单线艺术。一笔连绵构成人物与花，米色纸黑线，tattoo 设计感。
- **镜头语言**：居中平面 / 单线 / 留白
- **提示词模板**：minimal single-line ink illustration of {subject}, clean negative space, elegant continuous contour, white paper
- **风格补充**：single line, line art, minimalist, black on cream, tattoo design
- **创意模式**：平衡
- **推荐版本**：v8.2
- **推荐参数**：stylize=200, chaos=0, aspectRatio=1:1, referenceStrategy=prompt

### 58. 暗黑幻想 (`dark-fantasy-art`)

- **类别**：插画动画
- **校准**：生产校准
- **视觉机制**：暗黑幻想油画。血月、巨龙、哥特残塔、厚涂肌理，超现实暗黑不祥氛围。
- **镜头语言**：仰视巨物 / 厚涂 / 暗调红光
- **提示词模板**：{subject}, dark fantasy oil painting, blood moon, rich impasto texture, ominous atmosphere, crumbling gothic architecture, haunting surreal dark-fantasy tradition
- **风格补充**：dark fantasy, oil painting, blood moon, impasto, ominous
- **创意模式**：平衡
- **推荐版本**：v8.2
- **推荐参数**：stylize=400, chaos=0, aspectRatio=2:3, referenceStrategy=prompt

### 59. 故障艺术 (`glitch`)

- **类别**：实验创意
- **校准**：生产校准
- **视觉机制**：故障艺术。古典雕像 RGB 碎片化、扫描线、数字伪影，蒸汽波配色。
- **镜头语言**：中景 / 数字失真 / 粉青撞色
- **提示词模板**：{subject} fragmenting into RGB glitch distortion, digital artifacts and scan lines, vaporwave aesthetic, glitch art
- **风格补充**：glitch art, RGB distortion, scan lines, vaporwave, digital artifacts
- **创意模式**：平衡
- **推荐版本**：v8.2
- **推荐参数**：stylize=300, chaos=0, aspectRatio=16:9, referenceStrategy=prompt

### 60. 平铺摄影 (`knolling`)

- **类别**：商业设计
- **校准**：生产校准
- **视觉机制**：平铺收纳摄影。物件直角网格排列、俯拍、均匀间距，治愈强迫症。低 stylize 保物件真实。
- **镜头语言**：正俯视 / 网格排列 / 均光
- **提示词模板**：{subject} neatly arranged in a flat lay grid, knolling photography, top-down view, every object at right angles, warm natural light
- **风格补充**：knolling, flat lay, top-down, grid arrangement, organized
- **创意模式**：平衡
- **推荐版本**：v8.2
- **推荐参数**：stylize=100, chaos=0, aspectRatio=1:1, referenceStrategy=prompt

### 61. 生猛闪光人像 (`raw-flash-intimacy`)

- **类别**：真实摄影
- **校准**：导演校准
- **视觉机制**：近距离直闪、真实皮肤、汗光与碎发；保留毛孔和轻微瑕疵，拒绝塑料磨皮。
- **镜头语言**：85mm close portrait, shallow depth of field, slight foreground occlusion, direct on-camera flash
- **提示词模板**：raw direct-flash editorial portrait, truthful skin texture, damp flyaway hair, imperfect human detail, immediate eye contact, restrained color
- **风格补充**：raw direct-flash editorial portrait, truthful skin texture, damp flyaway hair, imperfect human detail, immediate eye contact, restrained color
- **创意模式**：忠实
- **推荐版本**：v8.2
- **推荐参数**：stylize=140, chaos=4, raw=true, referenceStrategy=prompt

### 62. 动态时装抓拍 (`kinetic-fashion-frame`)

- **类别**：真实摄影
- **校准**：导演校准
- **视觉机制**：让衣料、头发和肢体形成动势，奢华但不摆拍。
- **镜头语言**：handheld medium close shot, oblique framing, shutter drag on secondary movement
- **提示词模板**：kinetic fashion editorial, fabric caught mid-motion, candid asymmetry, selective motion blur, tactile styling, spontaneous luxury
- **风格补充**：kinetic fashion editorial, fabric caught mid-motion, candid asymmetry, selective motion blur, tactile styling, spontaneous luxury
- **创意模式**：平衡
- **推荐版本**：v8.2
- **推荐参数**：stylize=260, chaos=10, referenceStrategy=prompt

### 63. 东方珠玉盛装 (`ceremonial-jewelry`)

- **类别**：真实摄影
- **校准**：导演校准
- **视觉机制**：珠玉、金属丝、漆黑与深红组成高密度层次，人物五官仍是视觉中心。
- **镜头语言**：compressed telephoto portrait, narrow focus plane, warm practical highlights in deep shadow
- **提示词模板**：ceremonial East Asian couture portrait, dense handcrafted metal filigree, pearls and gemstone details, lacquer-black depth, red textile accents, museum-grade material realism
- **风格补充**：ceremonial East Asian couture portrait, dense handcrafted metal filigree, pearls and gemstone details, lacquer-black depth, red textile accents, museum-grade material realism
- **创意模式**：平衡
- **推荐版本**：v8.2
- **推荐参数**：stylize=260, chaos=4, referenceStrategy=style-reference

### 64. 暗夜猩红铠甲 (`nocturnal-crimson-armor`)

- **类别**：真实摄影
- **校准**：导演校准
- **视觉机制**：大面积黑中保留盔甲轮廓，红光只作结构锚点，材质必须可触摸。
- **镜头语言**：low-angle full figure, centered but not symmetrical, long-lens background compression
- **提示词模板**：nocturnal black armor portrait, wet reflective metal, sparse crimson edge light, drifting ground fog, severe silhouette, tactile battle wear
- **风格补充**：nocturnal black armor portrait, wet reflective metal, sparse crimson edge light, drifting ground fog, severe silhouette, tactile battle wear
- **创意模式**：平衡
- **推荐版本**：v8.2
- **推荐参数**：stylize=280, chaos=6, referenceStrategy=prompt

### 65. 废墟机甲考古 (`ruined-mecha-archaeology`)

- **类别**：电影叙事
- **校准**：导演校准
- **视觉机制**：把巨型机械当作真实遗址拍摄，重点是尺度、重量、剥落漆面与城市残骸。
- **镜头语言**：extreme low-angle 28mm lens, foreground rubble, hard daylight, occasional tilted frame
- **提示词模板**：monumental weathered mecha discovered in a collapsed concrete megastructure, chipped painted armor, exposed cables, dust and mineral deposits, documentary realism
- **风格补充**：monumental weathered mecha discovered in a collapsed concrete megastructure, chipped painted armor, exposed cables, dust and mineral deposits, documentary realism
- **创意模式**：忠实
- **推荐版本**：v8.2
- **推荐参数**：stylize=260, chaos=8, raw=true, referenceStrategy=prompt

### 66. 史诗留白远景 (`epic-negative-space`)

- **类别**：电影叙事
- **校准**：导演校准
- **视觉机制**：用极小人物和巨大环境建立尺度，构图克制，只有一个清晰叙事目标。
- **镜头语言**：ultra-wide establishing shot, low horizon or high horizon chosen for scale, restrained atmospheric perspective
- **提示词模板**：vast cinematic landscape with tiny human silhouettes, monumental negative space, one readable destination, wind-carved terrain, quiet narrative tension
- **风格补充**：vast cinematic landscape with tiny human silhouettes, monumental negative space, one readable destination, wind-carved terrain, quiet narrative tension
- **创意模式**：平衡
- **推荐版本**：v8.2
- **推荐参数**：stylize=240, chaos=7, referenceStrategy=prompt

### 67. 仪式性群像 (`ritual-procession`)

- **类别**：电影叙事
- **校准**：导演校准
- **视觉机制**：群像不是堆人，而是用队列、间距、姿态和光线组织权力关系。
- **镜头语言**：symmetrical wide shot broken by one moving subject, deep staging, hard cut visual clarity
- **提示词模板**：ritual procession in a monumental space, readable group hierarchy, repeated silhouettes, restrained theatrical blocking, smoke and directional light
- **风格补充**：ritual procession in a monumental space, readable group hierarchy, repeated silhouettes, restrained theatrical blocking, smoke and directional light
- **创意模式**：平衡
- **推荐版本**：v8.2
- **推荐参数**：stylize=260, chaos=8, referenceStrategy=prompt

### 68. 都市神话惊悚 (`urban-myth-thriller`)

- **类别**：电影叙事
- **校准**：导演校准
- **视觉机制**：现实城市保持可信，仅让一个神话元素侵入，避免满屏奇观。
- **镜头语言**：35mm street-level frame, hidden observer angle, practical lighting, deep shadow pockets
- **提示词模板**：contemporary urban location interrupted by an ancient mythic presence, believable street detail, sodium-vapor and fluorescent light, uneasy realism
- **风格补充**：contemporary urban location interrupted by an ancient mythic presence, believable street detail, sodium-vapor and fluorescent light, uneasy realism
- **创意模式**：平衡
- **推荐版本**：v8.2
- **推荐参数**：stylize=210, chaos=9, referenceStrategy=prompt

### 69. 生态层叠未来城 (`living-terrace-city`)

- **类别**：世界构建
- **校准**：导演校准
- **视觉机制**：未来建筑与山体、水系、植被形成生态循环，奇观背后仍有可生活的尺度。
- **镜头语言**：layered aerial establishing view, strong foreground framing, atmospheric depth across three planes
- **提示词模板**：biophilic terraced city grown across a mountain valley, translucent canopies, water circulation, cultivated forests, plausible civic infrastructure, inhabited scale
- **风格补充**：biophilic terraced city grown across a mountain valley, translucent canopies, water circulation, cultivated forests, plausible civic infrastructure, inhabited scale
- **创意模式**：探索
- **推荐版本**：v8.2
- **推荐参数**：stylize=420, chaos=14, referenceStrategy=prompt

### 70. 宇宙花园拼贴 (`celestial-garden-collage`)

- **类别**：世界构建
- **校准**：导演校准
- **视觉机制**：真实风景、宇宙孔洞与植物以拼贴逻辑衔接，层次丰富但叙事焦点单一。
- **镜头语言**：vertical journey composition, nested horizons, soft impossible transitions between scales
- **提示词模板**：surreal celestial garden assembled as a seamless editorial collage, flowering valleys, reflective rivers, cosmic void apertures, one poetic animal figure
- **风格补充**：surreal celestial garden assembled as a seamless editorial collage, flowering valleys, reflective rivers, cosmic void apertures, one poetic animal figure
- **创意模式**：探索
- **推荐版本**：v8.2
- **推荐参数**：stylize=360, chaos=12, referenceStrategy=style-reference

### 71. 不可能的自然博物馆 (`impossible-museum`)

- **类别**：世界构建
- **校准**：导演校准
- **视觉机制**：博物馆、地貌和生命样本互相嵌套，具有科普秩序与梦境尺度。
- **镜头语言**：one-point perspective interrupted by organic openings, measured architectural photography
- **提示词模板**：impossible natural-history museum embedded inside a living landscape, geological halls, specimen-scale architecture, quiet visitors, scientific wonder
- **风格补充**：impossible natural-history museum embedded inside a living landscape, geological halls, specimen-scale architecture, quiet visitors, scientific wonder
- **创意模式**：探索
- **推荐版本**：v8.2
- **推荐参数**：stylize=390, chaos=16, referenceStrategy=prompt

### 72. 静默粗粝未来 (`silent-brutalist-future`)

- **类别**：世界构建
- **校准**：导演校准
- **视觉机制**：冷静、少元素、强尺度，未来感来自结构与使用痕迹而不是霓虹装饰。
- **镜头语言**：24mm architectural frame, disciplined vanishing lines, overcast diffuse light
- **提示词模板**：silent brutalist future settlement, monolithic concrete, weathered surfaces, sparse human traces, fog-softened depth, functional details
- **风格补充**：silent brutalist future settlement, monolithic concrete, weathered surfaces, sparse human traces, fog-softened depth, functional details
- **创意模式**：忠实
- **推荐版本**：v8.2
- **推荐参数**：stylize=160, chaos=4, raw=true, referenceStrategy=prompt

### 73. 神话翼甲华服 (`mythic-winged-regalia`)

- **类别**：东方美学
- **校准**：导演校准
- **视觉机制**：羽翼、甲片和古代织物形成真实可制作的服装系统，人物身份清晰。
- **镜头语言**：three-quarter hero portrait, layered foreground figures, shallow depth, warm backlight
- **提示词模板**：mythic winged ceremonial armor, hand-forged dark metal feathers, ancient textile underlayers, restrained supernatural presence, historical material credibility
- **风格补充**：mythic winged ceremonial armor, hand-forged dark metal feathers, ancient textile underlayers, restrained supernatural presence, historical material credibility
- **创意模式**：平衡
- **推荐版本**：v8.2
- **推荐参数**：stylize=350, chaos=8, referenceStrategy=prompt

### 74. 宇宙王朝遗迹 (`cosmic-dynasty`)

- **类别**：东方美学
- **校准**：导演校准
- **视觉机制**：东方宫阙与宇宙尺度结合，强调遗迹感和庄严秩序，避免廉价仙侠光效。
- **镜头语言**：wide anamorphic composition, slow depth layers, silhouette-first lighting
- **提示词模板**：ancient dynasty ruins drifting through a cosmic environment, monumental gates, eroded inscriptions without readable text, celestial dust, solemn scale
- **风格补充**：ancient dynasty ruins drifting through a cosmic environment, monumental gates, eroded inscriptions without readable text, celestial dust, solemn scale
- **创意模式**：探索
- **推荐版本**：v8.2
- **推荐参数**：stylize=430, chaos=15, referenceStrategy=prompt

### 75. 民俗夜祭 (`folk-ritual-night`)

- **类别**：东方美学
- **校准**：导演校准
- **视觉机制**：民俗材料必须真实，奇异感来自行为、面具与火光，不靠随机怪物。
- **镜头语言**：handheld 35mm observational frame, mixed firelight and moonlight, imperfect focus
- **提示词模板**：night folk ritual with handmade masks, paper structures, ember light, smoke, worn textiles, documentary authenticity and uncanny restraint
- **风格补充**：night folk ritual with handmade masks, paper structures, ember light, smoke, worn textiles, documentary authenticity and uncanny restraint
- **创意模式**：平衡
- **推荐版本**：v8.2
- **推荐参数**：stylize=230, chaos=10, referenceStrategy=prompt

### 76. 古机械圣龛 (`ancient-machine-reliquary`)

- **类别**：东方美学
- **校准**：导演校准
- **视觉机制**：古代器物与机械结构融合，铜锈、石材和活动关节都要有功能依据。
- **镜头语言**：macro-to-medium product archaeology, raking side light, dark neutral environment
- **提示词模板**：ancient mechanical reliquary, oxidized bronze mechanisms, carved stone housing, ritual wear, tiny functional joints, sacred industrial atmosphere
- **风格补充**：ancient mechanical reliquary, oxidized bronze mechanisms, carved stone housing, ritual wear, tiny functional joints, sacred industrial atmosphere
- **创意模式**：平衡
- **推荐版本**：v8.2
- **推荐参数**：stylize=310, chaos=9, referenceStrategy=prompt

### 77. 雕塑产品舞台 (`sculptural-product-stage`)

- **类别**：商业设计
- **校准**：导演校准
- **视觉机制**：单一产品成为雕塑主体，用材质对比和阴影组织高级感，拒绝装饰堆砌。
- **镜头语言**：70mm product lens, controlled three-quarter view, clean studio falloff
- **提示词模板**：sculptural commercial product stage, one hero object, precise material contrast, engineered shadow, restrained accent color, premium art direction
- **风格补充**：sculptural commercial product stage, one hero object, precise material contrast, engineered shadow, restrained accent color, premium art direction
- **创意模式**：忠实
- **推荐版本**：v8.2
- **推荐参数**：stylize=170, chaos=3, raw=true, referenceStrategy=prompt

### 78. 半透明生物材质 (`translucent-biomaterial`)

- **类别**：商业设计
- **校准**：导演校准
- **视觉机制**：玻璃、凝胶和柔性薄膜有真实折射与厚度，色彩克制。
- **镜头语言**：macro product photography, grazing light, shallow focus with precise edge detail
- **提示词模板**：translucent biomaterial objects, soft membranes, glass and gel interfaces, internal light scattering, clinical yet sensual product visualization
- **风格补充**：translucent biomaterial objects, soft membranes, glass and gel interfaces, internal light scattering, clinical yet sensual product visualization
- **创意模式**：平衡
- **推荐版本**：v8.2
- **推荐参数**：stylize=290, chaos=8, referenceStrategy=prompt

### 79. 编辑部档案拼贴 (`editorial-archive-grid`)

- **类别**：商业设计
- **校准**：导演校准
- **视觉机制**：用档案照片、样本、纸张和网格讲清设计过程，避免 PPT 卡片感。
- **镜头语言**：top-down reprographic view mixed with one cinematic hero crop
- **提示词模板**：editorial archive composition, contact sheets, material swatches, cropped evidence photographs, disciplined grid, tactile paper depth, no readable text
- **风格补充**：editorial archive composition, contact sheets, material swatches, cropped evidence photographs, disciplined grid, tactile paper depth, no readable text
- **创意模式**：平衡
- **推荐版本**：v8.2
- **推荐参数**：stylize=220, chaos=11, referenceStrategy=prompt

### 80. 冷光科技极简 (`luminous-tech-minimal`)

- **类别**：商业设计
- **校准**：导演校准
- **视觉机制**：科技感来自光学路径、玻璃与精密金属，不用满屏蓝紫霓虹。
- **镜头语言**：telephoto still life, compressed layers, narrow rim lighting, clean reflections
- **提示词模板**：luminous technology still life, dark neutral field, thin optical light paths, precise glass and machined metal, controlled negative space
- **风格补充**：luminous technology still life, dark neutral field, thin optical light paths, precise glass and machined metal, controlled negative space
- **创意模式**：忠实
- **推荐版本**：v8.2
- **推荐参数**：stylize=150, chaos=4, raw=true, referenceStrategy=prompt

### 81. 尺度断裂奇观 (`scale-rupture`)

- **类别**：实验创意
- **校准**：导演校准
- **视觉机制**：只改变一个尺度关系，其他物理与材质保持真实，使奇观更可信。
- **镜头语言**：wide perspective with a foreground scale cue, deep focus, one decisive vanishing point
- **提示词模板**：a believable everyday scene ruptured by one impossible change of scale, seamless material continuity, clear human reference, cinematic wonder
- **风格补充**：a believable everyday scene ruptured by one impossible change of scale, seamless material continuity, clear human reference, cinematic wonder
- **创意模式**：探索
- **推荐版本**：v8.2
- **推荐参数**：stylize=360, chaos=18, referenceStrategy=prompt

### 82. 模拟介质梦境 (`analog-dream-transfer`)

- **类别**：实验创意
- **校准**：导演校准
- **视觉机制**：多重曝光、光晕和介质颗粒围绕主体发生，不能把主体完全溶解。
- **镜头语言**：close cinematic crop, layered focal planes, in-camera transition feeling
- **提示词模板**：analog dream transfer, optical printing artifacts, soft halation, layered exposures, tactile grain, recognizable subject preserved through abstraction
- **风格补充**：analog dream transfer, optical printing artifacts, soft halation, layered exposures, tactile grain, recognizable subject preserved through abstraction
- **创意模式**：探索
- **推荐版本**：v8.2
- **推荐参数**：stylize=400, chaos=17, referenceStrategy=prompt

### 83. 材质异变研究 (`material-mutation-study`)

- **类别**：实验创意
- **校准**：导演校准
- **视觉机制**：同一轮廓跨材质演化，像严谨的视觉实验，不是随机材质拼盘。
- **镜头语言**：orthographic sequence with one hero perspective insert, even reference lighting
- **提示词模板**：material mutation study where one object transitions through stone, textile, glass and living tissue, scientific sequencing, coherent silhouette
- **风格补充**：material mutation study where one object transitions through stone, textile, glass and living tissue, scientific sequencing, coherent silhouette
- **创意模式**：探索
- **推荐版本**：v8.2
- **推荐参数**：stylize=340, chaos=16, referenceStrategy=prompt

### 84. 诗性监控视角 (`poetic-surveillance`)

- **类别**：实验创意
- **校准**：导演校准
- **视觉机制**：疏离的观察角度与细小人物行为构成情绪，不生成时间码或界面文字。
- **镜头语言**：high corner angle or long-lens exterior view, partial occlusion, flat ambient light
- **提示词模板**：poetic surveillance image, distant human behavior, obstructed viewpoint, timestamp-free institutional framing, quiet emotional anomaly
- **风格补充**：poetic surveillance image, distant human behavior, obstructed viewpoint, timestamp-free institutional framing, quiet emotional anomaly
- **创意模式**：忠实
- **推荐版本**：v8.2
- **推荐参数**：stylize=130, chaos=5, raw=true, referenceStrategy=prompt
