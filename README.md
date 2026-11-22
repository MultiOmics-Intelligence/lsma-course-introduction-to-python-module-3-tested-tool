<a href="https://lsma.co.uk/courses"><img src="https://raw.githubusercontent.com/MultiOmics-Intelligence/.github/main/assets/lsma-walk-courses.svg" alt="LSMA, London School of Multiomics and AI: learn by doing, on real data" width="100%"></a>

# Module 3 project: A tested tool, built with AI

LSMA · Introduction to Python · Module 3 project

<p>
<img src="https://img.shields.io/badge/LSMA-free%20course-D9481F?style=flat-square" alt="LSMA free course">
<img src="https://img.shields.io/badge/course-Introduction%20to%20Python-0F1B33?style=flat-square" alt="Course">
<img src="https://img.shields.io/badge/language-Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Language">
<img src="https://img.shields.io/badge/checks-automatic-2F7D5B?style=flat-square&logo=githubactions&logoColor=white" alt="Automatic checks">
</p>

## Research question

Can you build a small, trustworthy command-line tool with an AI assistant, and prove it works? Build `fasta_stats.py`: given a FASTA file, print one line per sequence with its ID, length and GC%, with an option to skip short sequences. Run it as:

```
python scripts/fasta_stats.py data/practice_sequences.fasta --min-length 25
```

The order of the tasks is the point: you work out the answers before you ask for any code, you read and test what comes back, and only then do you share it.

## What you will build

| Files in | Files out |
|---|---|
| `data/practice_sequences.fasta`, four records, seq1 to seq4 | `results/expected_answers.md`, your hand-worked answers |
| `scripts/seqtools.py`, your module from Module 1 (`gc_content`) | `results/prompt.md`, the prompt you gave the assistant |
| | `scripts/fasta_stats.py`, the tool, with your comments |
| | `results/output_all.txt`, `results/output_min25.txt` and `results/help.txt` |
| | `tests/test_fasta_stats.py`, your pytest tests |
| | `scripts/README.md`, usage, tests and a "Use of AI tools" section |

The tool's output format: one line per sequence, tab-separated, ID, length and GC% to one decimal place, for example `seq1	36	44.4`.

## Before you start

1. Get your own copy. Use the GitHub Classroom invitation link in the project lesson on [lsma.co.uk](https://lsma.co.uk), or press **Use this template** on this page.
2. Clone your copy to your computer, or open it in GitHub Codespaces.
3. The tool needs Python 3 only. For the tests, install pytest once: `pip install pytest`.
4. Work in `scripts/` and `tests/`. Run everything from the top folder of your copy.
5. Write every output to `results/`, with the exact file names above.

You can run the checks yourself at any time: `python tests/check_results.py`, then `pytest -q tests`.

## Tasks

### 1. Expected answers first

Lesson to revisit: lessons 2 and 3.

Before asking anything, work out by hand the length and GC% of seq2 and seq3 in `practice_sequences.fasta`. Open the file in a text editor, not in Python. Write your working in `results/expected_answers.md`.

**Checkpoint:** seq2 has 23 bases and 8.7% GC; seq3 has 21 bases and 95.2% GC.

### 2. Prompt

Lesson to revisit: lesson 2.

Write a specific prompt in `results/prompt.md`: Python version, standard library only (argparse), reuse `gc_content` from your `seqtools.py`, the output format, the option, and your expected answers. Say exactly what the option should do with a sequence whose length equals the cut-off.

**Checkpoint:** a reader could write the tool from your prompt alone.

### 3. Review and run

Lesson to revisit: lesson 3.

Read every line of what you get back, save it as `scripts/fasta_stats.py` and run it. Check the output against Task 1, and try `--help`. Save the three outputs:

```
python scripts/fasta_stats.py data/practice_sequences.fasta > results/output_all.txt
python scripts/fasta_stats.py data/practice_sequences.fasta --min-length 25 > results/output_min25.txt
python scripts/fasta_stats.py --help > results/help.txt
```

**Checkpoint:** four rows with lengths 36, 23, 21 and 27 and GC% 44.4, 8.7, 95.2 and 48.1; with `--min-length 25`, only seq1 and seq4.

### 4. Tests

Lesson to revisit: lessons 4 and 5.

In `tests/test_fasta_stats.py`, write pytest tests with your own expected values, including a FASTA file with a sequence before the first header, and an empty file. Fix anything that fails, and add a test for each fix. `tests/conftest.py` already lets your tests import from `scripts/`, for example `from fasta_stats import main`.

**Checkpoint:** all tests pass, and a malformed file gives a clear error message rather than a crash deep inside the code.

### 5. Explain it back

Lesson to revisit: lesson 6.

Without the assistant, write a comment (`# ...`) directly above each function in `fasta_stats.py`, saying what it does and why.

**Checkpoint:** you can explain every line, including how argparse reads `--min-length`.

### 6. Disclose and share

Lesson to revisit: lessons 7 and 8.

Write `scripts/README.md` with usage, the tests, and a "Use of AI tools" section. Check that no secrets or private data are in the folder before sharing it, including hidden files whose names start with a dot.

**Checkpoint:** someone else could install, run and test the tool from the README, and knows exactly how AI was used.

## Hand in

Commit and push `scripts/`, `tests/` and `results/`. The **Checks** tab (GitHub Actions) then runs in two steps: first the results check, then your own tests with pytest. A green tick means every checkpoint passed and all your tests pass. You can push as often as you like.

## If a check fails

Open the failed run in the Actions tab and read the log. Each line of the results check starts with PASS or FAIL and names the task, for example `FAIL  Task 3 · Review and run: ...`. The message tells you what to look at, not the answer. If the pytest step fails, its report names the test that failed and the values that differed. Fix it and push again.

## Getting help

- The project lesson on lsma.co.uk, and the earlier lessons named in each task.
- Helix, the course tutor.
- Email info@lsma.co.uk.

Never post personal data in public, in an issue, a commit or a file.

**Follow LSMA**

<p>
  <a href="https://lsma.co.uk"><img src="https://raw.githubusercontent.com/MultiOmics-Intelligence/.github/main/assets/btn-lsma-website.svg" alt="LSMA: lsma.co.uk" height="54"></a>
  <a href="https://www.linkedin.com/showcase/113252126/"><img src="https://raw.githubusercontent.com/MultiOmics-Intelligence/.github/main/assets/btn-lsma-linkedin.svg" alt="LSMA on LinkedIn" height="54"></a>
  <a href="https://www.instagram.com/lsma.uk/"><img src="https://raw.githubusercontent.com/MultiOmics-Intelligence/.github/main/assets/btn-lsma-instagram.svg" alt="LSMA on Instagram: @lsma.uk" height="54"></a>
  <a href="mailto:info@lsma.co.uk"><img src="https://raw.githubusercontent.com/MultiOmics-Intelligence/.github/main/assets/btn-lsma-email.svg" alt="Email: info@lsma.co.uk" height="54"></a>
</p>

Good luck, and enjoy the project.

**Dr. Anas Alzaeem**<br>
Academic Director, LSMA

[![Dr. Anas Alzaeem, Academic Director, LSMA](https://raw.githubusercontent.com/MultiOmics-Intelligence/.github/main/assets/signature/LSMA_Banner_Anas_Alzaeem.png)](https://lsma.co.uk)

© 2026 MultiOmics Intelligence Ltd. LSMA is the education arm of MultiOmics Intelligence. Code licensed under MIT.
