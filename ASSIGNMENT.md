# Finance Tracker CLI — Assignment

## 1  Project Overview (non‑technical)

Design and build a **command‑line personal finance tracker** that lets everyday users log income and expenses, organise them into categories. Think of it as a "digital ledger in your terminal":

* Add or remove transactions (income / expense)
* Tag transactions with one or more categories
* List transactions with helpful filters (by date range, category, type)
* Persist data to a local SQLite file

---

## 2  How to Tackle the Assignment

The work happens in **three phases**. Complete them in order.

### 2.1  Phase 1 – *Picture*

Get the understanding of the project and think on how to implement it. \
Refer to the [From Features to Architecture Guide](docs/howto_architecture.md).

### 2.2  Phase 2 – *Implementation*

Build a vertical slice, then expand feature‑by‑feature.

#### 2.2.1  Tooling & Environment

| Requirement         | Details                                                           |
| ------------------- | ----------------------------------------------------------------- |
| **Python**          | 3.12+                                                             |
| **Package manager** | [`uv`](https://github.com/astral‑sh/uv) (`uv sync`, `.venv`)      |
| **CLI lib**         | [Typer](https://typer.tiangolo.com/) (recommended)                |
| **Database**        | Raw SQLite via `sqlite3` (required)                               |
| **CI**              | GitHub Actions or GitLab CI with lint+type‑check+tests (bonus)|

#### 2.2.2  Quality Gates

* **Testing:** `pytest`; aim ≥ 80 % line coverage.
* **Linting:** `ruff` — must pass with `ruff check .`.
* **Static types:** `pyrefly` — must pass with `pyrefly check src --search-path .`.
* **Docstrings:** Google‑style for all public symbols.
* **Error handling:** graceful CLI messages (exit codes, no stack traces on user error).
* **Logging (bonus):** structured log file + console with levels.

#### 2.2.2  Architecture
* Honour the 4‑layer dependency rule (Presentation → Application → Domain → Infrastructure).

Note: The good architecture is crucial in the assignment.

#### 2.2.3  Minimal Feature Set

| Area             | Supported Commands                                                               |
| ---------------- | -------------------------------------------------------------------------------- |
| **Transactions** | `add`, `remove`, `list` *(flags: `--after`, `--before`, `--category`, `--type`)* |
| **Categories**   | `add‑category`, `remove‑category`, `list‑categories`                             |

All commands must appear in `--help`.

#### 2.2.4  Documentation Deliverables

* **README.md** – setup, backend selection, CLI examples, screenshots.
* **Docstrings** – every public class/function.

**Important:** Without README.md, you'll lose at least 50% of the points.

### 2.3  Phase 3 – *Extra Task* (pick by TA after the feedback)

| Option                     | Description                                                                                                 |
| -------------------------- | ----------------------------------------------------------------------------------------------------------- |
| **A – SQLAlchemy Backend** | Add a second persistence adapter using SQLAlchemy; switch via `FINANCE_TRACKER_BACKEND` env var.            |
| **B – Budget Limits**      | Enforce per‑category spending limits; warn on `add` when limit > 80 % consumed.                             |
| **C – Reports**            | New `report` command that prints summary tables *and* saves a spending plot (`matplotlib`) as `report.png`. |

Bonus kudos for clean abstractions that make each option “plug‑in” small.

### 2.4  Grading

| Part | Points | Style | Correctness | Scope / expectation |
| ---- | ------ | ----- | ----------- | ------------------- |
| **1** | 75 | 50 | 25 | Implement the `add` feature only, but fully end‑to‑end (CLI, domain, persistence, tests, docs). |
| **2** | 50 | 30 | 20 | Implement the rest of the minimal features set. |
| **3** | 50 | 25 | 25 | Extra task completed after feedback. |

### 2.5  1‑to‑1 Demo with TA

You'll have a 1-to-1 demo with the TA to get the first feedback and extra task selection.

1. **Environment ready**: Python and `uv` versions, active virtualenv, `uv sync` done.
2. **Run quality gates**: `ruff check .`, `pyrefly check src --search-path .`, `pytest -q` (show all green).
3. **Architecture tour (≤3 min)**: walk through `src/` layers and where CLI ↔ services ↔ domain ↔ persistence connect.
4. **Help and UX**: `finance --help` and subcommands `add`, `remove`, `list`, `add-category`, etc. Flags visible.
5. **Part 1 demo (add end‑to‑end)**: add a transaction; immediately list it; restart the CLI and list again to prove persistence (SQLite file present).
6. **Part 2 demo (minimal set)**: show categories CRUD and transaction filters (`--after/--before/--category/--type`).
7. **Data storage**: briefly open/show where data is stored (SQLite path) and how repository abstracts it.
8. **Tests**: point to a couple of representative tests; explain what is covered; show coverage number if available.
9. **Further discussion**: TA will ask you questions about the code and the architecture.

---

## 3  Advice for Success

1. **Work incrementally.** Implement one CLI command end‑to‑end, commit, then move on.
2. **Don’t skip Phase 1.** A 30‑minute design sketch will save hours of refactor pain.
3. **Start with an in‑memory repo** for fast TDD, swap in SQLite once tests pass.
4. **Keep functions < 15 lines, files < 250 lines** (same old code‑quality rules).
5. **Use .gitignore** to keep the repo clean.
