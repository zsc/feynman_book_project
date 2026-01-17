# 自动生成内容的 Makefile

include input.mk

# 默认配置
PYTHON := python3
SCRIPTS := scripts
GEMINI := $(PYTHON) $(SCRIPTS)/gemini_wrapper.py
# 如果真实环境有 gemini cli，可以使用：
# GEMINI := gemini --yolo

# 输出目录
HTML_DIR := html

.PHONY: all index chapters images html commit clean list_chapters

all:
	@$(MAKE) index.md
	@$(MAKE) chapters
	@$(MAKE) images
	@$(MAKE) html
	@$(MAKE) commit

# 第一步：生成 index.md
index.md: input.mk CLAUDE.md
	@echo "正在生成 index.md..."
	@$(GEMINI) text --context CLAUDE.md --prompt "主题: $(TOPIC)。文件组织是 index.md + chapter1.md + ... 现在生成 index.md，包含详细的章节列表（文件名必须是 chapter1.md, chapter2.md 等），以及每章的详细小节列表。请用中文输出。使用 Markdown 代码块。" > index.raw
	@$(PYTHON) $(SCRIPTS)/extract_md.py index.raw > index.md
	@rm index.raw

# 第二步：生成章节
# 我们需要从 index.md 中解析出章节列表。我们可以生成一个辅助的 makefile 片段。
chapters.mk: index.md
	@echo "正在从 index.md 解析章节..."
	@echo "CHAPTERS := $$($(PYTHON) $(SCRIPTS)/parse_chapters.py index.md)" > chapters.mk

-include chapters.mk

chapters: chapters.mk
	@if [ -z "$(CHAPTERS)" ]; then \
		echo "在 index.md 中未找到章节"; \
		exit 1; \
	fi
	@echo "正在生成章节: $(CHAPTERS)"
	@$(MAKE) -j 4 $(CHAPTERS)

# 单个章节的生成规则
chapter%.md: index.md CLAUDE.md
	@echo "正在生成 $@..."
	@$(GEMINI) text --context CLAUDE.md index.md --prompt "生成 $@ (第 $* 章)。高质量，详细。使用 index.md 作为大纲。中文输出。使用 Markdown 代码块。" > $@.raw
	@$(PYTHON) $(SCRIPTS)/extract_md.py $@.raw > $@
	@rm $@.raw

# 第三步：生成图片
# 图片依赖于对应的章节
IMAGES := $(CHAPTERS:.md=.png)

images: chapters
	@echo "正在生成图片: $(IMAGES)"
	@$(MAKE) -j 1 $(IMAGES)

# 单个图片的生成规则
chapter%.png: chapter%.md
	@echo "正在为 $< 生成图片..."
	@$(GEMINI) image --context $< --prompt "根据本章内容，以吉伊卡哇风格生成一篇总结竖版海报（先分别细说细节，最后再进行总结比较）。真的生成图（中文）。" --output $@

# 第四步：转换为 HTML
html: $(CHAPTERS) $(IMAGES) index.md
	@echo "正在转换为 HTML..."
	@mkdir -p $(HTML_DIR)
	@$(PYTHON) $(SCRIPTS)/convert.py . $(HTML_DIR)

# 第五步：Git 提交
commit:
	@echo "正在提交更改..."
	git add .
	git commit -m "自动生成内容: $(TOPIC)" || echo "没有需要提交的内容"

clean:
	rm -f index.md chapter*.md *.png chapters.mk index.raw *.raw
	rm -rf $(HTML_DIR)