---
description: Tailor your resume to a specific job description
allowed-tools: Read, Write, Glob, WebFetch, WebSearch, mcp__c1fc4002-5f49-5f9d-a4e5-93c4ef5d6a75__google_drive_search, mcp__c1fc4002-5f49-5f9d-a4e5-93c4ef5d6a75__google_drive_fetch, Task
argument-hint: [job-description-url-or-paste-below]
---

You are running the `/tailor-resume` command. Your goal is to produce a tailored, ATS-optimized, and compelling resume for a specific job. Work through these phases carefully.

The user's argument (if provided) is: $ARGUMENTS

---

## Phase 1: Gather the Job Description

If $ARGUMENTS contains a URL, use WebFetch to retrieve the job description from that URL.

If $ARGUMENTS contains pasted text (not a URL), treat it as the job description directly.

If $ARGUMENTS is empty, ask the user: "Please paste the job description below, or share the URL to the posting."

Once you have the job description, confirm you've captured it by stating the job title and company name.

---

## Phase 2: Load the Experience Vault

Search for a file named `experience-vault.md` in the user's connected folder (look under /sessions/awesome-intelligent-edison/mnt/). Use Glob with pattern `**/experience-vault.md`.

If found, read it fully — this is the primary source of accomplishments and career history.

If not found, say: "I didn't find an experience vault yet. I'll work from your source resumes instead. You can build your vault anytime with `/update-profile`."

---

## Phase 3: Load Source Resumes from Google Drive

Search Google Drive for documents likely to be resumes. Use the google_drive_search tool with a query like:
`fullText contains 'resume' OR name contains 'resume' OR name contains 'CV'`

Fetch the top 2–3 results using google_drive_fetch. Extract all career history, accomplishments, skills, and job titles from the documents.

If no Google Drive connection is available, ask the user: "Do you have any resume files in your folder I can reference? If so, point me to the file name."

Consolidate all experience from the vault + source resumes into a working profile in your context.

---

## Phase 4: Research the Company

Using WebSearch, research the target company:
1. Search for the company name + "mission," "values," and recent news
2. Look for recent press releases, funding announcements, or product launches
3. Search for the company on Glassdoor or LinkedIn for culture signals

Synthesize what you find into a brief intel summary: what is this company focused on right now, what do they value, and what does success in this role likely look like beyond the JD?

---

## Phase 5: Analyze the Job Description

Apply the full JD analysis framework from the resume-expert skill:

1. Extract and categorize the top 10–15 keywords (Technical Skills, Domain Knowledge, Methodologies, Soft Skills)
2. Identify required vs. preferred qualifications
3. Read between the lines: what is this role really about? What signals does the language send about the team's situation and culture?
4. Map the user's experience to each requirement
5. Identify any gaps and determine how to handle them

Present a brief **Job Intel Report** to the user (5–8 bullets) covering:
- What this role is really about
- The top keywords to target
- Interesting company context
- Your recommended positioning angle
- Any gaps worth flagging

Ask: "Does this read right to you? Is there anything about your background or goals I should factor in before I start writing?"

Wait for the user's response before proceeding.

---

## Phase 6: Write the Tailored Resume

Using all gathered context, write a fully tailored resume:

### Structure (in order):
1. **Header** — Name, email, phone, LinkedIn URL, city/state (no full street address)
2. **Professional Summary** — 3–4 lines, tailored to this specific role. Include the target job title or close variant, 2–3 priority keywords, and a distinctive value statement. Mirror the JD's language and energy.
3. **Work Experience** — Ordered chronologically (most recent first). For each role: company name, title, dates (Month Year – Month Year), location (City, ST or Remote). 4–6 bullets per recent role, 2–3 for older roles. Lead every bullet with a strong action verb. Quantify impact. Order bullets within each role by relevance to THIS job (most relevant first, not just most impressive).
4. **Skills** — Single-column or simple comma list. Pull from keyword inventory. Include tools, platforms, methodologies, and domain expertise.
5. **Education** — Degree, field, institution, year. Place after Work Experience unless this is a role where credentials lead (academic, legal, medical).
6. **Certifications** (if applicable) — Official full names only.

### Quality Checks:
- Every bullet leads with an action verb
- At least 60% of bullets contain a quantified result
- Summary includes job title and top 2–3 keywords
- No tables, columns, text boxes, or fancy formatting
- All required qualifications addressed somewhere in the document
- Top 10 JD keywords appear at least once

---

## Phase 7: Collaborative Review

Present the full resume to the user.

Then ask targeted review questions:
- "Does the summary feel accurate to how you'd describe yourself?"
- "Are there any accomplishments I missed that would strengthen this?"
- "Any bullets you'd want to reframe or soften?"
- "Does the overall story make sense for this move?"

Incorporate feedback and revise as needed. Repeat until the user is satisfied.

---

## Phase 8: Output Files

Once the user approves the final resume, save three output files to the user's connected folder:

1. **Markdown version**: Save as `[Company]-[Role]-Resume.md` in the connected folder (e.g., `Stripe-ProductManager-Resume.md`)

2. **Word document (.docx)**: Use the docx skill to create a professionally formatted Word document with the same content. Save as `[Company]-[Role]-Resume.docx`. This is the ATS-safe submission format.

3. **PDF**: Use the pdf skill to produce a clean PDF version. Save as `[Company]-[Role]-Resume.pdf`.

Tell the user: "Your resume is ready in three formats. Submit the .docx to ATS systems, and the .pdf for email attachments or direct submissions where PDF is requested."

Also offer: "Would you like me to add the accomplishments used here to your experience vault?"
