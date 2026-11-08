"""Select local text files and produce a bounded Markdown context pack."""
import argparse
import fnmatch
import hashlib
import json
import os
from pathlib import Path
import re
from common import configure_console, report, write_json, write_text

IGNORED_DIRS = {'.git', '.codex', '.ssh', '.aws', '.azure', '.config', '.venv', 'venv', 'node_modules', '__pycache__', 'dist', 'build', 'outputs'}
IGNORED_FILES = {'.env', 'auth.json', 'credentials.json', 'id_rsa', 'id_ed25519'}
TEXT_EXTENSIONS = {'.py', '.js', '.ts', '.tsx', '.jsx', '.html', '.css', '.md', '.txt', '.json', '.toml', '.yaml', '.yml', '.sql', '.go', '.rs', '.java', '.c', '.cpp', '.h', '.sh', '.ps1', '.ini', '.cfg'}
SECRET_PATTERN = re.compile(r'(?:\b(?:api[_-]?key|access[_-]?token|password|secret)\b\s*[:=]\s*["\']?[^\s"\']{12,}|sk-[A-Za-z0-9_-]{16,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----)', re.I)


def collect(root, max_file=100000, max_total=1000000, exclude=(), output=None):
    root = Path(root).resolve()
    if not root.is_dir():
        raise ValueError('Input must be an existing directory')
    if max_file <= 0 or max_total <= 0:
        raise ValueError('Size limits must be positive integers')
    output = Path(output).resolve() if output else None
    if output == root:
        raise ValueError('Output directory must differ from the input directory')
    included, skipped, total = [], [], 0
    for directory, children, files in os.walk(root, followlinks=False):
        current = Path(directory)
        children[:] = sorted(name for name in children if name not in IGNORED_DIRS
                             and not (current / name).is_symlink()
                             and (output is None or (current / name).resolve() != output))
        for name in sorted(files):
            path = current / name
            relative = path.relative_to(root).as_posix()
            reason = None
            if path.is_symlink(): reason = 'symlink'
            elif name in IGNORED_FILES or name.startswith('.env') or path.suffix.lower() in {'.pem', '.key', '.p12', '.pfx'}: reason = 'sensitive filename'
            elif any(fnmatch.fnmatch(relative, pattern) for pattern in exclude): reason = 'custom exclusion'
            elif path.suffix.lower() not in TEXT_EXTENSIONS: reason = 'unsupported extension'
            elif path.stat().st_size > max_file: reason = 'file size limit'
            if reason:
                skipped.append({'path': relative, 'reason': reason})
                continue
            try:
                raw = path.read_bytes()
                content = raw.decode('utf-8-sig')
            except (OSError, UnicodeDecodeError):
                skipped.append({'path': relative, 'reason': 'unreadable or non-UTF-8'})
                continue
            if '\x00' in content or SECRET_PATTERN.search(content):
                skipped.append({'path': relative, 'reason': 'binary marker or potential secret'})
                continue
            if total + len(raw) > max_total:
                skipped.append({'path': relative, 'reason': 'total size limit'})
                continue
            total += len(raw)
            included.append({'path': relative, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(), 'content': content})
    return {'files': included, 'skipped': skipped, 'total_bytes': total}


def build_pack(result):
    lines = ['# Codex Context Pack', '', 'Review this pack before sharing it with any model or person.',
             '', '[NB破甲官网](https://nbpojia.lol) · [Telegram 社群](https://t.me/HaoNB_6666)', '']
    for item in result['files']:
        fence = '`' * max(3, max((len(m.group()) + 1 for m in re.finditer(r'`+', item['content'])), default=3))
        lines += ['## ' + item['path'].replace('\n', ' ').replace('\r', ' '), '', fence, item['content'], fence, '']
    return '\n'.join(lines)


def main():
    configure_console()
    parser = argparse.ArgumentParser(description='Codex context pack / 代码上下文打包器')
    parser.add_argument('root', type=Path)
    parser.add_argument('--out', type=Path, default=Path('outputs/context'))
    parser.add_argument('--max-file', type=int, default=100000, help='Maximum bytes per file')
    parser.add_argument('--max-total', type=int, default=1000000, help='Maximum total source bytes')
    parser.add_argument('--exclude', action='append', default=[], help='Repeated relative-path glob')
    args = parser.parse_args()
    try:
        result = collect(args.root, args.max_file, args.max_total, args.exclude, args.out)
        manifest = {'files': [{k: v for k, v in f.items() if k != 'content'} for f in result['files']],
                    'skipped': result['skipped'], 'total_bytes': result['total_bytes'],
                    'privacy': 'Filename/pattern filtering is heuristic, not a guarantee. Review before sharing.'}
        write_text(args.out / 'context.md', build_pack(result))
        write_json(args.out / 'manifest.json', manifest)
        write_text(args.out / 'report.html', report('Codex Context Pack / 上下文清单', manifest))
        print(json.dumps({'files': len(result['files']), 'bytes': result['total_bytes'], 'output': str(args.out)}, ensure_ascii=False))
    except (ValueError, OSError) as error:
        parser.exit(2, str(error) + '\n')


if __name__ == '__main__': main()
