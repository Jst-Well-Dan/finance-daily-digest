---
name: video-transcriber
description: Transcribe video and audio files to text/Markdown using SiliconFlow AI API (SenseVoiceSmall). Supports batch processing and various formats (MP4, MP3, etc.).
---

# Video Transcriber

## Overview

This skill provides AI-powered transcription capabilities to convert video and audio files into Markdown text. It uses the **SiliconFlow API** (specifically the `FunAudioLLM/SenseVoiceSmall` model) for high-accuracy, multi-language transcription.

## When to Use This Skill

Activate this skill when the user:
- Requests video transcription ("转录视频", "提取字幕", "视频转文字")
- Wants to convert video/audio to text or Markdown
- Provides a local video or audio file and asks for its content summary or transcript
- Needs to extract a transcript from a previously downloaded video

## Core Capabilities

### 1. Video/Audio Transcription
Convert video or audio files to Markdown text using SiliconFlow's free AI transcription API.

**Example usage:**
```
User: "Transcribe this video: course_recording.mp4"
User: "将这个转录成文字: interview_audio.mp3"
User: "Extract transcript from meeting_video.mkv"
```

**Supported formats:**
- Audio: MP3, WAV, M4A, FLAC, AAC, OGG, OPUS, WMA
- Video: MP4, AVI, MOV, MKV, FLV, WMV, WEBM, M4V

## Response Pattern

### Step 1: Check Prerequisites
Verify SiliconFlow API key is available via `SILICONFLOW_API_KEY` environment variable or provided by user.

**API Key Setup:**
- Get free API key from: https://cloud.siliconflow.cn/account/ak
- Set environment variable: `SILICONFLOW_API_KEY=sk-xxx`

### Step 2: Convert Video to Audio (Important!)
**SiliconFlow API 对大文件（>50MB）不稳定，建议先将视频转为音频再转录。**

**Project output convention:** For a new daily run, resolve `<daily_dir>/YYYYMMDD` with `python .\scripts\resolve_daily_dir.py --ensure`; `daily_dir` is defined once in the project-root `content_paths.json`. Put the source video, extracted audio, transcript Markdown, and any later summaries in that run's video subdirectory. If the user provides only a loose file, keep the transcript beside that file unless they ask otherwise.

```bash
# 使用 ffmpeg 将视频转换为 MP3 音频
ffmpeg -i "video.mp4" -vn -acodec libmp3lame -q:a 2 "video.mp3" -y
```

**说明：**
- 转换后文件大小通常减小 80-90%
- 避免 API 返回 500 错误
- 支持直接输入音频文件（MP3, WAV 等）

### Step 3: Execute Transcription
Use the bundled script `scripts/transcribe_siliconflow.py`:

```bash
# 转录音频（推荐）
python scripts/transcribe_siliconflow.py --file "video.mp3" --output "video.md"

# 输出仅包含转录文本，无元数据
```

### Step 4: Report Results
Report completion, content folder, output filename, size, and provide a short preview of the transcript.

## Troubleshooting

### Issue: Transcription API key error
**Solution:** Verify API key starts with `sk-` and is correctly set in environment or `.env` file.

### Issue: Transcription returns empty text
**Solution:** Check if audio is clear; verify file format; ensure file is not corrupted.

## Technical Details

### Bundled Script
The script `scripts/transcribe_siliconflow.py` handles the interaction with the SiliconFlow API.

**Parameters:**
- `--file, -f`: Input audio/video file (required)
- `--api-key, -k`: API key (optional if env var is set)
- `--output, -o`: Output path
- `--model, -m`: Model (default: `FunAudioLLM/SenseVoiceSmall`)
