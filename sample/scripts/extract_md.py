import sys
import re

def extract_markdown(text):
    # 尝试在 ```markdown ... ``` 块中查找内容
    pattern = r"```markdown\s*(.*?)\s*```"
    matches = re.findall(pattern, text, re.DOTALL)
    
    if matches:
        # 返回最长的匹配项，假设它是主要内容
        return max(matches, key=len)
    
    # 后备方案：尝试没有语言说明符的 ``` ... ```
    pattern_generic = r"```\s*(.*?)\s*```"
    matches_generic = re.findall(pattern_generic, text, re.DOTALL)
    if matches_generic:
         return max(matches_generic, key=len)

    # 如果没有代码块，假设整个文本是 markdown，但去除开头/结尾
    # 这是一个简单的启发式方法；最好依靠提示词强制使用代码块。
    return text

if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        content = sys.stdin.read()
    
    print(extract_markdown(content))