# my-claude-plugins

Personal Claude Cowork plugin marketplace. Add this repo as a GitHub marketplace source in Cowork to get all plugins below on any machine automatically.

## Plugins

| Plugin | Version | Description |
|--------|---------|-------------|
| [resume-tailor](./resume-tailor/) | 0.1.0 | Tailor your resume for any job — ATS-optimized, recruiter-ready |
| [gdrive-file-reader](./gdrive-file-reader/) | 0.1.0 | Read .docx, .pdf, and .md files from Google Drive that the native connector doesn't handle well |

## Adding a New Plugin

1. Create a new folder at the repo root: `mkdir my-new-plugin`
2. Add the required files (see structure below)
3. Register it in `.claude-plugin/marketplace.json` by adding an entry to the `plugins` array
4. Bump the marketplace `version` (e.g. `1.0.0` → `1.1.0`)
5. Commit and push — all your machines pick it up on next sync

### Minimum plugin structure

```
my-new-plugin/
├── .claude-plugin/
│   └── plugin.json          # name, version, description, author, keywords
├── README.md                # what the plugin does and how to use it
├── commands/                # optional: slash commands (/my-command)
│   └── my-command.md
└── skills/                  # optional: skills that auto-load from context
    └── my-skill/
        └── SKILL.md
```

### plugin.json template

```json
{
  "name": "my-new-plugin",
  "version": "0.1.0",
  "description": "One-line description.",
  "author": { "name": "Drew" },
  "keywords": ["keyword1", "keyword2"]
}
```

### marketplace.json — add one entry per plugin

```json
{
  "name": "drew-personal-plugins",
  "version": "1.1.0",
  "description": "Drew's personal Claude Cowork plugins",
  "owner": { "name": "Drew" },
  "plugins": [
    { "name": "resume-tailor",      "version": "0.1.0", "source": "./resume-tailor"      },
    { "name": "gdrive-file-reader", "version": "0.1.0", "source": "./gdrive-file-reader" },
    { "name": "my-new-plugin",      "version": "0.1.0", "source": "./my-new-plugin"      }
  ]
}
```

## One-Time Setup on a New Machine

1. In Cowork, open **Plugins → Add Marketplace**
2. Choose **GitHub** as the source
3. Enter your repo: `mrdrewvo/my-claude-plugins`
4. All plugins in this repo will appear and can be installed with one click

## Repo Structure

```
my-claude-plugins/
├── .claude-plugin/
│   └── marketplace.json          # marketplace registry — update when adding plugins
├── resume-tailor/                # plugin 1
│   ├── .claude-plugin/
│   │   └── plugin.json
│   ├── README.md
│   ├── commands/
│   │   ├── tailor-resume.md
│   │   └── update-profile.md
│   └── skills/
│       └── resume-expert/
│           ├── SKILL.md
│           └── references/
│               ├── ats-optimization.md
│               └── jd-analysis.md
├── gdrive-file-reader/           # plugin 2
│   ├── .claude-plugin/
│   │   └── plugin.json
│   ├── README.md
│   ├── commands/
│   └── skills/
│       └── gdrive-file-reader/
│           └── SKILL.md
└── [future-plugin]/              # drop new plugins here, register in marketplace.json
```
