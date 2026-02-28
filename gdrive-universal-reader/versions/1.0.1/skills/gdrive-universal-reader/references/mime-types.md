# Google Drive MIME Types & Search Syntax

## Supported file formats

| Format | MIME type string | Notes |
|--------|-----------------|-------|
| `.docx` | `application/vnd.openxmlformats-officedocument.wordprocessingml.document` | Microsoft Word (uploaded) |
| `.pdf` | `application/pdf` | PDF (uploaded) |
| `.md` | `text/markdown` | Markdown (uploaded) — try `text/plain` as fallback |
| `.txt` | `text/plain` | Plain text — also catches some .md files stored without explicit MIME type |
| Google Docs | `application/vnd.google-apps.document` | Native Google Doc |
| Google Sheets | `application/vnd.google-apps.spreadsheet` | Native Google Sheet |

## Search query examples

```
# Find all .docx files
mimeType = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'

# Find PDFs with "resume" in the name
name contains 'resume' and mimeType = 'application/pdf'

# Find any .md or .txt files
(mimeType = 'text/markdown' or mimeType = 'text/plain')

# Find .md files stored as plain text (common fallback)
name contains '.md' and mimeType = 'text/plain'

# Search by content keyword
fullText contains 'experience vault'

# Files modified in the last 30 days
modifiedTime > '2026-01-01'

# Files in a specific folder (use folder ID from a prior search)
'1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs' in parents

# Combine: find a docx resume by name
name contains 'Drew' and mimeType = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
```

## Notes on .md file detection

Google Drive doesn't always store `.md` files with the `text/markdown` MIME type.
Files uploaded directly sometimes get `text/plain` instead. If a markdown search
returns nothing, always retry with:
```
mimeType = 'text/plain' and name contains '.md'
```
