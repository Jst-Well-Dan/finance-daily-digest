#!/usr/bin/env python3
"""合并中英字幕(SRT)为按视频章节组织的双语 Markdown。
逻辑：滚动去重（自动字幕每条cue重复前文，只取新增部分）→ 按标点/字数/停顿分段 →
中英按时间重叠对齐 → 按章节输出。不做任何总结改写。
用法: python merge_subs.py <en.srt> <zh.srt> <out.md>
章节硬编码自 yt-dlp --print "%(chapters)s" (视频 7xTGNNLPyMI，2026-09-28 获取)。
"""
import re
import sys

CHAPTERS = [
    ("introduction", 0, 60),
    ("pretraining data (internet)", 60, 467),
    ("tokenization", 467, 867),
    ("neural network I/O", 867, 1211),
    ("neural network internals", 1211, 1561),
    ("inference", 1561, 1869),
    ("GPT-2: training and inference", 1869, 2572),
    ("Llama 3.1 base model inference", 2572, 3563),
    ("pretraining to post-training", 3563, 3666),
    ("post-training data (conversations)", 3666, 4832),
    ("hallucinations, tool use, knowledge/working memory", 4832, 6106),
    ("knowledge of self", 6106, 6416),
    ("models need tokens to think", 6416, 7271),
    ("tokenization revisited: models struggle with spelling", 7271, 7493),
    ("jagged intelligence", 7493, 7648),
    ("supervised finetuning to reinforcement learning", 7648, 8082),
    ("reinforcement learning", 8082, 8867),
    ("DeepSeek-R1", 8867, 9727),
    ("AlphaGo", 9727, 10106),
    ("reinforcement learning from human feedback (RLHF)", 10106, 11379),
    ("preview of things to come", 11379, 11715),
    ("keeping track of LLMs", 11715, 11914),
    ("where to find LLMs", 11914, 12106),
    ("grand summary", 12106, 12683),
]


def ts_to_sec(ts: str) -> float:
    h, m, s = ts.replace(",", ".").split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)


def sec_to_ts(sec: float) -> str:
    sec = max(0, int(sec))
    return f"{sec // 3600}:{(sec % 3600) // 60:02d}:{sec % 60:02d}"


def parse_srt(path: str):
    raw = open(path, encoding="utf-8-sig").read()
    blocks = re.split(r"\n\s*\n", raw.strip())
    cues = []
    for b in blocks:
        lines = b.strip().splitlines()
        if len(lines) < 3:
            continue
        m = re.match(r"(\S+)\s*-->\s*(\S+)", lines[1])
        if not m:
            continue
        text = " ".join(l.strip() for l in lines[2:] if l.strip())
        # 去掉行内多余空白
        text = re.sub(r"\s+", " ", text).strip()
        if not text:
            continue
        cues.append((ts_to_sec(m.group(1)), ts_to_sec(m.group(2)), text))
    return cues


def dedupe_rolling(cues):
    """自动字幕滚动去重：只保留相对上一条新增的文字。"""
    out = []
    prev = ""
    for s, e, t in cues:
        if e - s < 0.05:  # 10ms 级填充 cue，直接跳过
            continue
        if t == prev:
            continue
        if prev and t.startswith(prev):
            new = t[len(prev):].strip()
        elif prev and prev.startswith(t):
            continue
        else:
            # 找最大前后缀重叠
            overlap = 0
            for n in range(min(len(prev), len(t)), 0, -1):
                if prev.endswith(t[:n]):
                    overlap = n
                    break
            new = t[overlap:].strip()
        if new:
            out.append((s, e, new))
            prev = t if len(t) > len(prev) else (prev + " " + new)
        else:
            prev = t
    return out


END_PUNCT = re.compile(r"[.?!。？！…]$")


def to_paragraphs(cues, max_words=70, max_gap=3.0):
    paras = []
    cur_text, cur_s, cur_e, words = [], None, None, 0
    for s, e, t in cues:
        if cur_text is None or not cur_text:
            cur_s = s
        if cur_s is not None and cur_text and (s - cur_e) > max_gap:
            paras.append((cur_s, cur_e, " ".join(cur_text)))
            cur_text, cur_s, words = [], s, 0
        cur_text.append(t)
        cur_e = e
        words += len(t.split())
        if END_PUNCT.search(t) and words >= 15:
            paras.append((cur_s, cur_e, " ".join(cur_text)))
            cur_text, cur_s, words = [], None, 0
        elif words >= max_words:
            paras.append((cur_s, cur_e, " ".join(cur_text)))
            cur_text, cur_s, words = [], None, 0
    if cur_text:
        paras.append((cur_s, cur_e, " ".join(cur_text)))
    return paras


def align_zh(en_paras, zh_cues):
    """每个英文段落，按时间重叠取中文 cues 并滚动去重拼接。
    取不到则放宽 ±8 秒；仍取不到返回空（YouTube 中文轨止于约 3:03:50，
    后续英文段落本就没有中文，禁止用“最近一条”硬凑，避免张冠李戴）。"""
    out = []
    for s, e, t in en_paras:
        matched = [x for x in zh_cues if x[1] > s and x[0] < e]
        if not matched:
            matched = [x for x in zh_cues if x[1] > s - 8 and x[0] < e + 8]
        parts, prev = [], ""
        for _, _, zt in matched:
            if zt == prev or (prev and prev.endswith(zt)):
                continue
            if prev and zt.startswith(prev):
                zt = zt[len(prev):].strip()
            if zt:
                parts.append(zt)
                prev = (prev + " " + zt) if prev else zt
        out.append((s, e, t, " ".join(parts)))
    return out


def main():
    en_path, zh_path, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
    en_cues = dedupe_rolling(parse_srt(en_path))
    zh_cues = dedupe_rolling(parse_srt(zh_path))
    en_paras = to_paragraphs(en_cues)
    merged = align_zh(en_paras, zh_cues)

    lines = [
        "# Deep Dive into LLMs like ChatGPT｜中英对照（按章节）",
        "",
        "> 来源：https://www.youtube.com/watch?v=7xTGNNLPyMI ｜ "
        "YouTube 自动字幕整理，仅滚动去重与分段，未做总结改写。英文为语音识别原稿，中文为机器翻译。注意：YouTube 提供的简体中文轨止于约 3:03:50（第 19 章 RLHF 中段），此后约 27 分钟仅有英文。",
        "",
    ]
    for i, (title, cs, ce) in enumerate(CHAPTERS, 1):
        lines.append(f"## {i}. {title}（{sec_to_ts(cs)}–{sec_to_ts(ce)}）")
        lines.append("")
        segs = [(s, e, en, zh) for s, e, en, zh in merged if s >= cs and s < ce]
        if not segs:
            lines.append("（本章无字幕）")
            lines.append("")
            continue
        for s, e, en, zh in segs:
            lines.append(f"### {sec_to_ts(s)}–{sec_to_ts(e)}")
            lines.append("")
            lines.append(f"EN：{en}")
            lines.append("")
            lines.append(f"中文：{zh if zh else '（YouTube 中文自动字幕止于约 3:03:50，本段暂无中文）'}")
            lines.append("")
    open(out_path, "w", encoding="utf-8").write("\n".join(lines))
    n_para = sum(1 for l in lines if l.startswith("### "))
    print(f"chapters={len(CHAPTERS)} paragraphs={n_para} "
          f"en_cues={len(en_cues)} zh_cues={len(zh_cues)} -> {out_path}")


if __name__ == "__main__":
    main()
