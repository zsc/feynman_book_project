import sys
import re

def parse_chapters(index_content):
    # Look for patterns like [Chapter 1](chapter1.md) or just chapter1.md
    # We'll look for filenames ending in .md that look like chapters.
    # Regex to capture `chapterX.md` or `sectionX.md`
    
    # Pattern: match alphanumeric strings ending in .md, ignore index.md
    files = set(re.findall(r'\b(chapter\d+\.md)\b', index_content, re.IGNORECASE))
    
    # Sort them naturally
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
