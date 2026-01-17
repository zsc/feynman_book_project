有一个流程想转成 Makefile。你可以写一些 python 脚本把中间步自动化（只简单时用 bash；复杂一点都 python）。
输入是一行描述（放在一个 .mk里，放在一个目录下）。
第一步是把这个 .mk 嵌入（用 include？）到一个 CLAUDE.md 里，然后用提示词“文件组织是 index.md + chapter1.md + ... 现在生成 index.md，包含详细的 chapter list，和每 chapter 详细 section list”，来生成 index.md（需要从输出结果中匹配 markdown 块提取，也时会因为 index.md 里又含了 markdown 要处理下格式错乱）。
接下来是一个可并行步，用gemini-3-pro，把 CLAUDE.md 和 index.md 作为 prefix，后面接提示词“高质量生成 chapter1.md。尽量详细。”，再按多轮对话接一轮“方向正确，大幅扩写 chapter1.md”，来生成 chapter1.md。
接下是根据 index.md 和 chapter1.md 用 nano banana pro（gemini-3-pro） 来生成一张图，提示词是“根据以上，以吉伊卡哇风格生成一篇总结竖版海报（先分别细说细节，最后再进行总结比较）。真的生成图（中文）”。存好图。
最后调用 python ~/d/md_to_html/convert.py . html 在目录下新建 html，并在 html/index.ml 里可以看到多章的教程的索引。
把目录下的 .md 和 html 目录中内容 git commit。

gemini-3-pro 的调用用 gemini-cli（`gemini --yolo`）。gpt5-pro 得手动（但也尽量自动准备好输入，和尽量自动处理输出来兜底）。

----
现在在 sample 目录下生成 Makefile 等 scaffold 文件。
