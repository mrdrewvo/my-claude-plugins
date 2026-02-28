# Resume Tailor

Tailor your resume to any job posting — ATS-optimized, recruiter-ready, and tuned to what hiring managers actually want.

## What it does

This plugin helps you win the resume game at every layer: passing automated ATS filters, hooking recruiters in the first 6 seconds, and convincing hiring managers you're the obvious choice. It connects to your Google Drive to pull existing resumes, maintains a living vault of your accomplishments, researches target companies, and collaborates with you to produce polished output files.

## Components

| Component | Name | Purpose |
|-----------|------|---------|
| Skill | `resume-expert` | Deep expertise in ATS optimization, JD analysis, resume strategy, and company research. Loads automatically when resume tasks are detected. |
| Command | `/tailor-resume` | Full tailoring workflow: ingest a JD, research the company, map your experience, collaborate on the draft, output .md, .docx, and .pdf files. |
| Command | `/update-profile` | Scan your Google Drive resumes and build/update your experience vault — a structured repository of every role, accomplishment, and skill. |

## Getting Started

### Step 1: Build your experience vault

Run `/update-profile` to scan your existing Google Drive resumes and build your vault. This takes 2–3 minutes the first time and creates an `experience-vault.md` file in your connected folder.

You can also add individual updates anytime:
```
/update-profile Just closed a $3.2M enterprise deal at Acme Corp — largest in company history
```

### Step 2: Tailor a resume to a job

Run `/tailor-resume` with a job posting URL or paste the JD directly:

```
/tailor-resume https://jobs.stripe.com/jobs/123456
```

Or just run `/tailor-resume` and paste the job description when prompted.

The command will:
1. Parse the job description and extract keywords
2. Research the company online
3. Share a Job Intel Report with you for alignment
4. Write a tailored resume
5. Collaborate with you on review
6. Output `.md`, `.docx`, and `.pdf` files to your folder

## Output Files

Each tailoring session produces three files in your connected folder:
- `[Company]-[Role]-Resume.md` — Markdown version
- `[Company]-[Role]-Resume.docx` — ATS-safe Word document (**submit this to ATS systems**)
- `[Company]-[Role]-Resume.pdf` — Clean PDF for email or direct upload

## Experience Vault

The vault (`experience-vault.md`) is your persistent career repository. It stores:
- Every role with accomplishments and metrics
- Skills, tools, and domain expertise
- An Accomplishment Bank of your strongest quantified bullets

Keep it fresh by running `/update-profile` after major career milestones or when you add new accomplishments.

## Requirements

- **Google Drive** connected (to read your existing resumes and experience vault)
- **[gdrive-universal-reader](../gdrive-universal-reader/)** plugin installed (handles .pdf, .docx, and .md files that the native Drive connector can't read)
- **docx and pdf skills** installed (to generate Word and PDF output files)
- Your connected folder selected in Cowork (for vault and output storage)
