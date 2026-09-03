#!/usr/bin/env node
/**
 * generate_notes_via_pi.mjs
 * 用 pi（可切换供应商/模型）为本次 daily 目录下的新转写稿生成结构化笔记。
 * 不依赖 subagent，直接用 pi SDK 按 SKILL.md 的固定模板产出笔记。
 * 用法: node scripts/generate_notes_via_pi.mjs --daily-dir daily/20260903
 * 依赖: npm i @earendil-works/pi-coding-agent  + 已配置的模型密钥（OPENAI_API_KEY / ANTHROPIC_API_KEY 等，或 ~/.pi/auth.json）
 * pi 会自动在可用模型中选择，也可通过环境变量 PI_MODEL=provider/model 指定。
 */
import fs from "node:fs";
import path from "node:path";
import { createAgentSession, ModelRuntime, resolveCliModel } from "@earendil-works/pi-coding-agent";

const TEMPLATE = `# 结构化笔记｜{{TITLE}}

## 0. 来源与材料边界
- 视频标题｜发布日期｜视频 ID｜URL：{{META_LINE}}
- 发言者/机构：
- 材料质量：转写完整性、明显错字/拼接段、无时间戳等问题。
- 证据边界：除已回查的一手资料外，视频中的数字、政策和公司信息均仅视为“转写记录”，不直接当作事实。

## 1. 核心结论
<!-- 3–5 条；每条包含结论及适用条件/边界。此节将被每日总结原样引用。 -->

## 2. 事实与可核验信息
### 2.1 已核验事实
<!-- 仅放已回查至公告、财报、官方数据等一手来源的信息；未做外部核验时明确说明。 -->
### 2.2 视频中的事实性陈述（待核验）
| 陈述 / 数据 | 原始口径或时间 | 说话者 / 来源 | 可信度与问题 |
|---|---|---|---|
### 2.3 转写质量问题

## 3. 专家观点与逻辑链
### 观点 1：主题名称
- **观点归属：**
- **结论：**
- **前提事实：**
- **推导逻辑：** \`前提 A → 变化 B → 结论\`
- **隐含假设：**
- **反例 / 证伪条件：**
- **原文位置：**

## 4. 投资研究指引
> 记录视频所表达的研究方向，不构成买卖建议；没有明确投资含义时如实写“未给出可执行指引”。
| 主题 / 对象 | 视频隐含或明确的方向 | 为什么 | 正向验证信号 | 风险 / 失效信号 | 需补的证据 |
|---|---|---|---|---|---|

## 5. 下一步核验与跟踪
1. **优先核验：**
2. **后续数据 / 事件：**
3. **需回看原视频的位置：**

写作要求：完整阅读转写稿，区分“已核验事实/待核验/观点/整理”；核心结论 3-5 条可独立阅读；观点必须展示推导、隐含假设与证伪条件；无明确方向时写“未给出可执行指引”；发现串入文本须写入转写质量问题并从核心结论剔除。
`;

function parseArgs() {
  const args = process.argv.slice(2);
  let dailyDir = null;
  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--daily-dir" && args[i+1]) dailyDir = args[++i];
  }
  if (!dailyDir) {
    console.error("用法: node scripts/generate_notes_via_pi.mjs --daily-dir daily/YYYYMMDD");
    process.exit(1);
  }
  return { dailyDir };
}

async function generateOne(session, transcriptPath, notePath) {
  const transcript = fs.readFileSync(transcriptPath, "utf-8");
  const dirName = path.basename(path.dirname(transcriptPath));
  // 从转写稿头部提取标题与元信息
  const titleMatch = transcript.match(/^#\s+(.+)/m);
  const title = titleMatch ? titleMatch[1].trim() : dirName.replace(/\s*\[[^\]]+\]$/, "");
  const metaLines = transcript.split("\n").slice(0, 8).join(" | ").slice(0, 400);

  const prompt = `你是一名财经研究员。请完整阅读以下转写稿，并按固定模板生成结构化笔记，直接输出 Markdown 正文，不要解释过程。

固定模板（严格按此结构输出）：
${TEMPLATE.replace("{{TITLE}}", title).replace("{{META_LINE}}", metaLines)}

转写稿全文如下（标题：${title}，路径：${transcriptPath}）：
---
${transcript.slice(0, 30000)}
---

要求：
- 完整阅读后按模板输出，不要省略任何一级标题（0-5）。
- 核心结论 3-5 条，每条含结论+适用条件/边界，将被每日总结原样引用。
- 事实与观点必须分离，未核验的标为待核验。
- 发现串入/拼接/错字写入“转写质量问题”并从结论剔除。
- 直接输出 Markdown，不要包裹代码块。`;

  let output = "";
  const unsub = session.subscribe((event) => {
    if (event.type === "message_update" && event.assistantMessageEvent?.type === "text_delta") {
      output += event.assistantMessageEvent.delta;
      process.stdout.write(event.assistantMessageEvent.delta);
    }
  });
  try {
    await session.prompt(prompt);
  } finally {
    unsub();
  }
  // 清理可能的 ```markdown 包裹与尾部残留（如模型收尾的 `---`、多余空行）
  output = output.trim().replace(/^```markdown\s*/i, "").replace(/^```\s*/i, "").replace(/```\s*$/i, "");
  output = output.replace(/\n?---\s*$/, "").replace(/[\uFEFF\u200B]+/g, "").trim();
  if (output.length < 800) throw new Error(`生成内容过短 (${output.length} 字符)，可能被截断`);
  fs.mkdirSync(path.dirname(notePath), { recursive: true });
  fs.writeFileSync(notePath, output, "utf-8");
  console.log(`\n✓ 已写入 ${notePath} (${output.length} 字符)`);
}

async function main() {
  const { dailyDir } = parseArgs();
  const absDaily = path.resolve(dailyDir);
  if (!fs.existsSync(absDaily)) { console.error(`目录不存在: ${absDaily}`); process.exit(1); }

  // 枚举：目录名以 [ID] 结尾，且含转写稿但缺笔记
  const dirs = fs.readdirSync(absDaily, { withFileTypes: true }).filter(d => d.isDirectory() && /\[[A-Za-z0-9_-]{6,}\]$/.test(d.name));
  const tasks = [];
  for (const d of dirs) {
    const dirPath = path.join(absDaily, d.name);
    const vidMatch = d.name.match(/\[([A-Za-z0-9_-]{6,})\]$/);
    const vid = vidMatch ? vidMatch[1] : "";
    if (vid.startsWith("UC")) continue;
    if (d.name.includes("Decoding Finance")) continue;
    const transcripts = fs.readdirSync(dirPath).filter(f => f.endsWith(".md") && !f.endsWith("_结构化笔记.md") && f.includes(`[${vid}]`));
    if (transcripts.length === 0) {
      // 回退：任何非笔记 md
      const anyMd = fs.readdirSync(dirPath).filter(f => f.endsWith(".md") && !f.endsWith("_结构化笔记.md"));
      if (anyMd.length) transcripts.push(anyMd[0]);
    }
    for (const t of transcripts) {
      const tPath = path.join(dirPath, t);
      if (!fs.existsSync(tPath) || fs.statSync(tPath).size < 500) continue;
      const notePath = path.join(dirPath, `${path.basename(t, ".md")}_结构化笔记.md`);
      if (fs.existsSync(notePath) && fs.statSync(notePath).size > 800) {
        console.log(`跳过已存在: ${notePath}`);
        continue;
      }
      tasks.push({ tPath, notePath });
    }
  }
  if (tasks.length === 0) { console.log("无待生成笔记"); return; }
  console.log(`待生成 ${tasks.length} 篇笔记...`);

  // pi 会话：按环境自动选可用模型，支持 PI_MODEL=provider/model 覆盖
  const modelRuntime = await ModelRuntime.create();
  const opts = {};
  if (process.env.PI_MODEL) {
    const r = resolveCliModel({ cliModel: process.env.PI_MODEL, modelRuntime });
    if (r.model) opts.model = r.model;
    else console.warn(`PI_MODEL 无法解析（${r.error || r.warning}），使用默认模型`);
  }
  const { session } = await createAgentSession(opts);
  try {
    for (const { tPath, notePath } of tasks) {
      console.log(`\n=== 生成 ${path.basename(notePath)} ← ${path.basename(tPath)} ===`);
      try {
        await generateOne(session, tPath, notePath);
      } catch (e) {
        console.error(`✗ 失败 ${notePath}:`, e.message);
        // 保留失败现场，下次重试
      }
    }
  } finally {
    session.dispose();
  }
  console.log("\n全部完成");
}

main().catch(e => { console.error(e); process.exit(1); });
