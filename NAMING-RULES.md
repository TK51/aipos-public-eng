# NAMING-RULES.md  
**Version:** 1.0.0-RULES   
<!-- Last Updated: 2025-05-28 by Kay -->

---

## Purpose

This file defines the **non-negotiable naming rules** for AIPOS files.  
If your files don’t follow this — they don’t belong in the system. Period.

---

## Core Naming Rules

### 1. Use Hyphens Only

All file names must use hyphens `-`.  
Underscores `_` are banned system-wide.

| ✅ Valid                     | ❌ Invalid                    |
|-----------------------------|-------------------------------|
| `aipos-cfg-data-ops.txt`    | `aipos_cfg_data_ops.txt`      |
| `README.md`                 | `read_me.md`                  |
| `NAMING-RULES.md`           | `naming_rules.md`             |

---

### 2. Config Files Start With `aipos-cfg-`

Any file that controls runtime behavior **must** begin with:

```
aipos-cfg-
```

**Examples:**
- `aipos-cfg-base-cynical.txt`
- `aipos-cfg-gis-loader.txt`
- `aipos-cfg-output-neutral.txt`

---

### 3. Docs Don’t Use Prefix — But Must Be UPPERCASE

High-level docs (rules, templates, indices) use **UPPERCASE with hyphens**:

| File Role        | Valid Filename         |
|------------------|------------------------|
| Main Intro       | `README.md`            |
| Naming Rules     | `NAMING-RULES.md`      |
| Training Guide   | `TRAINING-GUIDE.md`    |

No prefix. No camelCase. No exceptions.

---

### 4. Filename Must Appear Inside The File

Top of every file must declare itself — for grep, trace, and human clarity.

```markdown
# aipos-cfg-base-cynical.txt
```

If filename ≠ header → it fails compliance.

---

## Accepted Extensions

| Type       | Extension | Use Case                |
|------------|-----------|-------------------------|
| Config     | `.txt`    | Runtime control logic   |
| Markdown   | `.md`     | Docs, rules, methods    |
| Archive    | `.zip`    | Multi-file sessions     |
| Data (opt) | `.json`   | Structured data (future)|

No `.docx`, `.rtf`, `.pdf`, or Google Drive exports.

---

## Naming Pattern Standard

```
aipos-cfg-[domain]-[purpose].txt
```

**Examples:**
- `aipos-cfg-data-automation.txt`
- `aipos-cfg-output-minimal.txt`
- `aipos-cfg-ui-neutral.txt`

**Docs:**
- `README.md`
- `NAMING-RULES.md`

---

## Violations to Kill On Sight

- Snake_case names  
- Missing filename in header  
- Generic junk like `cfg-session.txt`  
- Duplicate prefixes like `aipos-cfg-cfg.txt`  
- Files not in `.txt` or `.md` format  

---

## Philosophy

Structure ≠ polish.  
Naming ≠ vanity.  
This is **execution control** — no compromise allowed.

---

## Summary

If it’s runtime logic → `aipos-cfg-...txt`  
If it’s a doc → `ALLCAPS.md`  
Use hyphens. Declare names inside files. Reject fluff.

This is your **operational backbone**.

Break this — break your system.
