# Shell Guide for the Team

> **See also:** [Conventions for reproducible, schema-validated pipelines (CultureBotAI/KG-Microbe-search#8)](https://github.com/CultureBotAI/KG-Microbe-search/issues/8) — the broader best practices reference for all CultureBotAI repos.

This guide covers how to open a terminal, verify your tools are working, and use basic shell commands for data detective work. It applies to all CultureBotAI repos, not just auto-term-catalog.

---

## Prerequisites check

Before anything else, open a terminal (see [How to open a terminal](#how-to-open-a-terminal) below if you're not sure how) and run these three commands:

```bash
git --version
python --version
grep --version
```

You should see version numbers for all three. If any of them gives you an error like "command not found," see the troubleshooting section below.

| Command | Expected output | If it fails |
|---|---|---|
| `git --version` | `git version 2.x.x` | Install [Git for Windows](https://gitforwindows.org/) (Windows) or `xcode-select --install` (macOS) |
| `python --version` | `Python 3.x.x` | Try `python3 --version` instead. If that works, use `python3` everywhere this guide says `python`. |
| `grep --version` | `grep (GNU grep) 3.x` or `grep (BSD grep)` | On Windows, this means Git is not on your PATH — see [Windows troubleshooting](#windows-if-grep-is-not-found) |

---

## Terminal vs. shell: what's the difference?

These words get used interchangeably but they mean different things:

- **Terminal** (or "terminal emulator") = the **window/app** you type in. It draws text on your screen. That's all it does.
- **Shell** = the **program running inside** that window that actually interprets your commands.

Analogy: the terminal is like a web browser; the shell is like the website loaded inside it. The browser (terminal) is just a viewer — what matters is the site (shell) running in it.

When someone says "open a terminal," they mean: open a terminal app, which will automatically start a shell inside it.

---

## How to open a terminal

### macOS

Pick whichever method you prefer:

| Method | Steps |
|---|---|
| **Spotlight (fastest)** | Press **Cmd + Space**, type **Terminal**, press **Enter** |
| **Finder** | Open Finder → Go to **Applications** → **Utilities** → double-click **Terminal** |
| **Launchpad** | Click the Launchpad icon in the Dock (the grid of squares) → type **Terminal** in the search bar at the top → click it |
| **From VS Code** | Press **Ctrl + `** (the backtick key, top-left of keyboard below Esc) |

You'll see a prompt like `luke@MacBook ~ %`. This means you're in the **zsh** shell, which is the macOS default. All Unix commands (`grep`, `awk`, `head`, `wc`, `cd`, `ls`) work here immediately.

### Windows

On Windows, the default terminal app is **Windows Terminal** and the default shell inside it is **PowerShell**. PowerShell has its own command language that's different from Unix — but the good news is that **if you have Git installed, `grep` and other Unix tools already work in PowerShell too.** Git for Windows installs these tools and adds them to your system PATH.

**How to open Windows Terminal:**

| Method | Steps |
|---|---|
| **Start menu (fastest)** | Press the **Win** key (or click the Start button), type **Terminal**, press **Enter** |
| **Right-click Start** | Right-click the Start button (bottom-left corner) → choose **Terminal** |
| **From VS Code** | Press **Ctrl + `** (backtick) |
| **From File Explorer** | Open any folder in File Explorer → click the **address bar** at the top → type **`wt`** → press **Enter**. This opens Windows Terminal in that folder. |

When it opens, you'll see a prompt like `PS C:\Users\luke>`. The `PS` means you're in PowerShell.

**Important:** [GitHub Desktop](https://desktop.github.com/) is **not** the same as [Git for Windows](https://gitforwindows.org/). GitHub Desktop is a GUI app for commits and pushes — it installs its own private copy of Git that other programs cannot use. If you've only been using GitHub Desktop, you probably do not have `grep` on your PATH. You need to install [Git for Windows](https://gitforwindows.org/) separately (it's free and quick). During installation, keep the default options — especially the one that says **"Git from the command line and also from 3rd-party software"** — this is what puts `grep`, `awk`, `head`, etc. on your PATH.

### Verifying it worked (Windows)

After installing Git for Windows, close and reopen your terminal, then:

```
grep --version
```

If you see `grep (GNU grep) 3.x`, you're set. `grep`, `awk`, `head`, `wc`, and other Unix tools now work right here in PowerShell.

---

## Windows: if quoting gets weird

For simple commands, PowerShell works fine:

```powershell
grep "HGPBHO" merged-kg_nodes.tsv
grep -c "SAMN" auto_terms_by_microbe_with_kg_ids.csv
```

But PowerShell handles quotes differently from bash. If you try a command with single quotes and nested special characters, like this `awk` example, it may not work:

```bash
# This works in bash/zsh but may fail in PowerShell:
awk -F'\t' '$3 == ""' merged-kg_nodes.tsv
```

When that happens, switch to **Git Bash** — a proper bash shell that comes free with Git for Windows:

| Method | Steps |
|---|---|
| **Start menu** | Press **Win**, type **Git Bash**, press **Enter** |
| **From File Explorer** | Right-click inside any folder → **Open Git Bash here** (if this option appears) |
| **Inside Windows Terminal** | Click the **dropdown arrow** (small ▾ next to the **+** tab button) → select **Git Bash**. If it's not listed: open Settings → Profiles → Add new profile → set Command line to `C:\Program Files\Git\bin\bash.exe` |

Git Bash gives you a real bash shell where all commands and quoting work exactly like the examples you see in tutorials and on Stack Overflow.

**Our recommendation:** Use PowerShell for everyday work and simple `grep` commands. Switch to Git Bash when you need `awk` or when a command with quotes isn't working.

---

## Navigating to your files

When you first open a terminal, you're in your "home" directory. You need to `cd` (change directory) to where your project or data files are.

```bash
# See where you are right now
pwd

# List files in the current directory
ls

# Go to your Downloads folder
cd ~/Downloads

# Go to a specific project folder
cd ~/projects/auto-term-catalog

# Go up one directory
cd ..

# Go back to your home directory
cd ~
```

**macOS trick:** Type `cd ` (with a space after it), then **drag a folder from Finder** into the terminal window. It pastes the full path for you. Press Enter.

**Windows tricks:**
- In **File Explorer**, click the address bar, type **`wt`**, press Enter — opens a terminal already in that folder.
- In **Git Bash from Explorer**: right-click inside any folder → **Open Git Bash here**.
- In **PowerShell**, you can also drag-and-drop a folder from Explorer into the terminal to paste its path.

---

## grep basics

`grep` searches for text patterns in files. It's the most useful command for data detective work.

```bash
# Find a string in a file
grep "HGPBHO" merged-kg_nodes.tsv

# Count how many lines match
grep -c "HGPBHO" merged-kg_nodes.tsv

# Search case-insensitively
grep -i "hypothetical protein" merged-kg_nodes.tsv

# Show 2 lines of context around each match
grep -C 2 "HGPBHO" merged-kg_nodes.tsv

# Search all CSV files in the current directory
grep "AUTO:" *.csv

# Search recursively through all CSV files in all subdirectories
grep -r "AUTO:" . --include="*.csv"

# Invert: show lines that do NOT match
grep -v "UNKNOWN" auto_terms_by_microbe_with_kg_ids.csv
```

### Common patterns for our data

```bash
# Count how many rows mention a specific BioSample
grep -c "SAMN08731602" merged-kg_nodes.tsv

# Find ghost rows (kg_id present but no label)
grep ",,SAMN" auto_terms_by_microbe_with_kg_ids.csv

# Count AUTO terms in a YAML file
grep -c "AUTO:" chemical_utilization_anthropic_claude-sonnet_20251031_190413.yaml

# Find all files in the current directory that contain a string
grep -rl "HGPBHO" .
```

---

## Other useful commands

```bash
# Count lines in a file (= number of rows minus header)
wc -l merged-kg_nodes.tsv

# Show the first 5 lines (good for seeing headers)
head -5 merged-kg_nodes.tsv

# Show the last 5 lines
tail -5 merged-kg_nodes.tsv

# Show just the header line of a TSV
head -1 merged-kg_nodes.tsv
```

---

## Using Claude Code as a shell tutor

If you have access to [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview) (the `claude` CLI), you can run it directly in your terminal. It reads your files, runs commands for you, and — crucially — **shows you exactly what commands it runs**, so you learn the tools as you go.

```bash
# Install (requires Node.js 18+)
npm install -g @anthropic-ai/claude-code

# cd into your project and start it
cd ~/path/to/auto-term-catalog
claude
```

Then just ask questions in plain English:

```
> show me all rows in the CSV where kg_id is set but label is empty
> how many empty-name nodes are in merged-kg_nodes.tsv?
> what does this awk command do: awk -F'\t' '$3 == ""' file.tsv
```

Claude Code runs in the terminal directly — not inside an IDE. Compared to using an AI agent in an IDE panel (Cursor, VS Code Copilot Chat, etc.), this gives you:

- **Full screen width** for reading data files, diffs, and command output
- **Direct access to your shell** — you see real commands, not IDE abstractions
- **Less visual clutter** — just you, your files, and the AI
- **You learn shell skills organically** — every time it runs a `grep` or `awk` for you, you can see the command and try it yourself next time

If you don't have Node.js installed: download it from [nodejs.org](https://nodejs.org/) (pick the LTS version), install it, then run the `npm install` command above.

---

## Windows troubleshooting

### `grep` is not found

This means Git is not on your system PATH. Most likely you either:
- Only have **GitHub Desktop** installed (which bundles a private Git that doesn't go on PATH), or
- Installed Git for Windows but unchecked the PATH option during setup

**Fix:** Install (or reinstall) [Git for Windows](https://gitforwindows.org/). During installation, on the "Adjusting your PATH environment" screen, select **"Git from the command line and also from 3rd-party software"** (this is the default). After installation, close and reopen your terminal, then try `grep --version` again.

### `python` is not found but `python3` works (or vice versa)

On some systems, Python is installed as `python3` instead of `python`. You can either:
- Use `python3` everywhere instead of `python`, or
- On Windows, install Python from [python.org](https://www.python.org/downloads/) and check **"Add Python to PATH"** during installation

### `node` / `npm` is not found (for Claude Code)

Claude Code requires Node.js. Download the LTS version from [nodejs.org](https://nodejs.org/) and install it. The installer adds `node` and `npm` to your PATH automatically. Close and reopen your terminal after installing.
