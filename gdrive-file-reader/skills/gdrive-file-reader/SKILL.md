---
name: gdrive-file-reader
description: >
  This skill should be used whenever the user wants to read, open, access, summarize,
  extract, or work with a .docx, .pdf, or .md file stored in Google Drive. Use this
  skill when the user says things like "read my doc from Drive", "open the PDF in my
  Drive", "get the file from Google Drive", "pull up that markdown file", or references
  a file by name that might be in their Drive. Also use this when the user wants to
  search Google Drive for a specific file type, ask questions about a Drive document,
  compare two Drive files, or convert Drive file content into another format.
version: 0.1.0
---

# Google Drive File Reader

Handle .docx, .pdf, and .md files stored in Google Drive — search, read, extract,
summarize, and work with their content as naturally as any local file.

## How Google Drive file access works

Two MCP tools handle all Drive interactions:

- **`google_drive_search`** — find files by name, content, or type; returns metadata
  including the file ID, name, MIME type, and web URL
- **`google_drive_fetch`** — retrieve the content of one or more files by their IDs

The `google_drive_fetch` tool works for Google-native formats (Docs, Sheets, Slides)
and also for uploaded files including plain text, Markdown, and in many cases extracted
text from PDF and Word documents. Always attempt the fetch — fall back gracefully if
the content comes back empty or binary.

## Workflow for any file request

### Step 1: Find the file

Use `google_drive_search` to locate the file. Construct the search query based on
what the user gave you:

- Filename or partial name → `name contains 'filename'`
- File type filter → use MIME type (see table below)
- Content search → `fullText contains 'keyword'`
- Combined → `name contains 'Q4 report' and mimeType = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'`

**MIME types for the supported formats:**

| Format | MIME type |
|--------|-----------|
| .docx  | `application/vnd.openxmlformats-officedocument.wordprocessingml.document` |
| .pdf   | `application/pdf` |
| .md    | `text/markdown` or `text/plain` |

If you get multiple results, surface them briefly and ask the user to confirm which
one they want before fetching.

### Step 2: Fetch the content

Call `google_drive_fetch` with the document ID(s) from the search results.

- If content comes back: proceed to Step 3.
- If content is empty or unreadable (common with binary-heavy PDFs or complex .docx
  with embedded images): tell the user clearly, then offer the `webViewLink` URL so
  they can open it directly in their browser. Don't leave them stuck.

### Step 3: Process by file type

**For .md files:**
The content will be raw Markdown. Render it naturally in your response — respect
headers, lists, code blocks, etc. Treat it exactly like any other Markdown document.

**For .docx files:**
The returned content is typically extracted text with basic structure preserved.
Heading levels may be flattened. Tables may be linearized. Make clear if significant
formatting was lost, but still extract maximum useful content. If the user needs
the formatted version, offer to redirect them to the Drive URL.

**For .pdf files:**
Content extraction quality varies by PDF type:
- Text-based PDFs (born-digital): usually clean extracted text
- Scanned/image PDFs: often empty or garbled; tell the user this is a scan and
  suggest they view it in Drive or use Google Drive's built-in OCR feature
- Mixed: extract what's available, note any gaps

### Step 4: Respond to the user's actual request

Once you have the content, focus on what the user actually asked for:
- Summarize, extract key points, answer questions, compare documents, etc.
- Don't dump the raw file content unless they asked for it
- If the content is very long, summarize by default and offer to go deeper on
  specific sections

## Handling ambiguous file references

If the user mentions a file without enough detail to find it (e.g., "the report" or
"my notes"), ask one targeted clarifying question: the filename, approximate date, or
a few words from the content. Don't ask for the full path — users rarely know it.

## Multi-file requests

For requests involving multiple files (e.g., "compare these two docs"), run the
searches and fetches in parallel. Synthesize the results together rather than
presenting them one at a time.

## Error handling

| Situation | What to do |
|-----------|------------|
| File not found in Drive | Tell the user, ask if the name might be slightly different |
| Fetch returns empty content | Offer the Drive web URL as a fallback |
| Too many search results (5+) | Show the top results with name/date and ask for confirmation |
| Drive MCP not connected | Tell the user: "It looks like your Google Drive isn't connected. You can connect it in Cowork's connector settings." |

## Reference files

See `references/mime-types.md` for a full list of Drive MIME types and their
`google_drive_search` query syntax.
