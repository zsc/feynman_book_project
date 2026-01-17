# Automated Content Generation Pipeline / 自动化内容生成流水线

## Background / 背景

This project implements an automated workflow to generate comprehensive guides or books from a single topic description. It leverages **Makefiles** for process orchestration and **LLMs (like Gemini-3-Pro)** for content generation. The pipeline handles the entire lifecycle: from outlining (index generation) to detailed chapter writing, image generation, HTML conversion, and version control.

本项目实现了一个自动化工作流，能够根据单一主题描述生成指南或书籍。它利用 **Makefile** 进行流程编排，并使用 **LLM（如 Gemini-3-Pro）** 进行内容生成。该流水线涵盖了从大纲编写（生成索引）、详细章节写作、配图生成、HTML 转换到版本控制的全生命周期。

## Directory Structure (Sample) / 目录结构 (Sample)

The `sample/` directory contains a complete scaffold of the project. / `sample/` 目录包含项目的完整脚手架。

### Core Files / 核心文件

*   **`sample/Makefile`**
    *   **English:** The main orchestration script. It defines the dependencies and steps: `index -> chapters -> images -> html -> commit`. It supports parallel text generation and serial image generation.
    *   **Chinese:** 主流程编排脚本。定义了依赖关系和步骤：`索引 -> 章节 -> 图片 -> HTML -> 提交`。支持并行文本生成和串行图片生成。

*   **`sample/input.mk`**
    *   **English:** Configuration file containing the input `TOPIC`.
    *   **Chinese:** 配置文件，包含输入的 `TOPIC`（主题）。

*   **`sample/CLAUDE.md`**
    *   **English:** Context file containing project rules and prompt context for the LLM.
    *   **Chinese:** 上下文文件，包含项目规则和供 LLM 使用的提示词上下文。

### Scripts (`sample/scripts/`) / 脚本文件

*   **`gemini_wrapper.py`**
    *   **English:** A wrapper for the `gemini` CLI. It handles prompt construction and can run in **Mock Mode** (default) or call the real API (if `USE_REAL_GEMINI=1` is set).
    *   **Chinese:** `gemini` CLI 的包装器。处理提示词构建，可以在 **Mock 模式**（默认）下运行，或调用真实 API（需设置 `USE_REAL_GEMINI=1`）。

*   **`parse_chapters.py`**
    *   **English:** Parses the generated `index.md` to extract chapter filenames for dynamic Makefile dependencies.
    *   **Chinese:** 解析生成的 `index.md`，提取章节文件名以构建动态 Makefile 依赖。

*   **`extract_md.py`**
    *   **English:** Robustly extracts Markdown content blocks from LLM responses.
    *   **Chinese:** 健壮地从 LLM 响应中提取 Markdown 内容块。

*   **`convert.py`**
    *   **English:** Converts the generated Markdown files into a static HTML website with an index.
    *   **Chinese:** 将生成的 Markdown 文件转换为带有索引的静态 HTML 网站。

## Usage / 使用方法

```bash
cd sample

# Clean and run the full pipeline (Mock Mode)
# 清理并运行完整流程（Mock 模式）
make clean && make all

# To use real Gemini API (requires 'gemini' CLI)
# 使用真实 Gemini API（需要 'gemini' CLI）
export USE_REAL_GEMINI=1
make clean && make all
```
