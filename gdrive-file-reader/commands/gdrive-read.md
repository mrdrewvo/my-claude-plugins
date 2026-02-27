---
description: Read a .docx, .pdf, or .md file from Google Drive
allowed-tools: mcp__c1fc4002-5f49-5f9d-a4e5-93c4ef5d6a75__google_drive_search, mcp__c1fc4002-5f49-5f9d-a4e5-93c4ef5d6a75__google_drive_fetch
argument-hint: [filename or description]
---

The user wants to read a file from Google Drive. The file reference is: $ARGUMENTS

Do the following:

1. Use `google_drive_search` to find the file. If the user gave a filename, search
   by name. If they gave a description or partial title, use fullText search.
   Prioritize .docx, .pdf, and .md file types.

2. If multiple results come back, briefly list them (name + type + last modified)
   and ask the user to confirm which one before fetching.

3. Use `google_drive_fetch` with the confirmed file ID to retrieve the content.

4. Present the content in a way that matches what the user needs:
   - If they just said "read" or "open" with no further context: give a concise
     summary of the document, then offer to answer specific questions or go deeper.
   - If they said "summarize": give a structured summary with key points.
   - If they said "extract [something]": find and pull out that specific information.

5. If the content is empty or unreadable, explain why briefly (e.g., scanned PDF,
   complex formatting) and offer the Drive URL so they can open it directly.

Be helpful and direct. Don't over-explain the steps you're taking.
