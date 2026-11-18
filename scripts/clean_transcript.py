#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
clean_transcript.py — 转写稿清洗：规则层（免费/确定性）+ LLM 层（修错字/断句）。

产出独立文件 `标题 [ID]_清洗版.md`，**原文永不覆盖**，便于随时对照核验。
下游「结构化笔记」优先读清洗版，缺失或过短时自动回落原文。

用法:
    python scripts/clean_transcript.py --daily-dir daily/20261117
    python scripts/clean_transcript.py --daily-dir daily/20261117 --limit 1
    python scripts/clean_transcript.py --daily-dir daily/20261107 --rules-only
    python scripts/clean_transcript.py --daily-dir daily --all --limit 3    # 跨日期取最近 N 篇
    python scripts/clean_transcript.py --daily-dir daily/20261117 --force    # 覆盖重跑

两级清洗:
    ① 规则层：删语气词（啊/呢/呃/嗯…）、emoji、日文假名乱码、重复词与重复标点、
       残留的孤立拉丁噪声词。纯 Python，确定性、零成本、秒级。
    ② LLM 层：修 ASR 错字（验冷→液冷、民意GDP→名义GDP）、删口误自我重复
       （"我们觉得我们觉得"）、切分自然段落。不改写、不删观点、不补充内容。

健全性校验: LLM 输出长度须落在规则稿的 [55%, 115%] 区间，且不得比正文短到疑似
摘要。超界视为失败，保留规则稿（仍可用），下次运行自动重试 LLM 层。

环境变量:
    YOUTUBE_CLEAN_MODEL   清洗用 LLM 模型，默认回落到 YOUTUBE_NOTES_MODEL，
                          再回落到 opendesign/deepseek-v4.1-flash。
退出码: 0=全部成功或无待办, 1=部分失败(已保留规则稿)。
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
from pathlib import Path

# 2026-11-18: muse-spark(openCode Go) 订阅已失效，全链路默认改用 opendesign/deepseek-v4.1-flash
DEFAULT_MODEL = "opendesign/deepseek-v4.1-flash"
CLEAN_SUFFIX = "_清洗版.md"
NOTE_SUFFIX = "_结构化笔记.md"
DIR_RE = re.compile(r"\[[A-Za-z0-9_-]{6,}\]$")
VID_RE = re.compile(r"\[([A-Za-z0-9_-]{6,})\]$")
BODY_MARK = "## 转写正文"

# 语气助词集合。刻意不含「吧/嘛/啦」的句子末尾疑问用法之外的高风险词；
# 删除只发生在标点边界，避免误伤「什么呢」以外的实义词。
# 语气助词常量区（上方已定义 SOFT_CLASS / HARD_CLASS）

# ASR 常见拉丁噪声词：出现在句首且后接中文时几乎必然是识别噪声（So./No./OK.）
NOISE_TOKEN_RE = re.compile(
    r"((?<=[。！？；\n])|^)[ \t]*"
    r"(?:Ohello|Hhello|Hello|Oh|No|So|Yes|Well|Okay|OK|Uh|Um|Ah|Eh|Hmm)[.。，,]?[ \t]*"
    r"(?=[\u4e00-\u9fa5])",
    re.I,
)


def strip_noise_chars(text: str) -> str:
    """删除 emoji、变体选择符、零宽字符、日文假名乱码。"""
    out = []
    for ch in text:
        code = ord(ch)
        cat = unicodedata.category(ch)
        if cat in {"So", "Sk", "Cf"}:  # emoji / 修饰符号 / 零宽
            continue
        if 0x3040 <= code <= 0x30FF:  # 平假名 + 片假名
            continue
        if 0xFF66 <= code <= 0xFF9F:  # 半角片假名
            continue
        if code in {0xFE0F, 0xFE0E, 0x200B, 0x200C, 0x200D, 0xFEFF}:
            continue
        out.append(ch)
    return "".join(out)


# 纯语气词（永不是实词成分），可无条件删
SOFT_FILLERS = "啊呃嗯哦喔噢诶唉呀呗咯咩"
SOFT_CLASS = f"[{SOFT_FILLERS}]"
# 「呢/吧」可能表疑问，需看前文
HARD_CLASS = "[呢吧]"
QUESTION_WORDS = (
    "什么", "怎么", "哪", "谁", "多少", "几", "是否", "是不是",
    "有没有", "能不能", "会不会", "要不要", "该不该", "为什么",
)
# 「那」作指示代词时的后续字，不可当作口头语删除
NA_KEEP = "个些样边儿么时种里头边会次"

def _keep_hard(match: re.Match) -> str:
    """呢/吧：前文是疑问词则视为疑问助词保留，否则删除。"""
    head = match.string[: match.start()]
    return match.group(0) if head.endswith(QUESTION_WORDS) else ""


def drop_fillers(text: str) -> str:
    """删口头语气词。只在能判定为语气助词的位置删，避免破坏实词。"""
    prev = None
    while prev != text:
        prev = text
        # 固定口头语整体删除：哎呀 / 唉呀
        text = re.sub(r"[哎唉][呀啊][，、]?", "", text)
        # 汉字/标点 + 「呢吧」+ 标点或汉字 → 按前文决定去留
        text = re.sub(rf"{HARD_CLASS}(?=[，。！？；：、\u4e00-\u9fa5])", _keep_hard, text)
        # 纯语气词 + 标点 → 只留标点
        text = re.sub(rf"{SOFT_CLASS}+(?=[，。！？；：、])", "", text)
        # 汉字 + 纯语气词 + 汉字 → 删语气词
        text = re.sub(rf"([\u4e00-\u9fa5]){SOFT_CLASS}+(?=[\u4e00-\u9fa5])", r"\1", text)
        # 句首纯语气词（含后随逗号）
        text = re.sub(rf"((?<=[。！？\n])|^)[ \t]*{SOFT_CLASS}+[，、]?[ \t]*", r"\1", text, flags=re.M)
        # 句首口头语「那」：保留「那个/那些/那时」等指示用法
        text = re.sub(
            rf"((?<=[。！？\n])|^)[ \t]*那[，、][ \t]*", r"\1", text, flags=re.M
        )
        text = re.sub(
            rf"((?<=[。！？\n])|^)[ \t]*那(?=[\u4e00-\u9fa5])(?![{NA_KEEP}])", r"\1", text, flags=re.M
        )
    return text


def collapse_repeats(text: str) -> str:
    """删 ASR 自我重复：连续重复的 2-6 字短语、重复标点、重复整句。"""
    # 「我们觉得我们觉得」
    prev = None
    while prev != text:
        prev = text
        text = re.sub(r"([\u4e00-\u9fa5]{2,6})\1", r"\1", text)
    # 「产能。产能。」整句重复
    text = re.sub(r"([^。！？\n]{4,40}[。！？])\s*\1", r"\1", text)
    # 重复标点
    text = re.sub(r"[，、]{2,}", "，", text)
    text = re.sub(r"[。]{2,}", "。", text)
    # 空标点
    text = re.sub(r"([，、])\s*([。！？])", r"\2", text)
    text = re.sub(r"([。！？])[，、]+", r"\1", text)
    return text


def rules_clean(body: str) -> str:
    text = strip_noise_chars(body)
    text = NOISE_TOKEN_RE.sub(r"\1", text)
    text = drop_fillers(text)
    text = collapse_repeats(text)
    # 中文之间不应有空格；换行与段首标点整理
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\s*\n\s*", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"^\s*[，。！？；：、]+", "", text, flags=re.M)
    return text.strip()


LLM_PROMPT = """你是一名中文财经会议记录编辑。下面是一份 ASR（语音识别）自动转写稿，请你做**外科式清洗**，只做减法与纠错，绝不改写观点。

允许做的操作（仅此几类）：
1. 修 ASR 明显错字／错词，依据上下文能确定的才修。参考对：验冷→液冷、CPU（应为 CPO）上下文判断、民意GDP→名义GDP、疾数的抬身→基数的抬升、1几DP→GDP、政政策→政策、超超级点→超节点、次杠杆→去杠杆、突而不举→托而不举、ma by china→made by China。
2. 删除口误与自我重复（如「我们觉得我们觉得」「确实是比较良性的良性的」）、说一半改口的残句、无意义的语气词。
3. 按语义切分自然段（3–8 句一段），段间空一行。
4. 数字与单位还原成可读写法（4.31个→4.3%左右 这类不确定的**不要猜**，保持原样）。

严格禁止：
- 不许概括、缩写、合并观点，不许删掉任何论点、数字、机构名、人名、时间。
- 不许补充原文没有的信息，不许加入小标题、导语、总结、免责声明。
- 不许把口语改写成书面语风格，保持原始措辞与语气。

输出格式（严格遵守，不要任何额外文字）：
## 清洗正文

<清洗后的正文，保留原有顺序>

原始转写稿如下（标题：{title}）：
---
{body}
---
"""


def split_body(text: str) -> tuple[str, str]:
    """返回 (元信息头, 正文)。无标记时全文视为正文。"""
    idx = text.find(BODY_MARK)
    if idx < 0:
        return "", text.strip()
    head_end = idx + len(BODY_MARK)
    return text[:head_end].rstrip(), text[head_end:].strip()


def extract_title(text: str, fallback: str) -> str:
    m = re.search(r"^#\s+(.+)", text, flags=re.M)
    return m.group(1).strip() if m else fallback


def llm_clean(pi_bin: str, model: str, title: str, body: str, timeout: int) -> str | None:
    prompt = LLM_PROMPT.format(title=title, body=body)
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(prompt)
        prompt_file = f.name
    cmd = [pi_bin, "-p", "--no-session", "--no-tools", f"@{prompt_file}"]
    if model:
        cmd += ["--model", model]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, encoding="utf-8", errors="replace")
    except subprocess.TimeoutExpired:
        print(f"  ✗ LLM 超时（>{timeout}s），保留规则稿")
        return None
    finally:
        Path(prompt_file).unlink(missing_ok=True)
    if p.returncode != 0:
        print(f"  ✗ pi 退出码 {p.returncode}: {(p.stderr or '').strip()[-400:]}")
        return None
    out = (p.stdout or "").strip()
    out = re.sub(r"^```(?:markdown)?\s*", "", out, flags=re.I)
    out = re.sub(r"```\s*$", "", out).strip()
    m = re.search(r"##\s*清洗正文\s*\n(.*)$", out, flags=re.S)
    cleaned = m.group(1).strip() if m else out
    # 去掉模型可能加的小标题/分隔线噪声
    cleaned = re.sub(r"^[-*_]{3,}\s*$", "", cleaned, flags=re.M).strip()
    return cleaned or None


def sanity_ok(rule_len: int, llm_text: str) -> tuple[bool, str]:
    n = len(llm_text)
    if rule_len == 0:
        return False, "规则稿为空"
    ratio = n / rule_len
    if ratio < 0.55:
        return False, f"疑似摘要（{ratio:.0%} < 55%），丢弃"
    if ratio > 1.15:
        return False, f"疑似扩写（{ratio:.0%} > 115%），丢弃"
    return True, f"{ratio:.0%}"


def list_transcripts(daily_dirs: list[Path], only_newest: bool) -> list[Path]:
    found: list[Path] = []
    for daily in daily_dirs:
        for d in sorted(daily.iterdir()):
            if not d.is_dir() or not DIR_RE.search(d.name):
                continue
            vid = (VID_RE.search(d.name) or [None, ""])[1]
            if vid.startswith("UC") or "Decoding Finance - Videos" in d.name:
                continue
            for f in sorted(d.iterdir()):
                if not f.is_file() or f.suffix != ".md":
                    continue
                if f.name.endswith(NOTE_SUFFIX) or f.name.endswith(CLEAN_SUFFIX):
                    continue
                if "总结" in f.name:
                    continue
                if f.stat().st_size < 500:
                    continue
                found.append(f)
    # 按日期目录名（= 发布日期）从新到旧
    def key(p: Path):
        dd = p.parent.parent.name
        return (dd, p.stat().st_size)
    found.sort(key=key, reverse=True)
    return found


def process_one(pi_bin: str, model: str, src: Path, timeout: int, rules_only: bool, force: bool) -> tuple[bool, str]:
    target = src.parent / (src.stem + CLEAN_SUFFIX)
    if target.exists() and target.stat().st_size > 800 and not force:
        return True, "skipped"
    raw = src.read_text(encoding="utf-8")
    head, body = split_body(raw)
    title = extract_title(raw, re.sub(r"\s*\[[^\]]+\]$", "", src.parent.name))
    if not body:
        return False, "空正文"

    rule_text = rules_clean(body)
    if not rule_text:
        return False, "规则清洗后为空"
    final = rule_text
    layer = "规则层"
    ratio_note = ""

    if not rules_only:
        llm_text = llm_clean(pi_bin, model, title, rule_text, timeout)
        if llm_text:
            ok, msg = sanity_ok(len(rule_text), llm_text)
            if ok:
                final = llm_text
                layer = f"规则层 + LLM 层（{model}）"
                ratio_note = f"，体量校验 {msg}"
            else:
                ratio_note = f"，LLM 层被拒：{msg}"

    vid = (VID_RE.search(src.parent.name) or [None, ""])[1]
    date_m = re.search(r"发布日期[：:]\s*\**\s*(\d{4}-\d{2}-\d{2})", head)
    url_m = re.search(r"来源[：:]\s*\**\s*(\S+)", head)
    meta = [
        f"# {title}",
        "",
        f"- **视频 ID：** {vid}",
        f"- **发布日期：** {date_m.group(1) if date_m else ''}",
        f"- **来源：** {url_m.group(1) if url_m else ''}",
        f"- **清洗：** {layer}；原 {len(body):,} 字符 → 清洗后 {len(final):,} 字符"
        f"（{len(final)/max(len(body),1):.0%}{ratio_note}）",
        f"- **原文：** `{src.name}`",
        "",
        "## 清洗正文",
        "",
    ]
    target.write_text("\n".join(meta) + final + "\n", encoding="utf-8")
    return True, layer


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--daily-dir", required=True, help="单个日期目录或 daily 根目录")
    ap.add_argument("--limit", type=int, default=0, help="最多处理篇数（0=不限），从最新往前取")
    ap.add_argument("--timeout", type=int, default=600, help="单篇 LLM 超时秒数")
    ap.add_argument("--rules-only", action="store_true", help="只跑规则层，不调 LLM")
    ap.add_argument("--force", action="store_true", help="已存在也重跑覆盖")
    ap.add_argument("--pi-bin", default="pi")
    ap.add_argument("--model", default="", help="覆盖清洗模型")
    args = ap.parse_args()

    root = Path(args.daily_dir)
    if not root.is_dir():
        print(f"✗ 目录不存在: {root}")
        return 1
    daily_dirs = [root] if re.fullmatch(r"\d{8}", root.name) else sorted(
        p for p in root.iterdir() if p.is_dir() and re.fullmatch(r"\d{8}", p.name)
    )

    pi_bin = args.pi_bin
    model = args.model.strip()
    if not args.rules_only:
        if not Path(pi_bin).exists():
            found = shutil.which(pi_bin)
            if not found:
                print(f"✗ 找不到 pi：{pi_bin}（--rules-only 可跳过 LLM 层）")
                return 1
            pi_bin = found
        if not model:
            model = (
                os.environ.get("YOUTUBE_CLEAN_MODEL", "").strip()
                or os.environ.get("YOUTUBE_NOTES_MODEL", "").strip()
                or DEFAULT_MODEL
            )

    items = list_transcripts(daily_dirs, only_newest=True)
    if args.limit > 0:
        items = items[: args.limit]
    if not items:
        print("无待清洗转写稿")
        return 0

    print(f"待清洗 {len(items)} 篇" + ("" if args.rules_only else f"（model={model}）") + " ...")
    failed = 0
    for src in items:
        print(f"\n=== {src.parent.parent.name} / {src.stem[:60]} ===")
        try:
            ok, msg = process_one(pi_bin, model, src, args.timeout, args.rules_only, args.force)
            if ok:
                print(f"  ✓ {msg}")
            else:
                print(f"  ✗ {msg}")
                failed += 1
        except Exception as e:  # noqa: BLE001 — 单篇失败不中断
            print(f"  ✗ 异常: {e}")
            failed += 1
    if failed:
        print(f"\n⚠ {failed}/{len(items)} 篇失败（规则稿已尽量保留，可重跑）")
        return 1
    print("\n全部完成")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
