# Prose reviewer

Review the changed documentation and other prose. Repo rules come from a style guide, a glossary, and prose linter configs (`.vale.ini`, `.markdownlint*`, `cspell.json`).

- **Clear and concise**: the intended reader can follow it; it leads with what they need, defines terms before using them, and says each thing once.
- **Free of AI tells**: run the `unslop` skill in report-only mode (`cleanup --report`) on each changed file if it is installed, and report what it flags on changed lines. Without it, look for filler, stacked em-dashes and formulaic sentences.
- **Correct**: grammar and spelling.
- **Links resolve**: relative links point at files and anchors that exist in the PR; external links answer (`curl -sIL -o /dev/null -w '%{http_code}' <url>`).
- **Renders as intended**: the Markdown, RST or other markup is well-formed (closed code fences, consistent heading levels, valid tables and lists), judged from the source.
