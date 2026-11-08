import hashlib
import tempfile
import unittest
from pathlib import Path
import main

class ContextTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
    def file(self,name,text):
        path=self.root/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text,encoding='utf-8');return path
    def test_manifest_hash_unicode(self):
        p=self.file('app.py','print("你好")')
        r=main.collect(self.root)
        self.assertEqual(r['files'][0]['sha256'],hashlib.sha256(p.read_bytes()).hexdigest())
        self.assertEqual(r['total_bytes'],len(p.read_bytes()))
    def test_sensitive_names_and_contents(self):
        self.file('.env','hello');self.file('secret.py','api_key="abcdefghijklmnop"');self.file('ok.py','print(1)')
        self.assertEqual([f['path'] for f in main.collect(self.root)['files']],['ok.py'])
    def test_limits_and_custom_glob(self):
        self.file('a.py','abcd');self.file('b.py','12345')
        self.assertEqual(len(main.collect(self.root,max_file=4)['files']),1)
        self.assertEqual(len(main.collect(self.root,max_total=5)['files']),1)
        self.assertEqual(len(main.collect(self.root,exclude=['*.py'])['files']),0)
    def test_nested_output_and_ignored_dirs(self):
        self.file('a.py','x');self.file('report/leak.py','y');self.file('.git/leak.py','z')
        self.assertEqual([f['path'] for f in main.collect(self.root,output=self.root/'report')['files']],['a.py'])
    def test_binary_and_invalid_utf8(self):
        self.file('a.py','a\x00b');(self.root/'b.py').write_bytes(b'\xff')
        self.assertFalse(main.collect(self.root)['files'])
    def test_fence_does_not_close_early(self):
        self.file('readme.md','```python\nhello\n```')
        self.assertIn('````',main.build_pack(main.collect(self.root)))
    def test_invalid_limits(self):
        with self.assertRaises(ValueError): main.collect(self.root,max_total=0)
        with self.assertRaises(ValueError): main.collect(self.root,output=self.root)
