from pathlib import Path
import subprocess
import sys
import tempfile
import shutil
ROOT=Path(__file__).resolve().parent
COMMANDS=[]
COMMAND_LINES=['python main.py examples/demo --out outputs/demo', 'python main.py examples/demo --exclude "*.md" --max-total 10000 --out outputs/code-only']
import shlex
with tempfile.TemporaryDirectory() as temp:
    target=Path(temp)
    shutil.copytree(ROOT/'examples',target/'examples')
    for line in COMMAND_LINES:
        args=shlex.split(line)
        subprocess.run([sys.executable,str(ROOT/'main.py'),*args[2:]],cwd=target,check=True)
    assert list((target/'outputs').rglob('*.html')), 'No HTML report generated'
print('Examples passed')
