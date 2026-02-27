# Google Drive File Reader

Extends Cowork's Google Drive connector to fluently handle **.docx**, **.pdf**, and **.md** files — the formats Google Drive supports but its MCP tools don't natively surface well.

## What it does

The built-in Google Drive connector is great at reading Google Docs, but it often drops the ball on uploaded non-native files. This plugin fills that gap by giving Claude a complete workflow for finding, fetching, and processing those file types.

## Components

### Skill: `gdrive-file-reader`

Loads automatically when you ask Claude to read, open, search, or work with any Drive file that's a Word doc, PDF, or Markdown file. No slash command needed — just say the thing naturally:

- "Read my Q4 proposal from Drive"
- "Summarize the PDF John sent me last week"
- "Pull up that markdown spec from the product drive"
- "Compare the two contracts in my Drive folder"

### Commands

| Command | What it does |
|---------|-------------|
| `/gdrive-read [filename]` | Find and read a specific file; summarizes by default |
| `/gdrive-search [query]` | Search Drive for .docx, .pdf, or .md files matching a query |
| `/gdrive-extract [file] [what]` | Pull out specific content: action items, dates, key figures, a section |

## Setup

Requires the **Google Drive** connector to be connected in Cowork. If it's not connected, the plugin will tell you and you can set it up in Cowork's connector settings.

No additional environment variables or configuration needed.

## Usage examples

```
/gdrive-read Project Kickoff Notes.docx
/gdrive-search PDFs from last month
/gdrive-extract Q4 Review.pdf action items
```

Or just talk to Claude naturally — the skill triggers automatically on file-related requests.

## Limitations

- **Scanned PDFs** (image-only): text extraction won't work; Claude will offer the Drive URL as a fallback
- **Password-protected .docx**: can't be read via the MCP tools
- **Very large files**: content may be truncated; Claude will note when this happens
