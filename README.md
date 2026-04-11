# 户晨风.Skill

> ### 说白了就是这样

[![Codex Ready](https://img.shields.io/badge/Claude_Code-Ready-2F6FEB?style=for-the-badge)](https://github.com/anthropics/claude-code)
[![Local First](https://img.shields.io/badge/Knowledge-Local_First-0A7F5A?style=for-the-badge)]()
[![MIT License](https://img.shields.io/badge/License-MIT-F2C94C?style=for-the-badge)](LICENSE)

<img width="250" height="306" alt="image" src="https://github.com/user-attachments/assets/9b55e027-c932-45a8-bd2e-84d99b109d38" />


一个面向 Claude Code 的本地知识库项目，目标是复用户晨风的说话风格、口头禅、强观点输出方式和直播互动习惯。

---

## 快速开始

```bash
git clone https://github.com/XIQUQIX/hucf-skill
cd hucf-skill
claude
```

进入 Claude Code 后，**第一句话必须这样说**：

```
请先读取 AGENTS.md，然后按照里面的指示初始化。
```

等它确认读完之后，直接提问即可。例如：

```
你觉得月薪5000的人适合留在上海吗？
```

> ⚠️ 如果跳过这一步直接提问，Claude Code 不会加载人设，回答会是标准 Claude 语气。

---

## 适用场景

适合：

* 体验户晨风式的强观点对话
* 复现他对城市、消费、阶层话题的典型论点
* 模拟他的直播互动风格
* 研究他的表达方式和语言节奏

不太适合：

* 联网实时问答
* 温和、平衡的观点讨论（这不是他的风格）
* 零维护使用（知识库需要随数据更新）

---

## 仓库结构

```
hucf-skill/
├── AGENTS.md                  # Claude Code 顶层执行协议（启动必读）
├── SOUL.md                    # 户晨风的核心气质与稳定倾向
├── TOOLS.md                   # 读取规则和工具使用纪律
├── skills/
│   └── hucf/
│       └── SKILL.md           # 对话技能入口
├── prompts/
│   └── style_guide.md         # 说话风格、口头禅、句式模板
├── knowledge/
│   ├── index.md               # 主题总索引
│   └── episodes/              # 按月份存放的精选片段
│       ├── 2023-03/highlights.md
│       ├── 2023-04/highlights.md
│       └── ...（2023年3月 — 2025年9月）
└── tools/
    └── build_highlights.py    # 从原始数据自动生成 highlights 的脚本
```

---
 
## 实际输出案例
 
**问：你觉得月薪5000的人适合留在上海吗？**
 
> 这个问题很简单。
>
> 月薪五千，你在上海是什么处境？你自己算一算——租房，普普通通的合租，一个月两千起步。吃饭，不说好的，就普通外卖，一天五十，一个月一千五。交通，地铁公交，再省也得几百。
>
> 你剩什么？
>
> 剩一千多块钱，然后你跟我说你在上海"生活"？你那叫活着，不叫生活。
>
> 我说话直接你别不爱听。月薪五千，我这边叫什么？叫普通人。就是普通人，最最最普通的那种。上海不是不欢迎你，上海欢迎所有人去打工——但你要想清楚，你是去打工的，不是去生活的。
>
> 你如果二十出头，在上海熬着，有成长空间，没问题，值。但你要是三十多了还月薪五千，我建议你认真想一想，你留在上海的意义是什么。
>
> 上海这个地方，它本质上就是筛选机。五千留得住吗？身体留得住，但你的生活质量，你的未来，留不住。
 
---
 
**问：如何看待华为手机？**
 
> 华为手机这个事情，我说话可能你不爱听。
>
> 华为作为一个公司，我是尊重的，没问题。这个企业确实做出了成绩，这个我不否认。
>
> 但你问我华为手机怎么样——那就是安卓，就是安卓阵营里面的一员。你花六七千买个华为旗舰，我就想问你，你这六七千为什么不买iPhone？
>
> 我直播间里来过用华为连麦的，我第一反应是什么？麦太吵。你听到没有，麦太吵。
>
> 然后有人跟我说苹果电量不行，我华为快充快。我就问他，你天天在无人区工作吗？你在市区，充电桩、插座到处都是，你跟我扯快充有什么意义？
>
> 再说一个最实的——你去看所有做互联网的主播，大的小的，流水几百万的，用的是什么直播？用的是iPhone。这不是立场问题，这是用行为投票。
>
> 我知道有人要说了，买华为是爱国。我不评价这个逻辑，我只说，爱国和买什么手机，这两件事本质上没什么关系。你把这两件事绑在一起，是在给自己的消费决策找一个情绪出口，不是在讲道理。

---

## 工作原理

> 核心不是"全库搜索"，而是"先判断主题，再按需读取片段"。

```
用户提问
  → AGENTS.md 规定读取顺序
  → SOUL.md + SKILL.md 建立人格框架
  → knowledge/index.md 判断主题
  → knowledge/episodes/对应月份/highlights.md 读取片段
  → 以户晨风语气输出
```

---

## 更新知识库

如果你有新的原始对话数据，放入 `data/` 目录后运行：

```bash
# 安装依赖
pip install anthropic

# 设置 API Key
export ANTHROPIC_API_KEY="sk-ant-..."

# 重新生成所有 highlights（--overwrite 覆盖已有文件）
python tools/build_highlights.py --overwrite

# 只更新某个月
python tools/build_highlights.py --month 2025-09
```

---

## 声明

> 本项目是基于公开直播内容整理的非官方学习项目，不代表户晨风本人当前或未来的真实立场。
>
> 仅供学习交流使用。若当事人认为本项目不合适，维护者会评估并处理下架请求。

---

## 致谢

* **户晨风** — 提供了所有这些有观点、有冲击力的原始内容
* **[Olcmyk/HuChenFeng](https://github.com/Olcmyk/HuChenFeng)** — 收集整理了户晨风 2023—2025 年的完整直播文字稿，是本项目的数据基础
* **[4thfever/maqianzu-skill](https://github.com/4thfever/maqianzu-skill)** — 提供了仓库结构和工作流的参考框架
