import argparse
import subprocess
import sys
import shutil
import os
import time

def run_gemini_text(context_files, prompt):
    # 构建完整提示词
    full_content = ""
    for fpath in context_files:
        try:
            with open(fpath, 'r', encoding='utf-8') as f:
                full_content += f.read() + "\n\n"
        except FileNotFoundError:
            print(f"警告: 未找到上下文文件 {fpath}。", file=sys.stderr)

    full_content += prompt
    
    # 检查 'gemini' 命令是否存在，并且用户是否想要使用它
    if shutil.which("gemini") and os.environ.get("USE_REAL_GEMINI") == "1":
        # echo full_content | gemini --yolo
        process = subprocess.Popen(["gemini", "--yolo"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate(input=full_content)
        if process.returncode != 0:
            print(f"Gemini CLI 错误: {stderr}", file=sys.stderr)
            sys.exit(process.returncode)
        print(stdout)
    else:
        # 模拟行为
        print(f"未找到 GEMINI CLI 或未启用。模拟响应。", file=sys.stderr)
        print("```markdown")
        print(f"# 生成的响应: {prompt[:30]}...")
        if "index.md" in prompt:
            print("这里是索引：\n\n[第一章](chapter1.md)\n[第二章](chapter2.md)")
        else:
            print("## 第一节\n本章内容...\n\n## 第二节\n更多内容...")
        print("```")

def run_gemini_image(context_files, prompt, output_path):
    # 构建提示词
    full_content = ""
    for fpath in context_files:
        try:
            with open(fpath, 'r', encoding='utf-8') as f:
                full_content += f.read() + "\n\n"
        except Exception:
            pass
    full_content += prompt

    if shutil.which("gemini") and os.environ.get("USE_REAL_GEMINI") == "1":
        # 对于图片，假设 gemini cli 可以处理或者我们需要特定的标志。
        # 提示词暗示 `gemini --yolo` 适用于文本。
        # 对于图片，它说“nano banana pro”。可能是不同的模型参数。
        # 暂时只传递提示词给 gemini，但在实际情况中这可能需要特定的图片生成工具。
        # 因为我是脚手架，我会只 touch 文件或复制一个占位符。
        print(f"正在生成图片到 {output_path} (模拟真实生成调用)", file=sys.stderr)
        # 模拟：创建一个空白图片
        with open(output_path, 'wb') as f:
            f.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82')
    else:
        print(f"模拟图片生成: {output_path}", file=sys.stderr)
        with open(output_path, 'wb') as f:
             f.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82')

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    text_parser = subparsers.add_parser("text")
    text_parser.add_argument("--context", nargs="+", default=[])
    text_parser.add_argument("--prompt", required=True)

    image_parser = subparsers.add_parser("image")
    image_parser.add_argument("--context", nargs="+", default=[])
    image_parser.add_argument("--prompt", required=True)
    image_parser.add_argument("--output", required=True)

    args = parser.parse_args()

    if args.command == "text":
        run_gemini_text(args.context, args.prompt)
    elif args.command == "image":
        run_gemini_image(args.context, args.prompt, args.output)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()