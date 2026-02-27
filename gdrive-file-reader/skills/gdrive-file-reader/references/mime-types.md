# Google Drive MIME Types & Search Syntax

## Supported file formats for this plugin

| Format | MIME type string | Notes |
|--------|-----------------|-------|
| `.docx` | `application/vnd.openxmlformats-officedocument.wordprocessingml.document` | Microsoft Word (uploaded) |
| `.pdf` | `application/pdf` | PDF (uploaded) |
| `.md` | `text/markdown` | Markdown (uploaded) |
| `.txt` | `text/plain` | Plain text — also catches some .md files |
| Google Docs | `application/vnd.google-apps.document` | Native Google Doc (for reference) |

## Search query examples

```
# Find all .docx files
mimeType = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'

# Find PDFs with "Q4" in the name
name contains 'Q4' and mimeType = 'application/pdf'

# Find any .md or .txt files
(mimeType = 'text/markdown' or mimeType = 'text/plain')

# Search by content keyword
fullText contains 'budget forecast'

# Files modified in the last 30 days
modifiedTime > '2025-12-01'

# Files shared with me
sharedWithMe

# Combine: find a docx by name
name contains 'proposal' and mimeType = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
```

## Notes on .md file detection

Google Drive doesn't always store `.md` files with the `text/markdown` MIME type —
some are stored as `text/plain`. If a markdown search returns nothing, retry with
`text/plain` and filter by the `.md` extension in the filename:
`name contains '.md' and mimeType = 'text/plain'`
