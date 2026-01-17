import sys
import os

try:
    import markdown
    HAS_MARKDOWN = True
except ImportError:
    HAS_MARKDOWN = False

def convert_to_html(source_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Simple index generation
    html_index = "<html><head><meta charset='utf-8'><title>Guide</title></head><body><h1>Guide Index</h1><ul>"
    
    # Find all MD files
    md_files = [f for f in os.listdir(source_dir) if f.endswith('.md')]
    md_files.sort()
    
    for f in md_files:
        if f == "CLAUDE.md": continue
        
        with open(os.path.join(source_dir, f), 'r', encoding='utf-8') as mdf:
            content = mdf.read()
            if HAS_MARKDOWN:
                html = markdown.markdown(content)
            else:
                html = f"<pre>{content}</pre>"
            
        out_name = f.replace('.md', '.html')
        with open(os.path.join(output_dir, out_name), 'w', encoding='utf-8') as outf:
            outf.write(f"<html><head><meta charset='utf-8'></head><body>{html}</body></html>")
            
        html_index += f"<li><a href='{out_name}'>{f}</a></li>"

    html_index += "</ul></body></html>"
    with open(os.path.join(output_dir, "index.html"), 'w', encoding='utf-8') as f:
        f.write(html_index)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python convert.py <source_dir> <output_dir>")
        sys.exit(1)
        
    convert_to_html(sys.argv[1], sys.argv[2])
