# 户晨风.Skill

> ### 说白了就是这样

[![Codex Ready](https://img.shields.io/badge/Claude_Code-Ready-2F6FEB?style=for-the-badge)](https://github.com/anthropics/claude-code)
[![Local First](https://img.shields.io/badge/Knowledge-Local_First-0A7F5A?style=for-the-badge)]()
[![MIT License](https://img.shields.io/badge/License-MIT-F2C94C?style=for-the-badge)](LICENSE)

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
