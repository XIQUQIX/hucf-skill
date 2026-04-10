"""
build_highlights.py

从 data/ 下的原始对话文件，自动提炼每月 highlights.md。

用法：
    python tools/build_highlights.py                  # 处理所有月份
    python tools/build_highlights.py --month 2023-03  # 只处理某个月
    python tools/build_highlights.py --overwrite      # 覆盖已有的 highlights

依赖：
    pip install anthropic
    并设置环境变量 ANTHROPIC_API_KEY
"""

import os
import re
import argparse
import time
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

import anthropic

# ── 路径配置 ──────────────────────────────────────────────
ROOT = Path(__file__).parent.parent
DATA_DIR = ROOT / "hucf-skill" / "data"
EPISODES_DIR = ROOT / "hucf-skill" / "knowledge" / "episodes"

# ── 提示词 ────────────────────────────────────────────────
SYSTEM_PROMPT = """你是一个语料整理助手。
你的任务是从户晨风的直播对话原文中，挑选出最能体现他说话风格的片段，整理成结构化的 highlights.md 文件。

选片段的标准：
1. 能体现他的强观点输出（结论先行、不留灰度）
2. 能体现他的标签化表达（苹果人/安卓人、月薪XXX等）
3. 能体现他的直播互动风格（对线、连麦、施压）
4. 能体现他的口头禅和节奏感

每个月挑 5-8 个片段，不要太多。
每个片段保留足够上下文（至少保留户晨风的完整一段话），不要截断。"""

USER_PROMPT_TEMPLATE = """以下是户晨风 {year_month} 的直播对话原文（可能包含多个文件的内容）：

{raw_content}

---

请从中挑选 5-8 个最有代表性的片段，输出为以下格式的 Markdown：

```markdown
# {year_month} 精选片段

## 片段 001 — [一句话描述]
**日期**：YYYY-MM-DD  
**主题**：[主题标签，如：直播互动 / 购买力 / 品牌消费观 / 社会阶层 / 城市选择]

> [对话内容，保留"某网友："和"户晨风："的对话格式]

**风格要点**：[2-3个关键词，描述这个片段体现了他的什么风格特点]

---

## 片段 002 — ...
```

只输出 Markdown 内容，不要加任何解释。"""


def get_month_folders():
    """获取所有月份文件夹，返回 (folder_path, month_key) 列表"""
    months = []
    for folder in sorted(DATA_DIR.iterdir()):
        if not folder.is_dir():
            continue
        # 文件夹名如 "2023年03月"，转成 "2023-03"
        match = re.match(r"(\d{4})年(\d{2})月", folder.name)
        if match:
            month_key = f"{match.group(1)}-{match.group(2)}"
            months.append((folder, month_key))
    return months


def load_month_content(folder: Path, max_chars=40000):
    """读取一个月份文件夹下所有 .md 文件，合并成一段文本"""
    parts = []
    for md_file in sorted(folder.glob("*.md")):
        if md_file.name == "README.md":
            continue
        text = md_file.read_text(encoding="utf-8").strip()
        if text:
            parts.append(f"<!-- 文件：{md_file.name} -->\n{text}")

    combined = "\n\n---\n\n".join(parts)

    # 超长则截断，避免超出 token 限制
    if len(combined) > max_chars:
        combined = combined[:max_chars] + "\n\n[... 内容过长，已截断 ...]"

    return combined


def build_highlights(folder: Path, month_key: str, client: anthropic.Anthropic):
    """调用 Claude API，生成一个月的 highlights.md"""
    year_month_cn = folder.name  # 如 "2023年03月"

    raw_content = load_month_content(folder)
    if not raw_content.strip():
        print(f"  ⚠️  {month_key}: 没有有效内容，跳过")
        return None

    print(f"  📖  {month_key}: 读取了 {len(raw_content)} 字符，正在调用 API...")

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4000,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": USER_PROMPT_TEMPLATE.format(
                    year_month=year_month_cn,
                    raw_content=raw_content,
                ),
            }
        ],
    )

    result = response.content[0].text

    # 去掉可能的 ```markdown ``` 包裹
    result = re.sub(r"^```markdown\n?", "", result.strip())
    result = re.sub(r"\n?```$", "", result.strip())

    return result.strip()


def main():
    parser = argparse.ArgumentParser(description="自动生成每月 highlights.md")
    parser.add_argument("--month", type=str, help="只处理某个月，如 2023-03")
    parser.add_argument(
        "--overwrite", action="store_true", help="覆盖已有的 highlights.md"
    )
    args = parser.parse_args()

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ 请先设置环境变量 ANTHROPIC_API_KEY")
        return

    client = anthropic.Anthropic(api_key=api_key)

    months = get_month_folders()
    if not months:
        print(f"❌ 在 {DATA_DIR} 下没有找到月份文件夹")
        return

    # 过滤指定月份
    if args.month:
        months = [(f, m) for f, m in months if m == args.month]
        if not months:
            print(f"❌ 没有找到月份 {args.month}")
            return

    print(f"📅 共找到 {len(months)} 个月份，开始处理...\n")

    success, skip, error = 0, 0, 0

    for folder, month_key in months:
        output_dir = EPISODES_DIR / month_key
        output_file = output_dir / "highlights.md"

        # 跳过已有文件（除非 --overwrite）
        if output_file.exists() and not args.overwrite:
            print(f"  ⏭️  {month_key}: 已存在，跳过（用 --overwrite 强制重建）")
            skip += 1
            continue

        try:
            result = build_highlights(folder, month_key, client)
            if result:
                output_dir.mkdir(parents=True, exist_ok=True)
                output_file.write_text(result, encoding="utf-8")
                print(f"  ✅  {month_key}: 已生成 → {output_file.relative_to(ROOT)}")
                success += 1
            # 避免频繁请求
            time.sleep(1)
        except Exception as e:
            print(f"  ❌  {month_key}: 出错 — {e}")
            error += 1

    print(f"\n🎉 完成！成功 {success} 个，跳过 {skip} 个，失败 {error} 个")


if __name__ == "__main__":
    main()
