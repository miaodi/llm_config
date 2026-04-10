# llm_config

Personal LLM settings, system prompts, and tool configurations.

## Structure

```
llm_config/
├── prompts/
│   ├── general.md        # General-purpose assistant instructions
│   └── coding.md         # Coding assistant instructions (C++ / scientific computing)
└── configs/
    ├── claude.md         # Custom instructions for Claude
    ├── copilot-instructions.md  # GitHub Copilot workspace instructions
    └── cursor-rules.md   # Cursor IDE rules
```

## Usage

- **`prompts/`** – Reusable system prompts. Paste or reference these when starting a new chat session.
- **`configs/`** – Tool-specific configuration snippets. Follow each file's instructions to apply settings in the respective tool.