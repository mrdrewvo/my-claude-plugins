# ATS Optimization Reference

Applicant Tracking Systems (ATS) are software tools that parse, rank, and filter resumes before a human ever sees them. An estimated 75% of resumes are rejected by ATS before reaching a recruiter. These rules ensure the user's resume passes the filter.

## How ATS Systems Work

1. **Parsing**: The ATS extracts text and attempts to categorize it into fields (name, contact, work history, education, skills)
2. **Keyword matching**: The system compares the resume against the job description, scoring for keyword presence and frequency
3. **Ranking**: Resumes are ranked by score; only top-ranked ones reach human reviewers
4. **Filtering**: Some systems apply hard filters (minimum years of experience, required credentials)

Different companies use different ATS systems (Workday, Greenhouse, Lever, iCIMS, Taleo, Jobvite, SmartRecruiters). Taleo and iCIMS are among the most aggressive parsers; format conservatively when targeting large enterprises.

## Formatting Rules

### Structure
- Use a single-column layout — two-column layouts break most parsers
- No tables — cells confuse parsing order
- No text boxes — content is often skipped entirely
- No headers or footers — text in these areas is frequently ignored
- No graphics, icons, logos, or decorative lines
- No embedded hyperlinks as primary content (URLs can be listed as plain text)

### Fonts and Sizing
- Body: 10–12pt minimum
- Headers/section names: 12–14pt
- Standard typefaces only: Calibri, Arial, Helvetica, Georgia, Times New Roman, Garamond
- Avoid: Fancy display fonts, custom downloaded fonts, icon fonts

### File Format
- Submit as **.docx** unless the application explicitly accepts or requires PDF
- .docx is the most reliably parsed format across all major ATS systems
- If PDF is required, export from Word (not Google Docs) for cleaner text encoding

### Section Headers
Use standard, recognizable section names:
- ✅ "Work Experience" or "Professional Experience" (not "My Journey" or "Career Highlights")
- ✅ "Education" (not "Degrees" or "Academic Background")
- ✅ "Skills" or "Technical Skills" (not "Toolkit" or "What I Know")
- ✅ "Summary" or "Professional Summary" (not "About Me")
- ✅ "Certifications" (not "Credentials" or "Certs")

## Keyword Strategy

### Exact Phrase Matching
Most ATS systems do exact or near-exact phrase matching. If the JD says "cross-functional collaboration," the resume should say "cross-functional collaboration" — not "worked with multiple teams."

**How to extract keywords from a JD:**
1. Paste the JD into a text analysis tool or manually scan
2. Identify: technical skills, tools/platforms, methodologies, domain terms, soft skills mentioned explicitly
3. Note frequency — terms appearing 2+ times are high priority
4. Look for role-specific jargon

### Keyword Placement Rules
- Use high-priority keywords in the Summary (highest weight), then in bullet points
- Don't stuff keywords — use them naturally within accomplishment statements
- Include both full names and abbreviations: "Search Engine Optimization (SEO)", "Machine Learning (ML)"
- Spell out acronyms once even if the JD uses only the abbreviation

### Skills Section
- List relevant tools, platforms, and technologies explicitly in a Skills section
- ATS systems often parse the Skills section separately with higher weight
- Format as a simple list or comma-separated items — no tables or columns
- Include certifications with their full official names

## Content Optimization

### Bullet Points
- Lead every bullet with a strong action verb (past tense for previous roles, present for current)
- Quantify wherever possible: %, $, headcount, time saved, revenue generated, volume handled
- Formula: **[Action verb] + [what you did] + [result/impact]**
  - ❌ "Responsible for managing a team"
  - ✅ "Led a 7-person engineering team to deliver a $2M platform migration 3 weeks ahead of schedule"

### Strong Action Verbs by Function
- Leadership: Led, Directed, Spearheaded, Championed, Orchestrated
- Building: Developed, Architected, Designed, Built, Launched, Established
- Improving: Streamlined, Optimized, Accelerated, Reduced, Improved, Transformed
- Analysis: Analyzed, Synthesized, Evaluated, Assessed, Modeled, Forecasted
- Collaboration: Partnered, Coordinated, Facilitated, Aligned, Influenced

### The Summary
The summary is the highest-weight section for both ATS and human readers. It should:
- Be 3–4 lines maximum
- Mirror the seniority and language of the JD
- Include the job title they're applying for (or close variation) naturally in the text
- Include 2–3 of the most important keywords
- Communicate unique value or specialization, not just years of experience

**Weak summary**: "Experienced marketing professional with 8 years of experience looking for new opportunities."
**Strong summary**: "Growth marketing leader with 8 years driving acquisition and retention for B2B SaaS companies. Known for building data-driven programs that reduce CAC while scaling pipeline — delivered 40% YoY growth at two consecutive Series B companies."

### Education
- Place education after Work Experience for candidates with 3+ years of experience
- Place education first for recent graduates or roles where credentials are the primary qualification (law, medicine, academia)
- Include: Degree, Field of Study, Institution, Graduation Year
- Omit GPA unless above 3.5 and within 5 years of graduation

## Common ATS Failure Modes

| Problem | Fix |
|---------|-----|
| Resume parsed as one block of text | Remove all tables, text boxes, and columns |
| Name not recognized | Place name on its own line at the top, not inside a header |
| Dates not parsed | Use consistent format: "Jan 2020 – Mar 2023" or "2020–2023" |
| Keywords missing | Add a Skills section and weave JD terms into bullets |
| Low score despite qualifications | Summary doesn't include key role terminology |
| PDF parsing failure | Re-submit as .docx |
