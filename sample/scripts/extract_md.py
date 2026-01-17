import sys
import re

def extract_markdown(text):
    # Try to find content within ```markdown ... ``` blocks
    pattern = r"```markdown\s*(.*?)\s*```"
    matches = re.findall(pattern, text, re.DOTALL)
    
    if matches:
        # Return the longest match, assuming it's the main content
        return max(matches, key=len)
    
    # Fallback: try ``` ... ``` without language specifier
    pattern_generic = r"```\s*(.*?)\s*```"
    matches_generic = re.findall(pattern_generic, text, re.DOTALL)
    if matches_generic:
         return max(matches_generic, key=len)

    # If no code blocks, assume the whole text is markdown but strip intro/outro
    # This is a naive heuristic; better to rely on prompts enforcing code blocks.
    return text

if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        content = sys.stdin.read()
    
    print(extract_markdown(content))
