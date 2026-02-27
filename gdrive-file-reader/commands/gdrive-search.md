---
description: Search Google Drive for .docx, .pdf, and .md files
allowed-tools: mcp__c1fc4002-5f49-5f9d-a4e5-93c4ef5d6a75__google_drive_search
argument-hint: [search query or file type]
---

The user wants to search their Google Drive for files. Their query is: $ARGUMENTS

Search strategy:

1. Parse the user's query to determine what to search for:
   - If they specified a file type (e.g., "PDFs", "Word docs", "markdown files"),
     filter by the appropriate MIME type.
   - If they gave a keyword or topic, use fullText search.
   - If they gave both, combine them.

   MIME types:
   - .docx → `application/vnd.openxmlformats-officedocument.wordprocessingml.document`
   - .pdf → `application/pdf`
   - .md → `text/markdown` (also try `text/plain` with name contains '.md')

2. Run the search with `google_drive_search`.

3. Present results as a clean list showing:
   - File name
   - File type (human-readable: "Word doc", "PDF", "Markdown")
   - Last modified date if available
   - A direct link if available

4. If there are more than 10 results, show the 10 most relevant and mention there
   are more.

5. After showing results, ask if they'd like to open or read any of them. If they
   say yes, fetch the file with `google_drive_fetch` and surface the content.

Keep the response clean and scannable.
