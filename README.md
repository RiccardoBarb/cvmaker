# CV Builder

A minimal local CV build system using a LaTeX template and a YAML data file.
Edit your data in `template.yml`, run one command, get a PDF.

## Files

| File                 | Description                                                   |
|----------------------|---------------------------------------------------------------|
| `template.yaml`      | Your CV data (the only file you need to edit)                 |
| `template.tex`       | LaTeX template with `<<PLACEHOLDERS>>`                        |
| `fortysecondscv.cls` | LaTeX class file                                              |
| `cvmake.py`          | Fills `template.tex` with data from `template.yml` → `cv.tex` |
| `cvbuild.sh`         | One-command build script                                      |

## Requirements

### LaTeX
Install BasicTeX via Homebrew:
```bash
brew install --cask basictex
```

Then install required packages:
```bash
sudo tlmgr update --self
sudo tlmgr install latexmk textpos clearsans fontaxes
```

### Python
Python and PyYAML:
```bash
pip install pyyaml
```

## Usage

```bash
./cvbuild.sh
```

This will:
1. Run `cvmake.py` to inject `template.yaml` data into `template.tex` → `cv.tex`
2. Compile `cv.tex` to PDF via `latexmk`
3. Move `cv.pdf` to the project root
4. Clean up all auxiliary files

## Editing your CV

All content lives in `cv.yaml`. The structure is:

```yaml
personal:       # name, role, phone, email, linkedin, github
technical_skills:
  tags:         # chip labels shown in sidebar
  tools:        # category + items lines
transferable_skills:  # name + description blocks
experience:     # list of companies, each with roles and highlights
education:      # list of degrees
```

Do not edit `cv.tex` directly — it is overwritten on every build.