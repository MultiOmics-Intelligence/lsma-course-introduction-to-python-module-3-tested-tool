"""Automatic checks for LSMA Introduction to Python, Module 3 project.

Run from the top folder of your copy:   python tests/check_results.py
It reads only the files you commit in results/ and scripts/, uses the Python
standard library only, and prints PASS or FAIL for each task.
"""
import csv
import hashlib
import re
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
SCRIPTS = ROOT / "scripts"
DATA = ROOT / "data"
_failed = []


class Fail(Exception):
    pass


def check(label):
    """Run one labelled check and print PASS or FAIL."""
    def wrap(fn):
        try:
            fn()
        except Fail as err:
            print(f"FAIL  {label}: {err}")
            _failed.append(label)
        except Exception as err:  # an unreadable file should guide, not crash
            print(f"FAIL  {label}: could not read your results ({type(err).__name__}: {err})")
            _failed.append(label)
        else:
            print(f"PASS  {label}")
        return fn
    return wrap


def finish():
    print()
    if _failed:
        print(f"{len(_failed)} check(s) failed. Read the messages above, fix that task and push again.")
        sys.exit(1)
    print("Every checkpoint passed. Well done.")


def need(path):
    path = Path(path)
    if not path.exists():
        raise Fail(f"{path.relative_to(ROOT)} not found; create it and commit it")
    return path


def read_rows(path):
    """Read a CSV (or tab-separated) file into a list of dicts with lower-case keys."""
    text = need(path).read_text(encoding="utf-8-sig")
    dialect = "excel-tab" if "\t" in text.splitlines()[0] else "excel"
    rows = list(csv.DictReader(text.splitlines(), dialect=dialect))
    return [{(k or "").strip().lower(): (v or "").strip() for k, v in r.items()} for r in rows]


def column(rows, *names, path=""):
    if not rows:
        raise Fail(f"{path} has no data rows")
    for n in names:
        if n in rows[0]:
            return n
    raise Fail(f"{path} needs a column called {names[0]}; found {', '.join(rows[0])}")


def num(value, what):
    try:
        return float(str(value).replace("%", "").strip())
    except ValueError:
        raise Fail(f"{what}: '{value}' is not a number")


def near(a, b, tol):
    return abs(a - b) <= tol


def _norm(text):
    return re.sub(r"\s+", " ", text.replace("\r", "")).strip()


def sha(path):
    return hashlib.sha256(_norm(Path(path).read_text(encoding="utf-8")).encode()).hexdigest()


def edited(path, starter_sha):
    path = need(path)
    if sha(path) == starter_sha:
        raise Fail(f"{path.relative_to(ROOT)} is still the untouched starter; write your code in it")
    return path


def png_info(path):
    """Width, height and dpi (None if not stored) of a PNG file."""
    data = Path(path).read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    w, h = struct.unpack(">II", data[16:24])
    dpi = None
    i = 8
    while i + 8 <= len(data):
        length, kind = struct.unpack(">I4s", data[i:i + 8])
        if kind == b"pHYs":
            x, _, unit = struct.unpack(">IIB", data[i + 8:i + 17])
            if unit == 1:
                dpi = x * 0.0254
            break
        if kind == b"IDAT":
            break
        i += 12 + length
    return w, h, dpi


def image(path, min_px=300, min_bytes=5000):
    """Check that a PNG or SVG is a real image of sensible size; return PNG info."""
    path = need(path)
    rel = path.relative_to(ROOT)
    size = path.stat().st_size
    if size < min_bytes:
        raise Fail(f"{rel} is only {size} bytes; it looks empty")
    if path.suffix.lower() == ".svg":
        head = path.read_text(encoding="utf-8", errors="replace")[:5000]
        if "<svg" not in head:
            raise Fail(f"{rel} is not a valid SVG file")
        return None
    info = png_info(path)
    if info is None:
        raise Fail(f"{rel} is not a real PNG file (was it renamed from another format?)")
    w, h, _ = info
    if w < min_px or h < min_px // 3:
        raise Fail(f"{rel} is only {w} x {h} pixels; save it with a higher dpi")
    return info


def text_of(path, min_words=0):
    path = need(path)
    text = path.read_text(encoding="utf-8", errors="replace")
    words = len(re.findall(r"\w+", text))
    if words < min_words:
        raise Fail(f"{path.relative_to(ROOT)} has {words} words; write at least {min_words}")
    return text


WANT = {"seq1": (36, 44.4), "seq2": (23, 8.7), "seq3": (21, 95.2), "seq4": (27, 48.1)}


@check("Setup · Your tool")
def _():
    edited(SCRIPTS / "fasta_stats.py", "cbedb81391c6c4a78eab82f699816dba1da32a732c61c86cdadc2b05414d027a")


@check("Task 1 · Expected answers first")
def _():
    text = text_of(RESULTS / "expected_answers.md")
    for sid in ("seq2", "seq3"):
        if sid not in text:
            raise Fail(f"results/expected_answers.md should give the length and GC% of {sid}")
    nums = re.findall(r"\d+(?:\.\d+)?", text)
    for sid, (length, gc) in (("seq2", WANT["seq2"]), ("seq3", WANT["seq3"])):
        if str(length) not in nums or f"{gc}" not in nums:
            raise Fail(f"results/expected_answers.md: the hand-worked length or GC% of {sid} is missing "
                       "or not right (GC% to one decimal place)")


@check("Task 2 · Prompt")
def _():
    text = text_of(RESULTS / "prompt.md", min_words=60)
    low = text.lower()
    needs = [
        (r"python\s*3", "the Python version"),
        (r"standard library", "standard library only"),
        (r"argparse", "argparse"),
        (r"gc_content", "reuse of gc_content from seqtools.py"),
        (r"--min-length", "the --min-length option"),
        (r"8\.7", "your expected answers (seq2)"),
        (r"95\.2", "your expected answers (seq3)"),
    ]
    for pat, what in needs:
        if not re.search(pat, low):
            raise Fail(f"results/prompt.md does not yet state {what}")
    if not re.search(r"equal|exactly|at least|or more|shorter than|>=|≥", low):
        raise Fail("results/prompt.md: say exactly what --min-length does with a sequence whose "
                   "length equals the cut-off")


def parse_output(path):
    lines = [l for l in text_of(path).splitlines() if l.strip()]
    out = {}
    for l in lines:
        parts = re.split(r"[\t,;]\s*|\s+", l.strip())
        if len(parts) < 3:
            continue
        try:
            out[parts[0]] = (int(parts[1]), float(parts[2].rstrip("%")))
        except ValueError:
            continue  # a header line
    return out


@check("Task 3 · Review and run")
def _():
    allrows = parse_output(RESULTS / "output_all.txt")
    if len(allrows) != 4:
        raise Fail(f"expected 4 rows in results/output_all.txt, found {len(allrows)} "
                   "(ID, length and GC% on each line)")
    for sid, (length, gc) in WANT.items():
        if sid not in allrows:
            raise Fail(f"results/output_all.txt has no line for {sid}")
        got_len, got_gc = allrows[sid]
        if got_len != length:
            raise Fail(f"results/output_all.txt: the length of {sid} does not match your Task 1 answers")
        if not near(got_gc, gc, 0.051):
            raise Fail(f"results/output_all.txt: the GC% of {sid} is not right "
                       "(a percentage, one decimal place)")
    short = parse_output(RESULTS / "output_min25.txt")
    if sorted(short) != ["seq1", "seq4"]:
        raise Fail(f"results/output_min25.txt should keep only the sequences of 25 bases or more; "
                   f"found {', '.join(sorted(short)) or 'none'}")
    helptext = text_of(RESULTS / "help.txt")
    if "usage" not in helptext.lower() or "--min-length" not in helptext:
        raise Fail("results/help.txt should hold the output of --help, including the --min-length option")


@check("Task 4 · Tests")
def _():
    files = sorted((ROOT / "tests").glob("test_*.py"))
    if not files:
        raise Fail("no tests/test_*.py file found")
    code = "\n".join(f.read_text() for f in files)
    starter = ROOT / "tests" / "test_fasta_stats.py"
    if len(files) == 1 and starter.exists() and sha(starter) == "114f7fc4fc270c131abf648ec107d2df3222355116cee6a7f5aa41b8bd00c323":
        raise Fail("tests/test_fasta_stats.py is still the untouched starter; write your tests in it")
    n = len(re.findall(r"^\s*def\s+test_\w*\s*\(", code, flags=re.M))
    if n < 4:
        raise Fail(f"found {n} test function(s); write at least four (practice file, option, "
                   "empty file, sequence before the first header)")
    if "tmp_path" not in code:
        raise Fail("use pytest's tmp_path to write the awkward files your tests need")
    if not re.search(r"""write_text\(\s*(""|'')\s*\)|empty""", code, flags=re.I):
        raise Fail("add a test with an empty file")
    if not (re.search(r"""["'][ACGTNacgtn]+\\n>""", code)
            or re.search(r"""["']{3}\s*[ACGTNacgtn]+\s*\n\s*>""", code)
            or re.search(r"before.{0,20}header", code, flags=re.I)):
        raise Fail("add a test with sequence letters before the first header")


@check("Task 5 · Explain it back")
def _():
    lines = need(SCRIPTS / "fasta_stats.py").read_text().splitlines()
    defs = [i for i, l in enumerate(lines) if re.match(r"\s*def\s+\w+", l)]
    if not defs:
        raise Fail("scripts/fasta_stats.py has no functions; put the work in functions such as main()")
    for i in defs:
        j = i - 1
        while j >= 0 and lines[j].strip().startswith("@"):
            j -= 1
        if j < 0 or not lines[j].strip().startswith("#"):
            name = re.match(r"\s*def\s+(\w+)", lines[i]).group(1)
            raise Fail(f"write a comment (# ...) directly above the function {name}() "
                       "saying what it does and why")


SECRETS = [
    (r"sk-[A-Za-z0-9_-]{20,}", "an API key"),
    (r"gh[pousr]_[A-Za-z0-9]{30,}", "a GitHub token"),
    (r"AKIA[0-9A-Z]{16}", "a cloud access key"),
    (r"-----BEGIN [A-Z ]*PRIVATE KEY-----", "a private key"),
    (r"(api[_-]?key|password|secret|token)\s*[:=]\s*['\"][^'\"\s]{8,}['\"]", "a password or key"),
]


@check("Task 6 · Disclose and share")
def _():
    text = text_of(SCRIPTS / "README.md")
    low = text.lower()
    if "fasta_stats.py" not in text or "--min-length" not in text:
        raise Fail("scripts/README.md should show how to run the tool, with the --min-length option")
    if "pytest" not in low:
        raise Fail("scripts/README.md should say how to run the tests")
    m = re.search(r"^#+\s*use of ai tools\s*$(.*?)(?=^#|\Z)", text, flags=re.M | re.S | re.I)
    if not m:
        raise Fail("scripts/README.md needs a section headed 'Use of AI tools'")
    if len(re.findall(r"\w+", m.group(1))) < 25:
        raise Fail("the 'Use of AI tools' section is too short: say which tool, what for, and how you checked it")
    if "[tool and version]" in low or "[month year]" in low:
        raise Fail("replace the placeholders in square brackets with the real tool and date")
    for f in ROOT.rglob("*"):
        if ".git" in f.parts or not f.is_file() or f.stat().st_size > 2_000_000:
            continue
        if f.name == ".env":
            raise Fail(f"remove {f.relative_to(ROOT)} before sharing: it usually holds secrets")
        body = f.read_text(errors="ignore")
        for pat, what in SECRETS:
            if f.name != "check_results.py" and re.search(pat, body, flags=re.I):
                raise Fail(f"{f.relative_to(ROOT)} seems to contain {what}; remove it before sharing")


finish()
