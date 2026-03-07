---
name: gdrive-universal-reader
description: >
  Read, write, or delete .md, .pdf, and .docx files. Use this skill whenever
  a user or another skill needs to access files of these types — whether they're
  stored in Google Drive or in the user's locally mounted folder. The Google Drive
  MCP can only natively fetch .gdoc files; this skill handles the adaptive search
  and format fallback for all other types. Invoke when someone says "read my file
  from Drive", "get this document from Google Drive", "pull up that markdown file",
  "save this as a PDF", "update this doc", "delete that file", or references
  any .md, .pdf, or .docx file by name or location. Use it proactively whenever
  file access, creation, or deletion is needed for these types.
---

# Google Drive Universal File Handler

Handles read, write, and delete operations for `.md`, `.pdf`, and `.docx` files.

**Read**: Supports files in Google Drive (via adaptive search + fallback) and in the user's locally mounted Cowork folder.

**Write/Delete**: The Google Drive MCP connector is read-only — no write or delete tools exist for Drive. All write and delete operations target the user's **locally mounted folder** only.

---

## Reading Files

### From Google Drive

The Google Drive MCP (`google_drive_fetch`) works reliably for Google Docs (.gdoc). For uploaded file types (.md, .pdf, .docx), it either fails or returns empty. Use the adaptive search strategy below.

**Key insight**: When a file isn't found in the format you searched for, don't stop. The file likely exists in a different format (e.g., what a user calls "my resume PDF" may actually be stored as a Google Doc). Always escalate to broader searches before concluding the file doesn't exist.

#### Step 1: Search Drive with increasing breadth

Work through these queries in order, stopping when you find the file:

**1a. Target MIME type + name (specific)**

| Format | MIME type |
|--------|-----------|
| .docx  | `application/vnd.openxmlformats-officedocument.wordprocessingml.document` |
| .pdf   | `application/pdf` |
| .md    | `text/markdown` — if no results, retry with `text/plain` and name contains `.md` |
| .gdoc  | `application/vnd.google-apps.document` |

**1b. Name only, no MIME filter (broader)**
Drop the MIME type constraint if 1a returns nothing — catches files stored in an unexpected format.

**1c. Known folder, no format filter**
If you know the folder name, find its ID first, then list its contents:
```
name = 'Folder Name' and mimeType = 'application/vnd.google-apps.folder'
```
Then: `'folder-id' in parents`

**1d. Google Doc variant**
Files users think of as .pdf or .docx are frequently stored as Google Docs. Search explicitly:
```
name contains 'filename' and mimeType = 'application/vnd.google-apps.document'
```

**1e. Broad content search (last resort)**
```
fullText contains 'keyword from file'
```

If none of the above find the file, report what you searched and suggest the user upload it.

**Critical**: Empty results from a MIME-specific search do NOT mean the Drive connector is broken. Always try broader searches before concluding there's a connectivity issue.

#### Step 2: Retrieve the content from Drive

**Google Docs (.gdoc)**: Call `google_drive_fetch` with the document ID. Works reliably.

**Non-.gdoc files (.pdf, .docx, .md)**: Try `google_drive_fetch` first — occasionally works. If it returns empty or errors, use the local filesystem fallback below.

#### Local filesystem fallback (macOS + Google Drive for Desktop only)

This fallback only works when running on the user's Mac with Google Drive for Desktop installed and synced. It will **not** work in a Linux VM (Cowork) environment.

```bash
ls ~/Library/CloudStorage/ 2>/dev/null || echo "not found"
```

Base path if found:
```
~/Library/CloudStorage/GoogleDrive-[email]/My Drive/
```

Locate the file:
```bash
find ~/Library/CloudStorage/ -name "filename.ext" 2>/dev/null
```

### From the Local Mounted Folder (Cowork)

In Cowork, the user's folder is mounted at `/sessions/{session-name}/mnt/`. The session name changes with every new session — never hardcode it. Discover it dynamically:

1. List `/sessions/` to find the current session name
2. Use Glob with `**/filename.ext` starting from `/sessions/{session-name}/mnt/`

**Reading by file type:**
- **.md** — use the `Read` tool
- **.pdf** — use `mcp__Desktop_Commander__read_file` or the `pdf` skill
- **.docx** — use `mcp__Desktop_Commander__read_file` or the `docx` skill

---

## Writing Files

All writes go to the user's locally mounted folder. The Google Drive connector is read-only.

**Discover the mounted folder path first** (see above — list `/sessions/`, construct the path).

| File type | How to write |
|-----------|--------------|
| `.md`     | Use the `Write` tool to create or overwrite. Use `Edit` for partial updates. |
| `.pdf`    | Use `mcp__Desktop_Commander__write_pdf` or invoke the `pdf` skill. |
| `.docx`   | Use `mcp__Desktop_Commander__write_file` (for new files) or invoke the `docx` skill. |

Always confirm the destination path with the user before writing if it's not clear from context.

---

## Deleting Files

All deletes target the user's locally mounted folder only.

```bash
rm /sessions/{session-name}/mnt/path/to/file.ext
```

If the delete fails with "Operation not permitted", use the `mcp__cowork__allow_cowork_file_delete` tool to request permission, then retry.

**Always confirm with the user before deleting.** State the full filename and path before proceeding.

---

## Failure Handling

| Situation | What to do |
|-----------|------------|
| Target MIME search returned nothing | Try broader searches (1b → 1c → 1d) |
| `google_drive_fetch` returns empty for non-.gdoc | Expected — try local filesystem fallback |
| Local sync folder not found | Environment may be Cowork (Linux VM) — check mounted folder instead |
| File not found anywhere | Ask if the file has been uploaded or if the name might differ |
| PDF is a scanned image (no extractable text) | Tell the user; suggest Drive's built-in OCR |
| Drive MCP not connected | Only say this if ALL queries fail with a connection error — not just empty results |
| Delete fails with permission error | Use `mcp__cowork__allow_cowork_file_delete` to request permission |

---

## Multi-file requests

Run Drive searches in parallel where possible. For writes or deletes across multiple files, confirm the full list with the user before proceeding.

---

## Reference files

See `references/mime-types.md` for extended MIME type reference and search syntax examples.
