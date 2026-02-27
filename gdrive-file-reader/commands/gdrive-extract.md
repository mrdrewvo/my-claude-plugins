---
description: Extract specific information from a Google Drive file
allowed-tools: mcp__c1fc4002-5f49-5f9d-a4e5-93c4ef5d6a75__google_drive_search, mcp__c1fc4002-5f49-5f9d-a4e5-93c4ef5d6a75__google_drive_fetch
argument-hint: [filename] [what to extract]
---

The user wants to extract specific content from a Google Drive file.
Their request: $ARGUMENTS

Parse the arguments to identify:
1. The file they're referring to (name, partial name, or description)
2. What they want to extract (action items, dates, names, tables, key figures,
   a specific section, etc.)

If either piece is missing, ask one focused clarifying question.

Then:

1. Search for the file with `google_drive_search` using the filename or description.
   Confirm with the user if multiple results come back.

2. Fetch the file content with `google_drive_fetch`.

3. Extract exactly what the user asked for:
   - **Action items / tasks**: pull out anything that sounds like a to-do, decision,
     or commitment. Present as a clean list.
   - **Dates / deadlines**: find all temporal references. Present in chronological order.
   - **Names / people**: extract all named individuals and their roles or context.
   - **Key numbers / figures**: financial amounts, percentages, metrics.
   - **A specific section**: find the section by heading or keyword and return it.
   - **Tables / structured data**: reconstruct the table as clearly as possible.
   - **Summary / TL;DR**: synthesize into 3-5 bullet points covering the key substance.

4. If the content is too sparse to extract what they need (e.g., scanned PDF),
   explain clearly and offer the Drive URL.

Present extracted content cleanly. Don't pad with unnecessary preamble.
