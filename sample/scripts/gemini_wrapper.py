import argparse
import subprocess
import sys
import shutil
import time

def run_gemini_text(context_files, prompt):
    # Construct full prompt
    full_content = ""
    for fpath in context_files:
        try:
            with open(fpath, 'r', encoding='utf-8') as f:
                full_content += f.read() + "\n\n"
        except FileNotFoundError:
            print(f"Warning: Context file {fpath} not found.", file=sys.stderr)

    full_content += prompt
    
    import os
    
    # Check if 'gemini' command exists and user wants to use it
    if shutil.which("gemini") and os.environ.get("USE_REAL_GEMINI") == "1":
        # echo full_content | gemini --yolo
        process = subprocess.Popen(["gemini", "--yolo"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate(input=full_content)
        if process.returncode != 0:
            print(f"Gemini CLI Error: {stderr}", file=sys.stderr)
            sys.exit(process.returncode)
        print(stdout)
    else:
        # Mock behavior
        print(f"FAILED TO FIND GEMINI CLI. MOCKING RESPONSE.", file=sys.stderr)
        print("```markdown")
        print(f"# Generated Response for: {prompt[:30]}...")
        if "index.md" in prompt:
            print("Here is the index:\n\n[Chapter 1](chapter1.md)\n[Chapter 2](chapter2.md)")
        else:
            print("## Section 1\nContent for this chapter...\n\n## Section 2\nMore content...")
        print("```")

def run_gemini_image(context_files, prompt, output_path):
    # Construct prompt
    full_content = ""
    for fpath in context_files:
        try:
            with open(fpath, 'r', encoding='utf-8') as f:
                full_content += f.read() + "\n\n"
        except Exception:
            pass
    full_content += prompt

    if shutil.which("gemini"):
        # For images, assuming gemini cli handles it or we need a specific flag.
        # The prompt implies `gemini --yolo` works for text. 
        # For images, it says "nano banana pro". Might be a different model param.
        # I'll just pass the prompt to gemini for now, but in reality this might need a specific image generation tool.
        # Since I am scaffolding, I will just touch the file or copy a placeholder.
        print(f"Generating image to {output_path} (Mocking real generation call)", file=sys.stderr)
        # Mock: create a blank image
        with open(output_path, 'wb') as f:
            f.write(b'\x89PNG\r\n\x1a\n\0\0\0\rIHDR\0\0\0\x01\0\0\0\x01\x08\x06\0\0\0\x1f\x15\xc4\x89\0\0\0\nIDATx\x9cc\0\0\x05\0\x01\r\n-\xb4\0\0\0\0IEND\xaeB`\x82')
    else:
        print(f"MOCK IMAGE GEN: {output_path}", file=sys.stderr)
        with open(output_path, 'wb') as f:
             f.write(b'\x89PNG\r\n\x1a\n\0\0\0\rIHDR\0\0\0\x01\0\0\0\x01\x08\x06\0\0\0\x1f\x15\xc4\x89\0\0\0\nIDATx\x9cc\0\0\x05\0\x01\r\n-\xb4\0\0\0\0IEND\xaeB`\x82')

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
