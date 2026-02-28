---
name: gdrive-universal-reader
description: >
  Read any file stored in Google Drive — .md, .pdf, .docx, or native Google Docs.
  Use this skill whenever a user or another skill needs to access Drive files,
  especially non-.gdoc formats that the Google Drive MCP can't natively fetch.
  Invoke when someone says "read my file from Drive", "get my resume from Google
  Drive", "pull up that markdown file", "grab my experience vault", or references
  any Drive file by name or type. Also invoke this from within other skills (like
  resume-tailor) when the workflow requires reading .md, .pdf, or .docx files
  stored in Google Drive — the standard google_drive_fetch MCP call will fail for
  these types. Use it proactively whenever Drive file access is needed and the
  file is not a native Google Doc.
---

# Google Drive Universal File Reader

The Google Drive MCP (`google_drive_fetch`) works reliably for Google Docs (.gdoc).
For uploaded file types (.md, .pdf, .docx), it either fails or returns empty.
This skill provides an adaptive search strategy that locates files regardless of
what format they're actually stored in — because users often don't know whether
their file is a .docx, .gdoc, or .pdf.

**Key insight**: When a file isn't found in the format you searched for, don't stop.
The file likely exists in a different format (e.g., what a user calls "my resume PDF"
may actually be stored as a Google Doc). Always escalate to broader searches before
concluding the file doesn't exist.

---

## Step 1: Search Drive with increasing breadth

Work through these queries in order, stopping when you find the file:

### 1a. Target MIME type + name (specific)
Start with the format the user mentioned:

| Format | MIME type |
|--------|-----------|
| .docx  | `application/vnd.openxmlformats-officedocument.wordprocessingml.document` |
| .pdf   | `application/pdf` |
| .md    | `text/markdown` — if no results, retry with `text/plain` and name contains `.md` |
| .gdoc  | `application/vnd.google-apps.document` |

```
name contains 'resume' and mimeType = 'application/pdf'
```

### 1b. Name only, no MIME filter (broader)
If 1a returns nothing, drop the MIME type constraint:
```
name contains 'resume'
```
This catches files stored in a different format than expected.

### 1c. Known folder, no format filter (folder-based)
If you know or can find the folder name, search within it without any MIME constraint:
```
'folder-id' in parents
```
To find the folder ID first:
```
name = 'Drew Resumes' and mimeType = 'application/vnd.google-apps.folder'
```
Then use that ID to list the folder contents.

### 1d. Google Doc variant (always try this if no file found yet)
Files users think of as .pdf or .docx are frequently stored as Google Docs.
Search explicitly for a Google Doc version:
```
name contains 'resume' and mimeType = 'application/vnd.google-apps.document'
```

### 1e. Broad content search (last resort)
If name is ambiguous, try a fullText search:
```
fullText contains 'keyword from file'
```

**If none of the above find the file**, the file likely doesn't exist in Drive yet.
Report what you searched and suggest the user upload it.

**Critical**: Empty results from a MIME-specific search do NOT mean the Drive
connector is broken. The connector is working — the file just isn't in that format.
Always try broader searches before concluding there's a connectivity issue.

---

## Step 2: Retrieve the content

### Google Docs (.gdoc)
Call `google_drive_fetch` with the document ID. This works reliably.

### Non-.gdoc files (search found a .pdf, .docx, or .md)
Try `google_drive_fetch` first — occasionally it works for binary files.
If it returns empty or an error, proceed to the local filesystem.

### Local filesystem fallback (macOS + Google Drive for Desktop only)

This fallback only works when running on the user's Mac with Google Drive for
Desktop installed and synced. It will NOT work in a Linux VM environment.

Check if the sync folder exists:
```bash
ls ~/Library/CloudStorage/ 2>/dev/null || echo "not found"
```

If found, the base path is:
```
~/Library/CloudStorage/GoogleDrive-[email]/My Drive/
```

Fallback paths to try in order:
```bash
~/Library/CloudStorage/GoogleDrive-*/My\ Drive/
~/Google\ Drive/
```

Once you have the base path, locate the file:
```bash
find ~/Library/CloudStorage/ -name "filename.ext" 2>/dev/null
```

**Reading by file type:**

- **.md files** — use the `Read` tool or `cat`. Treat as plain Markdown.
- **.pdf files** — use `mcp__Desktop_Commander__read_file` with the local path.
- **.docx files** — use `mcp__Desktop_Commander__read_file` with the local path.

---

## Step 3: Handle failures gracefully

| Situation | What to do |
|-----------|------------|
| Target MIME search returned nothing | Try broader searches (1b → 1c → 1d) before giving up |
| Empty results from any Drive search | **Not** a connectivity failure — try a different query |
| `google_drive_fetch` returns empty for non-.gdoc | Expected — try local filesystem |
| Local sync folder not found | Environment may not be macOS with GDrive Desktop — offer Drive web URL |
| File not found in Drive at all | Ask if the file has been uploaded or if the name might differ |
| PDF is a scanned image (no extractable text) | Tell the user, suggest Drive's built-in OCR |
| Drive MCP genuinely not connected | "Your Google Drive connector isn't connected. Add it in Cowork's connector settings." — only say this if ALL queries fail with a connection error, not just empty results |

---

## Step 4: Deliver what the user needs

Once you have the content, focus on the actual task:
- Summarize, extract key points, answer questions, compare — don't dump raw content
  unless they asked for it
- Tell the user what format the file was actually found in if it differed from what
  they requested (e.g., "Your resume is stored as a Google Doc, not a .pdf")
- For long files, summarize by default and offer to go deeper on specific sections

## Multi-file requests

Run Drive searches in parallel where possible. Synthesize results together rather
than presenting files one at a time.

---

## Reference files

See `references/mime-types.md` for extended MIME type reference and search syntax examples.
