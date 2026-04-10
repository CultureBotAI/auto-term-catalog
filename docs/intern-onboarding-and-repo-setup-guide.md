# Intern Onboarding and Repo Setup Guide

This guide covers two things:

1. How to install the local tooling needed to use Codex with an LBL account.
2. What Python and repository setup this repo should use so Codex can help productively.

Repository covered here:

- `CultureBotAI/auto-term-catalog`
- Local checkout example: `~/gitrepos/auto-term-catalog`

## Current repo state

As of April 10, 2026, this repo is very minimal:

- `README.md` is one sentence.
- There is no `pyproject.toml`.
- There is no pinned Python version.
- There is no lockfile.
- There are no tests.
- There is no CI.
- The main script is `src/process_terms/auto_terms_table.py`.
- That script has a hard-coded local file path pointing at one user's Downloads folder.

That means the intern can install Codex and open the repo today, but Codex will be much more useful after the repo has a basic Python project scaffold.

## Why this guide exists

This repo needs a repo-local guide because two separate things are true at once:

- The broader CultureBotAI onboarding materials already exist.
- This specific repo is not yet set up in a way that makes local, reproducible work easy for a new contributor.

This guide is therefore intended as a supplement to broader CultureBotAI onboarding, not a replacement for it.

## Why use Codex CLI here instead of only the web app, desktop app, or IDE plugin

For this repo, the CLI is the most useful starting point.

Why:

- It runs directly in the checked-out repository the contributor is already working in.
- It works naturally with shell commands, Git, local files, and data artifacts.
- It makes it easier to inspect project structure and run the exact commands that the repo depends on.
- It encourages contributors to stay close to the real execution environment instead of treating the repo like an abstract document browser.

Compared with other entry points:

- A web interface is useful for discussion and quick experiments, but it is less grounded in the local repo state.
- A desktop app can be convenient, but it is still one step removed from the shell-based workflow that this repo currently requires.
- An IDE plugin can be helpful after the basics are working, but it does not replace understanding how the repo is actually run, tested, and versioned.

For undergraduates especially, the CLI has a second benefit: it makes the relationship between prompts, files, commands, and Git history much more explicit.

## Why repo setup matters beyond this one intern

Good repo setup is not just about making one onboarding session smoother.

It is an investment in:

- our future selves
- the next student who joins
- collaborators reviewing or extending the work
- anyone trying to reproduce results after the original author has moved on

Without that setup, a repo quietly accumulates avoidable friction:

- hidden local assumptions
- hard-coded file paths
- undocumented dependencies
- one-machine-only workflows
- brittle scripts that no one wants to touch later

Undergraduates often optimize for getting the script to run once. That is understandable, but the repo needs to optimize for something broader: repeatable, inspectable work that other people can run, review, and improve.

That is why this guide pairs Codex onboarding with concrete repo-setup recommendations.

## Part 1: Install the local tools

### Step 1: Install Homebrew

Official Homebrew install command:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Official references:

- Homebrew homepage: https://brew.sh/
- Homebrew installation docs: https://docs.brew.sh/Installation.html

Notes:

- On Apple Silicon Macs, Homebrew installs under `/opt/homebrew`.
- On Intel Macs, it usually installs under `/usr/local`.
- The installer prints a command to add Homebrew to the shell environment. Do not skip that step.

Typical post-install step on Apple Silicon:

```bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

Verify:

```bash
brew --version
```

### Step 2: Install Node.js

Codex is distributed as an npm package, so the machine needs Node and npm.

Install with Homebrew:

```bash
brew install node
```

Verify:

```bash
node --version
npm --version
```

### Step 3: Install Git if needed

On many Macs, Git is already present. Check first:

```bash
git --version
```

If it is missing, install Xcode Command Line Tools:

```bash
xcode-select --install
```

### Step 4: Install Codex CLI

Install Codex globally with npm:

```bash
npm install -g @openai/codex
```

Official references:

- Codex CLI docs: https://developers.openai.com/codex/cli
- Codex package README: https://github.com/openai/codex

Verify:

```bash
codex --version
```

### Step 5: Sign in with ChatGPT using the LBL account

Start Codex:

```bash
codex
```

Then choose:

- `Sign in with ChatGPT`

Use the intern's Berkeley Lab email identity if that account has been provisioned in the Berkeley Lab ChatGPT workspace.

Official reference:

- https://help.openai.com/en/articles/11369540-codex-in-chatgpt

Important:

- An `@lbl.gov` email address by itself is not enough.
- The account must actually be enabled in the LBL ChatGPT Business / Enterprise / Edu workspace.
- Workspace admins may also control whether the user can access Codex.

If sign-in succeeds, the CLI should open a browser flow and then store local auth state for future sessions.

### Step 6: Confirm the intern is actually using subscription-backed access

After login:

```bash
codex
```

If it starts normally and does not ask for an API key, that is the desired path.

If the machine was previously configured with an API key, switch away from that:

```bash
codex logout
codex
```

Then sign in again with ChatGPT.

## Part 2: Clone and open the target repo

Clone:

```bash
cd ~/gitrepos
git clone git@github.com:CultureBotAI/auto-term-catalog.git
cd auto-term-catalog
```

If SSH is not configured, use HTTPS instead:

```bash
git clone https://github.com/CultureBotAI/auto-term-catalog.git
```

Verify current branch:

```bash
git branch --show-current
git status
```

## Part 3: Recommended Python version

Recommendation: use Python `3.11`.

Why:

- This repo currently depends only on `pandas` and `PyYAML`, both of which are very stable on 3.11.
- Python 3.11 is conservative enough for student onboarding and broad package compatibility.
- The code in this repo does not need 3.12-only or 3.13-only features.
- A lightweight data-processing repo benefits more from stability than from chasing the newest interpreter.

I would not start this repo on 3.9 or 3.10 now, and I would not make 3.13 the baseline for student onboarding unless other CultureBotAI repos are already standardized there.

## Part 4: Recommended repo infrastructure

Recommendation: keep the repo simple and use `uv`, not Poetry.

Why `uv`:

- Fast install and environment creation.
- Simple lockfile and dependency workflow.
- Good fit for small script-heavy repos.
- Easier for undergrads than a more opinionated packaging stack.

### Minimum baseline I recommend

Add these files:

- `pyproject.toml`
- `.python-version`
- `.gitignore`
- `.github/workflows/ci.yml`
- `tests/test_auto_terms_table.py`

Use these tools:

- `uv` for environment and lockfile
- `pytest` for tests
- `ruff` for linting and formatting

### Suggested dependency set

Runtime:

- `pandas`
- `pyyaml`

Dev:

- `pytest`
- `ruff`

### Suggested commands

Install `uv`:

```bash
brew install uv
```

Create the project environment:

```bash
uv python install 3.11
uv venv --python 3.11
source .venv/bin/activate
```

Add dependencies:

```bash
uv add pandas pyyaml
uv add --dev pytest ruff
```

Run the script:

```bash
uv run python src/process_terms/auto_terms_table.py
```

Run tests:

```bash
uv run pytest
```

Run lint/format:

```bash
uv run ruff check .
uv run ruff format .
```

## Part 5: Recommended code cleanup before asking the intern to do real work

These are the highest-value fixes:

1. Move the logic out of `src/process_terms/auto_terms_table.py` into an importable package directory with a valid Python module name such as `src/auto_term_catalog/`.
2. Replace the hard-coded YAML input path with `argparse` arguments.
3. Replace the hard-coded output path with a command-line option.
4. Add a small fixture YAML file and 2-4 tests for:
   - YAML document iteration
   - AUTO-term detection
   - category inference
   - CSV row generation
5. Add a short real README with setup, usage, and example command lines.

## Part 6: Concrete recommendation for this repo

If the immediate use case is:

- deciding Python version
- deciding repo infrastructure
- making the repo usable with Codex

then the right short-term choice is:

- Python `3.11`
- `uv`
- `pytest`
- `ruff`
- simple CLI with `argparse`
- package layout under `src/auto_term_catalog/`
- GitHub Actions CI running lint + tests on Python 3.11

That is enough structure for Codex to help reliably without overengineering the repo.

## Part 7: What the intern should actually do on day 1

1. Install Homebrew.
2. Install Node.
3. Install Codex CLI.
4. Sign in with ChatGPT using the LBL-provisioned account.
5. Clone `CultureBotAI/auto-term-catalog`.
6. Install `uv`.
7. Create a Python 3.11 virtual environment.
8. Ask Codex to scaffold:
   - `pyproject.toml`
   - `.python-version`
   - `.gitignore`
   - `tests/`
   - `argparse`-based CLI
9. Open a PR that only does repo scaffolding and removes hard-coded local paths.

## Part 8: Quick troubleshooting

### `brew: command not found`

The shell init step was probably skipped. Re-run the `brew shellenv` command that the installer printed.

### `npm: command not found`

Node was not installed correctly or the shell needs to be restarted.

### `codex: command not found`

Check:

```bash
npm bin -g
npm list -g @openai/codex
```

Then open a new shell.

### ChatGPT sign-in works, but Codex access does not

That usually means one of these:

- the LBL account is not actually provisioned for the workspace
- Codex is disabled by workspace policy
- the user is signed into the wrong OpenAI/ChatGPT identity

### The script fails on the intern's machine

That is expected in the current repo, because the main script contains a hard-coded path:

- `~/Downloads/chemical_utilization_cborg_gpt5_20250819_113045.yaml`

This should be removed before onboarding someone else.

## Sources

- Homebrew homepage: https://brew.sh/
- Homebrew installation docs: https://docs.brew.sh/Installation.html
- Codex CLI docs: https://developers.openai.com/codex/cli
- Codex in ChatGPT: https://help.openai.com/en/articles/11369540-codex-in-chatgpt
