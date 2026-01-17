# Makefile for automating content generation

include input.mk

# Defaults
PYTHON := python3
SCRIPTS := scripts
GEMINI := $(PYTHON) $(SCRIPTS)/gemini_wrapper.py
# If real gemini cli exists, use it:
# GEMINI := gemini --yolo

# Output directories
HTML_DIR := html

.PHONY: all index chapters images html commit clean list_chapters

all:
	@$(MAKE) index.md
	@$(MAKE) chapters
	@$(MAKE) images
	@$(MAKE) html
	@$(MAKE) commit

# Step 1: Generate index.md
index.md: input.mk CLAUDE.md
	@echo "Generating index.md..."
	@$(GEMINI) text --context CLAUDE.md --prompt "Topc: $(TOPIC). File organization is index.md + chapter1.md + ... Now generate index.md, containing detailed chapter list (filenames must be chapter1.md, chapter2.md, etc.), and detailed section list for each chapter. Please output in Chinese. Use Markdown code block." > index.raw
	@$(PYTHON) $(SCRIPTS)/extract_md.py index.raw > index.md
	# @rm index.raw

# Step 2: Generate chapters
# We need to know the list of chapters. We can generate a helper makefile.
chapters.mk: index.md
	@echo "Parsing chapters from index.md..."
	@echo "CHAPTERS := $$($(PYTHON) $(SCRIPTS)/parse_chapters.py index.md)" > chapters.mk

-include chapters.mk

chapters: chapters.mk
	@if [ -z "$(CHAPTERS)" ]; then \
		echo "No chapters found in index.md"; \
		exit 1; \
	fi
	@echo "Generating chapters: $(CHAPTERS)"
	@$(MAKE) -j 4 $(CHAPTERS)

# Rule for individual chapters
chapter%.md: index.md CLAUDE.md
	@echo "Generating $@..."
	@$(GEMINI) text --context CLAUDE.md index.md --prompt "Generate $@ (Chapter $*). High quality, detailed. Use index.md as outline. Output in Chinese. Use Markdown code block." > $@.raw
	@$(PYTHON) $(SCRIPTS)/extract_md.py $@.raw > $@
	@rm $@.raw

# Step 3: Generate images
# Images depend on their respective chapters
IMAGES := $(CHAPTERS:.md=.png)

images: chapters
	@echo "Generating images: $(IMAGES)"
	@$(MAKE) -j 1 $(IMAGES)

# Rule for individual images
chapter%.png: chapter%.md
	@echo "Generating image for $<..."
	@$(GEMINI) image --context $< --prompt "Generate a vertical poster summarizing this chapter in Chiikawa style. First details, then summary. Chinese text." --output $@

# Step 4: Convert to HTML
html: $(CHAPTERS) $(IMAGES) index.md
	@echo "Converting to HTML..."
	@mkdir -p $(HTML_DIR)
	@$(PYTHON) $(SCRIPTS)/convert.py . $(HTML_DIR)

# Step 5: Git Commit
commit:
	@echo "Committing changes..."
	git add .
	git commit -m "Auto-generated content for $(TOPIC)" || echo "Nothing to commit"

clean:
	rm -f index.md chapter*.md *.png chapters.mk index.raw *.raw
	rm -rf $(HTML_DIR)

debug:\n\twhich python3\n\tpython3 --version
