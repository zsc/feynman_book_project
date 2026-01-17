import sys
import re

def parse_chapters(index_content):
    # 查找类似 [Chapter 1](chapter1.md) 或仅仅是 chapter1.md 的模式
    # 我们将查找以 .md 结尾且看起来像章节的文件名。
    # 正则表达式捕获 `chapterX.md` 或 `sectionX.md`
    
    # 模式：匹配以 .md 结尾的字母数字字符串，忽略 index.md
    files = set(re.findall(r'\b(chapter\d+\.md)\b', index_content, re.IGNORECASE))
    
    # 自然排序
    def natural_sort_key(s):
        return [int(text) if text.isdigit() else text.lower()
                for text in re.split('([0-9]+)', s)]
    
    return sorted(list(files), key=natural_sort_key)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        content = sys.stdin.read()
        
    chapters = parse_chapters(content)
    print(" ".join(chapters))