#!/usr/bin/env node
/** 聚合当日所有*_结构化笔记.md 的“核心结论”写入 YYYYMMDD_解读君视频总结.md，逻辑与 SKILL.md 固定总结结构一致，用 pi 生成便于月度换模型 */
import fs from "node:fs"; import path from "node:path";
import { createAgentSession, ModelRuntime, resolveCliModel } from "@earendil-works/pi-coding-agent";
const args = process.argv.slice(2);
const idx = args.indexOf("--daily-dir"); const dailyDir = idx>=0 ? args[idx+1] : null;
if (!dailyDir) { console.error("--daily-dir required"); process.exit(1); }
const abs = path.resolve(dailyDir);
const date = path.basename(abs);
const notes = [];
for (const d of fs.readdirSync(abs, {withFileTypes:true}).filter(x=>x.isDirectory())) {
  const dir = path.join(abs,d.name);
  for (const f of fs.readdirSync(dir).filter(x=>x.endsWith("_结构化笔记.md"))) {
    const p = path.join(dir,f); const txt = fs.readFileSync(p,"utf-8");
    const core = (txt.match(/## 1\. 核心结论[\s\S]*?(?=\n## \d+\.)/)||[])[0] || txt.slice(0,4000);
    const title = (txt.match(/^# 结构化笔记｜(.+)/m)||[])[1] || d.name;
    notes.push({title, core});
  }
}
if (notes.length===0) { console.log("no notes"); process.exit(0); }
const prompt = `你是财经编辑。请将以下 ${notes.length} 篇视频的“核心结论”原样聚合为每日总结，严格按以下结构输出，不要加入综合判断、跨视频结论或额外段落：

# 解读君视频摘要

${notes.map((n,i)=>`## ${i+1}. ${n.title}\n\n<!-- 原样复制该视频结构化笔记的“核心结论”章节。 -->\n${n.core.trim()}`).join("\n\n")}

要求：只做原样聚合与编号，不改写、不总结、不加综合段落。直接输出 Markdown。`;
let out=""; const modelRuntime=await ModelRuntime.create(); const opts={};
if(process.env.PI_MODEL){ const r=resolveCliModel({cliModel:process.env.PI_MODEL,modelRuntime}); if(r.model) opts.model=r.model; else console.warn(`PI_MODEL 无法解析（${r.error||r.warning}），使用默认模型`); }
const {session}=await createAgentSession(opts);
const unsub=session.subscribe(e=>{ if(e.type==="message_update"&&e.assistantMessageEvent?.type==="text_delta"){ out+=e.assistantMessageEvent.delta; process.stdout.write(e.assistantMessageEvent.delta);} });
try{ await session.prompt(prompt);} finally{ unsub(); session.dispose(); }
out=out.trim().replace(/^```markdown\s*/i,"").replace(/```\s*$/,"").trim();
const target=path.join(abs, `${date}_解读君视频总结.md`);
fs.writeFileSync(target,out,"utf-8");
console.log(`\n✓ 总结已写入 ${target}`);
