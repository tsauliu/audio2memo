# Audio to Memo 项目

## 项目简介

本项目旨在将音频文件（如会议录音、语音备忘录等）自动化处理，最终生成结构化的会议纪要、逐字稿等文本产物。整个流程包括音频文件的预处理、语音识别、大语言模型内容提炼及格式化输出。

## 主要功能

*   自动从 Dropbox 获取最新的音频文件。
*   支持多种音频格式（如 MP3, M4A, WAV 等），并能自动分割大型音频文件以符合处理要求。
*   集成 OpenAI (GPT-4o, Whisper) 进行语音转文字。
*   使用大语言模型 (Gemini, Deepseek) 将原始语音转录稿优化为通顺的逐字稿。
*   使用大语言模型 (Gemini) 从逐字稿中提炼生成会议纪要。
*   将最终的会议纪要和逐字稿整合成 `.docx` 文件，并保存到本地及 Dropbox。
*   生成 Markdown 格式的纪要，并上传到对象存储服务 (OSS)。
*   通过飞书机器人发送处理状态通知。

## 技术栈

*   **Python**: 主要编程语言。
*   **pydub**: 用于音频文件处理和分割。
*   **OpenAI API**: 用于语音识别 (Whisper, GPT-4o 系列模型)。
*   **Google Generative AI (Gemini API)**: 用于文本生成和摘要 (会议纪要、逐字稿优化)。
*   **Deepseek API**: 可选的文本生成模型。
*   **python-docx**: 用于创建和操作 `.docx` 文件。
*   **boto3**: 用于与腾讯云对象存储 COS 交互。
*   **tiktoken**: 用于计算文本的 token 数量。

## 环境要求

1.  **Python**: 建议使用 Python 3.8 或更高版本。
2.  **操作系统**: 无特殊要求，Windows, macOS, Linux 均可。
3.  **依赖库**:
    *   在项目根目录下有一个 `requirements.txt` 文件，包含了所有必要的 Python 依赖。通过以下命令安装：
        ```bash
        pip install -r requirements.txt
        ```
    *   **FFmpeg**: `pydub` 依赖 FFmpeg 进行音频格式转换和处理。请确保 FFmpeg 已正确安装并配置在系统路径中。
4.  **环境变量与API密钥**:
    *   项目中包含一个 `env.py` 文件 (或 `env_example.py` 类似的模板文件)，用于存储各种 API 密钥和配置信息。请根据模板创建或修改 `env.py` 文件，并填入以下密钥：
        *   `keysecret`: OpenAI API 密钥。
        *   `api_key_deepseek`, `model_id_deepseek`: Deepseek API 密钥和模型 ID (如果使用)。
        *   `gemini_key`: Google Gemini API 密钥。
        *   `oss_key`, `oss_access`, `bucket_name`: 腾讯云对象存储 (COS) 的 Access Key ID, Secret Access Key, 以及存储桶名称。
        *   飞书机器人 Webhook URL (在 `funcs.py` 中的 `feishu_bot` 函数内硬编码，可按需修改)。
    *   Dropbox 路径：脚本中硬编码了 Dropbox 路径 (`~/Dropbox/VoiceMemos/`)，请根据实际情况修改或配置。

## 安装与配置

1.  **克隆仓库** (如果项目在版本控制下):
    ```bash
    git clone <repository_url>
    cd audio2memo
    ```
2.  **安装依赖**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **安装 FFmpeg**:
    *   访问 [FFmpeg 官网](https://ffmpeg.org/download.html) 下载适合您操作系统的版本并安装。确保将其添加到系统 PATH 环境变量中。
4.  **配置 API 密钥**:
    *   复制 `env_example.py` (如果存在) 为 `env.py`。
    *   编辑 `env.py` 文件，填入上一节中提到的所有必需的 API 密钥和配置信息。
5.  **检查模板文件**:
    *   确保项目根目录下存在 `memo_template.docx` 文件，此为生成 Word 文档的模板。

## 使用方法

通过运行主脚本 `run.py` 来启动整个处理流程：

```bash
python run.py
```

脚本运行时会提示用户进行以下选择：

1.  **选择音频文件**:
    *   脚本会列出 `~/Dropbox/VoiceMemos/` 目录下的所有音频文件（按修改时间倒序排列，排除 `.docx` 文件）。
    *   用户需要输入文件对应的序号来选择要处理的音频。默认选择第一个文件。
2.  **选择语音识别模型**:
    *   用户可以选择使用的语音识别模型：
        1.  `gpt-4o-transcribe` (默认)
        2.  `gpt-4o-mini-transcribe`
        3.  `whisper-1`
    *   输入对应的数字选择模型，默认为 1。

脚本会根据用户的选择，自动执行后续所有处理步骤。

## 处理流程详解

项目的数据处理流程主要分为以下几个阶段，每个阶段由相应的 Python 脚本和函数负责：

1.  **初始化与文件准备 (`run.py`)**
    *   设置基础路径 `base_path`。
    *   列出并允许用户从 `~/Dropbox/VoiceMemos/` 目录选择音频文件。
    *   解析项目名称 (`project`) 和文件类型 (`filetype`)。
    *   允许用户选择语音识别模型 (`input_model`)。
    *   将选定的音频文件从 Dropbox 路径复制到本地的 `0_raw_audio/` 目录（如果目标文件不存在）。
    *   通过飞书机器人发送文件复制状态通知。

2.  **音频预处理与分割 (`process_audio.py`)**
    *   **调用**: `run.py` 中调用 `split_audio` 函数。
    *   **输入**: `0_raw_audio/{project}.{filetype}` 中的原始音频文件。
    *   **处理**:
        *   `get_file_size_mb`: 获取文件大小。
        *   `get_format`: 根据文件扩展名获取 `pydub` 支持的正确格式名称。
        *   `split_audio`:
            *   加载音频文件 (使用 `AudioSegment.from_file`)。
            *   如果文件大小和时长未超过预设阈值 (`max_size_mb=25MB`, `max_duration_sec=1500s`)，则直接复制到输出目录。
            *   否则，根据大小和时长计算需要分割的段数，确保每段符合 API 的限制。
            *   将音频分割成多个部分，并尝试以原始格式导出。如果失败，则尝试以 MP3 格式导出。
    *   **输出**: 分割后的音频片段保存到 `./0_processed_audio/{project}/` 目录下。
    *   **依赖**: `pydub`, FFmpeg。

3.  **语音转文字 (`audio2text.py`)**
    *   **调用**: `run.py` 中调用 `process_audio_files` 函数。
    *   **输入**: `./0_processed_audio/{project}/` 目录下的音频片段。
    *   **处理**:
        *   `process_audio_files`:
            *   遍历指定项目处理后的音频文件夹中的所有音频文件。
            *   对每个音频文件调用 `audio2text` 函数。
        *   `audio2text`:
            *   使用 `openai.audio.transcriptions.create` API 将音频文件转换为文本。
            *   `input_model` 参数决定了使用的 OpenAI 模型 (e.g., `gpt-4o-transcribe`, `whisper-1`)。
            *   生成的转录文本包含时间戳。
    *   **输出**: 每个音频片段的转录文本（`.txt` 文件）保存到 `./1_transcript/{project}/` 目录下，文件名包含原始音频名和时间戳。
    *   **依赖**: `openai` 库, OpenAI API 密钥 (`env.py`)。

4.  **生成逐字稿 (`text_to_wordforword.py`)**
    *   **调用**: `run.py` 中调用 `text_to_wordforword` 函数。
    *   **输入**: `./1_transcript/{project}/` 目录下的所有转录文本文件。
    *   **处理**:
        *   `combine_transcripts` (来自 `funcs.py`):
            *   读取并合并 `./1_transcript/{project}/` 目录下的所有 `.txt` 文件，按文件名排序，确保转录内容的正确顺序。
        *   加载 `./prompt/prompt_audio2word.md` 作为大语言模型的提示 (prompt)。
        *   动态替换提示中的 `{wordcountmin}` 和 `{wordcountmax}` 占位符。
        *   计算输入 token 数量 (使用 `funcs.count_tokens`)。
        *   调用大语言模型 (默认 `gemini_model`，可选 `deepseek_model`，均来自 `funcs.py`) 处理合并后的转录稿和提示，生成优化后的逐字稿。
    *   **输出**: 生成的逐字稿文本文件保存到 `./2_wordforword/{project}_{timestamp}.txt`。
    *   **依赖**: `google-generativeai` 或 `openai` (for Deepseek) 库, Gemini/Deepseek API 密钥 (`env.py`)。

5.  **生成会议纪要 (`wordforword_to_memo.py`)**
    *   **调用**: `run.py` 中调用 `wordforword_to_memo` 函数。
    *   **输入**: `./2_wordforword/` 中最新的逐字稿文件 (通过 `combine_transcripts` 间接获取，实际是 `./1_transcript/{project}/` 的合并内容，这里逻辑上应使用 `2_wordforword` 的输出，但代码显示 `combine_transcripts` 仍读取 `1_transcript`。**注意：此处可能需要检查逻辑是否符合预期，如果 `wordforword_to_memo` 依赖的是优化后的逐字稿，则应读取 `2_wordforword` 目录下的文件。** 当前脚本 `wordforword_to_memo.py` 调用 `combine_transcripts`，它读取的是 `1_transcript` 目录。)
    *   **处理**:
        *   加载 `./prompt/prompt_word2memo.md` 作为大语言模型的提示。
        *   调用 `gemini_model` (来自 `funcs.py`) 处理（可能是原始）转录稿和提示，生成会议纪要。
    *   **输出**: 生成的会议纪要文本文件保存到 `./3_memo/{project}_{timestamp}.txt`。
    *   **依赖**: `google-generativeai` 库, Gemini API 密钥 (`env.py`)。

6.  **合并输出与分发 (`combine_to_docx.py`)**
    *   **调用**: `run.py` 中调用 `combine_to_docx` 函数。
    *   **输入**:
        *   `./3_memo/` 中最新的会议纪要文件。
        *   `./2_wordforword/` 中最新的逐字稿文件。
        *   `memo_template.docx` 模板文件。
    *   **处理**:
        *   使用 `python-docx` 加载 `memo_template.docx`。
        *   读取会议纪要 (`.txt` 文件)，根据 Markdown 风格的标题 (`#`, `##`, `###`) 添加到 Word 文档中，并应用预设样式 (`title1`, `title2`, `contentlist`, `sublist`)。
        *   添加分页符。
        *   添加 "Full Discussion" 章节标题。
        *   读取逐字稿 (`.txt` 文件)，同样根据 Markdown 标题风格添加到 Word 文档中。
        *   保存生成的 Word 文档到 `./4_docx/{project}_{todaydate}.docx`。
        *   将生成的 `.docx` 文件复制到 Dropbox 路径 `~/Dropbox/VoiceMemos/`。
        *   创建 Markdown 文件：
            *   在 `./5_markdown/{project}_{todaydate}.md` 创建文件。
            *   写入 "Key takeaways" 部分，内容来自会议纪要，并将 Markdown 标题层级调整。
            *   写入 "Full Discussion" 部分，内容来自逐字稿。
        *   `save_transcript_to_oss` (来自 `funcs.py`): 将生成的 Markdown 文件上传到腾讯云 COS。
    *   **输出**:
        *   `.docx` 文件: `./4_docx/{project}_{todaydate}.docx` 和 `~/Dropbox/VoiceMemos/{project}_{todaydate}.docx`。
        *   Markdown 文件: `./5_markdown/{project}_{todaydate}.md`。
        *   文件上传到 COS。
    *   **依赖**: `python-docx` 库, `boto3` 库, 腾讯云 COS 配置 (`env.py`)。

7.  **辅助函数 (`funcs.py`)**
    *   `combine_transcripts`: 合并指定项目下的所有转录文本。
    *   `count_tokens`: 使用 `tiktoken` 计算文本的 token 数量。
    *   `deepseek_model`: 调用 Deepseek API 进行文本生成。
    *   `gemini_model`: 调用 Gemini API 进行文本生成。
    *   `feishu_bot`: 向指定的飞书机器人 Webhook URL 发送文本消息。
    *   `save_transcript_to_oss`: 将文件上传到腾讯云 COS。

## 目录结构

```
.
├── 0_raw_audio/                  # 存放从 Dropbox 复制过来的原始音频文件
│   └── {project_name}.{ext}
├── 0_processed_audio/            # 存放分割后的小音频片段
│   └── {project_name}/
│       └── {project_name}_part1.{ext}
│       └── ...
├── 1_transcript/                 # 存放语音转文字的原始文本结果
│   └── {project_name}/
│       └── {project_name}_part1_{timestamp}.txt
│       └── ...
├── 2_wordforword/                # 存放优化后的逐字稿
│   └── {project_name}_{timestamp}.txt
├── 3_memo/                       # 存放生成的会议纪要
│   └── {project_name}_{timestamp}.txt
├── 4_docx/                       # 存放最终生成的 .docx 文件
│   └── {project_name}_{timestamp}.docx
├── 5_markdown/                   # 存放最终生成的 Markdown 文件 (用于上传OSS)
│   └── {project_name}_{timestamp}.md
├── prompt/                       # 存放给大语言模型的提示文件
│   ├── prompt_audio2word.md
│   └── prompt_word2memo.md
├── run.py                        # 主运行脚本
├── process_audio.py              # 音频处理与分割脚本
├── audio2text.py                 # 语音转文字脚本
├── text_to_wordforword.py        # 逐字稿生成脚本
├── wordforword_to_memo.py        # 会议纪要生成脚本
├── combine_to_docx.py            # 合并输出为 .docx 和 .md 的脚本
├── funcs.py                      # 包含通用函数 (API调用、文件合并等)
├── env.py                        # (用户需自行创建) 存放API密钥和配置
├── requirements.txt              # Python 依赖列表
├── memo_template.docx            # 生成 Word 文档的模板
└── README.md                     # 本说明文件
```

## 注意事项

*   **API 成本**: 使用 OpenAI, Gemini, Deepseek 等 API 会产生费用，请注意控制使用量。
*   **FFmpeg**: 必须正确安装 FFmpeg 并且其路径已添加到系统环境变量中，否则 `pydub` 可能无法正常工作。
*   **文件路径**: 脚本中部分文件路径 (如 Dropbox 路径) 是硬编码的，如果您的目录结构不同，请相应修改脚本。
*   **错误处理**: 脚本包含一些基本的错误处理，但在生产环境中使用前建议进行更全面的测试和增强。
*   **提示工程**: 生成文本的质量高度依赖于 `prompt/` 目录下的提示文件内容，您可以根据需要调整这些提示。
*   **模型选择**: `run.py` 中允许用户选择语音识别模型。不同模型的准确率、速度和成本各不相同。
*   **逻辑一致性检查**: `wordforword_to_memo.py` 当前似乎使用原始转录稿 (来自 `1_transcript`) 生成纪要，而非优化后的逐字稿 (来自 `2_wordforword`)。如果预期是基于优化稿生成纪要，需要调整 `wordforword_to_memo.py` 中获取输入文本的逻辑。

## 未来可改进方向

*   将硬编码的路径和配置项移至配置文件。
*   增加更灵活的音频来源选择（例如本地上传、URL等）。
*   对生成的文本进行更细致的后处理和校对。
*   提供 Web 界面进行操作。
*   更完善的错误处理和日志记录。 