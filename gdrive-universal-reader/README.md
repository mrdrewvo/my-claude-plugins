# gdrive-universal-reader

Read any file from Google Drive — `.md`, `.pdf`, `.docx`, or native Google Docs.

The Google Drive MCP (`google_drive_fetch`) only reliably fetches Google Docs. This plugin works around that with an adaptive search strategy that locates files regardless of what format they're actually stored in.

## What it does

- Searches Drive with progressively broader queries until it finds your file
- Falls back from format-specific searches to name-only and folder-based searches
- Explicitly tries Google Docs as a fallback (common — files users think of as PDFs are often stored as Google Docs)
- On macOS with Google Drive for Desktop, reads non-.gdoc files directly from the local sync folder

## Skills

| Skill | Trigger |
|-------|---------|
| `gdrive-universal-reader` | "read my file from Drive", "get my resume from Google Drive", "pull up that markdown file", "grab my experience vault" |

## When to use

Use this from within any other plugin when you need to read a file from Google Drive and the standard `google_drive_fetch` isn't working or the file isn't a native Google Doc.
