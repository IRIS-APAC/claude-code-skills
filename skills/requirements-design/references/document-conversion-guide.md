# Document Conversion Guide

Convert documents (Word, PDF, Excel, PowerPoint) to Markdown for easier access and version control during requirements gathering.

---

## Quick Start

```bash
# Convert single file
python ~/.claude/skills/requirements-design/scripts/convert-docs-to-md.py \
  --file requirements.docx

# Convert entire folder
python ~/.claude/skills/requirements-design/scripts/convert-docs-to-md.py \
  --folder ./docs/Reference/Original/ \
  --output ./docs/Reference/

# Recursive folder conversion
python ~/.claude/skills/requirements-design/scripts/convert-docs-to-md.py \
  --folder ./docs/ \
  --output ./docs/Markdown/ \
  --recursive
```

---

## Prerequisites

### Install Pandoc (Recommended - handles most formats)

**Linux:**
```bash
sudo apt install pandoc
```

**macOS:**
```bash
brew install pandoc
```

**Windows:**
- Download: https://pandoc.org/installing.html
- Or via Chocolatey: `choco install pandoc`

### Optional Tools

**For PDFs (without pandoc):**
```bash
# Linux
sudo apt install poppler-utils

# macOS
brew install poppler
```

**For Excel files:**
```bash
pip install openpyxl
```

**For PowerPoint (without pandoc):**
```bash
pip install python-pptx
```

---

## Supported Formats

Check supported formats:
```bash
python convert-docs-to-md.py --supported-formats
```

| Format | Description | Tool Required |
|--------|-------------|---------------|
| `.docx` | Word Document | pandoc |
| `.doc` | Word (old) | pandoc |
| `.pdf` | PDF Document | pandoc or pdftotext |
| `.xlsx` | Excel Spreadsheet | openpyxl |
| `.xls` | Excel (old) | openpyxl |
| `.pptx` | PowerPoint | pandoc or python-pptx |
| `.ppt` | PowerPoint (old) | pandoc or python-pptx |
| `.odt` | OpenDocument | pandoc |
| `.rtf` | Rich Text Format | pandoc |
| `.html` | HTML Document | pandoc |
| `.vtt` | WebVTT Video Transcript | Built-in parser |

---

## When to Extract Images

**Decision tree for handling images:**

### ✅ Use --extract-images when:
- Document has **important diagrams** that explain concepts (architecture, flowcharts)
- **Screenshots** that show UI/UX requirements
- **Charts/graphs** with data you'll reference
- Images are **essential to understanding** the content

**Example:**
```bash
# Architecture doc with system diagrams
python convert-docs-to-md.py --file architecture.docx --extract-images
```

### ⏭️ Skip conversion (keep original) when:
- Document is **mostly diagrams** (>70% visual content)
- Complex **PowerPoint presentations** with visual layouts
- PDFs with **infographics** or complex layouts
- **Annotated screenshots** or mockups

**Example:**
```markdown
# Just reference it in your requirements
See [UI Mockups](Original/mockups.pptx) for screen designs
See [Process Map](Original/process-flow.pdf) for detailed workflow
```

### 📝 Convert without images (default) when:
- Document is **mostly text** (requirements, specifications)
- Images are **decorative** or not critical
- **Data tables** (images of tables → convert to markdown tables instead)
- Want to **keep git repo small**

**Example:**
```bash
# Requirements doc - mostly text
python convert-docs-to-md.py --file requirements.docx
# Adds note in markdown: "Images omitted - see original for diagrams"
```

**Quick rule:** If you need the images to understand the text → use `--extract-images`. If images are optional → skip them.

---

## Usage Examples

### Convert Single File

```bash
# Convert to same directory
python convert-docs-to-md.py --file requirements.docx

# Specify output location
python convert-docs-to-md.py \
  --file requirements.docx \
  --output ./docs/requirements.md
```

### Convert Folder

```bash
# Convert all supported files in folder
python convert-docs-to-md.py \
  --folder ./docs/Reference/Original/ \
  --output ./docs/Reference/

# Recursive (include subfolders)
python convert-docs-to-md.py \
  --folder ./docs/ \
  --output ./docs/Markdown/ \
  --recursive
```

### Advanced Options

```bash
# Overwrite existing .md files (default: skip)
python convert-docs-to-md.py --folder ./docs/ --overwrite

# Extract images to separate folder
python convert-docs-to-md.py --file document.docx --extract-images

# Delete original after conversion
python convert-docs-to-md.py --file old-doc.docx --delete-original

# Quiet mode (only show errors)
python convert-docs-to-md.py --folder ./docs/ --quiet
```

---

## Workflow Integration

### Typical Requirements Gathering Workflow

```bash
# 1. Download from SharePoint (or user provides files)
python sharepoint-access.py \
  --url "<sharepoint-url>" \
  --action download \
  --output ./docs/Reference/Original/

# 2. Convert to Markdown
python convert-docs-to-md.py \
  --folder ./docs/Reference/Original/ \
  --output ./docs/Reference/

# 3. Now Claude can easily read and reference the markdown files
```

### Organize Downloaded Docs

```
docs/
├── Reference/
│   ├── Original/              # Keep originals here (don't commit to git)
│   │   ├── requirements.docx
│   │   ├── process-map.pdf
│   │   └── data-dictionary.xlsx
│   ├── requirements.md        # Converted markdown (commit to git)
│   ├── process-map.md
│   └── data-dictionary.md
└── Design/                    # New requirements you create
    ├── constraints.md
    ├── requirements.md
    └── architecture.md
```

### Reference in New Requirements

After conversion, reference the markdown in your new requirements:

```markdown
## References

See existing documentation:
- [Previous Requirements](../Reference/requirements.md) - Converted from SharePoint
- [Process Mapping](../Reference/process-map.md) - Current workflow
- [Data Dictionary](../Reference/data-dictionary.md) - Existing data structures
```

---

## Format-Specific Notes

### Word Documents (.docx)

**Best conversion quality** - preserves:
- Headings (converted to `#` markdown)
- Lists (bullet and numbered)
- Tables (converted to markdown tables)
- Bold/italic formatting
- Links

**Lost in conversion:**
- Complex formatting (colors, fonts)
- Page layout
- Comments/track changes

### PDF Documents (.pdf)

**Quality varies** depending on PDF type:
- ✅ **Good**: Text-based PDFs (created from Word, etc.)
- ⚠️ **Limited**: Scanned PDFs (OCR text only)
- ❌ **Poor**: Image-only PDFs (no text extraction)

**Tip**: If PDF conversion quality is poor, convert original source document (e.g., .docx) instead.

### Excel Spreadsheets (.xlsx)

**Converts to markdown tables** - each sheet becomes:
```markdown
## Sheet Name

| Column 1 | Column 2 | Column 3 |
| --- | --- | --- |
| Data 1 | Data 2 | Data 3 |
```

**Lost in conversion:**
- Formulas (converts to values only)
- Formatting (colors, borders)
- Charts/graphs
- Multiple merged cells may look odd

**Tip**: For complex Excel files, consider exporting specific sheets to CSV first.

### PowerPoint Presentations (.pptx)

**Extracts slide text** - creates:
```markdown
## Slide 1

Title text

Bullet points
- Point 1
- Point 2

---

## Slide 2
...
```

**Lost in conversion:**
- Images/diagrams (use --extract-images to save separately)
- Slide layouts
- Animations
- Speaker notes (may be included depending on tool)

**Tip**: For diagram-heavy presentations, screenshot key slides and reference separately.

### Video Transcripts (.vtt)

**Converts WebVTT format to readable markdown** - creates:
```markdown
# Meeting Recording

*Converted from WebVTT video transcript*

---

**[00:05]** Welcome to the requirements review meeting.

**[00:08]** Today we'll discuss the livestock allocation system.

**[00:15]** The main goal is to optimize livestock assignment based on customer requirements.

**[01:30]** Key constraints include delivery schedules and animal welfare standards.
```

**Features:**
- Preserves timestamps for reference
- Removes VTT metadata and cue numbers
- Consolidates text into readable paragraphs
- Simplified timestamp format (MM:SS or HH:MM:SS)

**Use Cases:**
- ✅ Teams meeting transcripts from SharePoint
- ✅ Recorded requirements sessions
- ✅ Client interview recordings
- ✅ Design review meetings

**Example workflow:**
```bash
# Download Teams recording folder from SharePoint
python sharepoint-access.py \
  --url "<meeting-folder-url>" \
  --action download \
  --output ./docs/Reference/Original/

# Convert transcript
python convert-docs-to-md.py \
  --file ./docs/Reference/Original/Meeting-Recording.vtt

# Result: Meeting-Recording.md with readable transcript
```

**Tip**: Meeting transcripts are valuable for capturing:
- Discussed requirements and constraints
- Client questions and clarifications
- Design decisions and rationale
- Action items and follow-ups

---

## Common Issues

### Issue: "Pandoc not installed"

**Solution:**
```bash
# Linux
sudo apt install pandoc

# macOS
brew install pandoc

# Windows
# Download from https://pandoc.org/installing.html
```

### Issue: Excel conversion fails - "openpyxl not installed"

**Solution:**
```bash
pip install openpyxl
```

### Issue: Conversion creates empty/garbled markdown

**Causes:**
- Corrupted source file
- Unsupported file format variant
- PDF is image-only (no text)

**Solutions:**
1. Try opening file in original application to verify it's not corrupted
2. For PDFs: Check if it's text-based (can you select text?)
3. Try converting with different tool (e.g., manual export to .txt)

### Issue: Images not extracted

**Solution:**
Use `--extract-images` flag and ensure pandoc is installed:
```bash
python convert-docs-to-md.py --file document.docx --extract-images
```

Images will be saved to `./images/` folder.

---

## Tips & Best Practices

### 1. Keep Originals Separate

```bash
# Don't mix originals and conversions
docs/Reference/
├── Original/     # Binary files (.docx, .pdf) - exclude from git
└── *.md          # Converted markdown - commit to git
```

Add to `.gitignore`:
```
docs/Reference/Original/
```

### 2. Convert Only What You Need

Don't convert everything blindly:
- ✅ Convert requirements, specs, design docs
- ✅ Convert data dictionaries, glossaries
- ❌ Skip large presentations with mostly diagrams
- ❌ Skip complex Excel models (just reference key insights)

### 3. Review Converted Output

Always review markdown after conversion:
- Check tables rendered correctly
- Verify headings are at right level
- Fix any formatting issues manually
- Add clarifying notes where needed

### 4. Add Metadata

Add front matter to converted documents:
```markdown
---
source: requirements.docx
converted: 2026-02-01
location: SharePoint/Project/Requirements/
status: Reference only - do not modify
---

# Requirements Document
...
```

### 5. Batch Conversion

For many files, use folder conversion:
```bash
# Convert all at once
python convert-docs-to-md.py \
  --folder ./docs/Reference/Original/ \
  --output ./docs/Reference/ \
  --recursive
```

Then review and commit the markdown files.

---

## Integration with SharePoint Workflow

Combined workflow for SharePoint documents:

```bash
# 1. List SharePoint folder
python sharepoint-access.py --url "<url>" --action list

# 2. Download relevant docs
python sharepoint-access.py \
  --url "<folder-url>" \
  --action download \
  --output ./docs/Reference/Original/

# 3. Convert to markdown
python convert-docs-to-md.py \
  --folder ./docs/Reference/Original/ \
  --output ./docs/Reference/

# 4. Review markdown files
ls -lh docs/Reference/*.md

# 5. Add to git (markdown only, not originals)
git add docs/Reference/*.md
```

---

## Troubleshooting Checklist

- [ ] Pandoc installed? (`pandoc --version`)
- [ ] File format supported? (`python convert-docs-to-md.py --supported-formats`)
- [ ] File not corrupted? (Can open in original app?)
- [ ] For Excel: `openpyxl` installed? (`pip install openpyxl`)
- [ ] For PowerPoint: `python-pptx` installed? (if not using pandoc)
- [ ] Output folder writable?
- [ ] Using `--overwrite` if needed?

---

## Further Reading

- [Pandoc User Guide](https://pandoc.org/MANUAL.html)
- [Markdown Guide](https://www.markdownguide.org/)
- [openpyxl Documentation](https://openpyxl.readthedocs.io/)
