import unittest,sys,tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from hostname import apply_mapping
from common import validate

class HostnameTests(unittest.TestCase):
 def test_mapping_is_idempotent_and_removable(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'hosts';p.write_text('127.0.0.1 localhost\n')
   c={'cln_connect_ip':'192.168.1.111','cln':{'uri':'https://startos.local:39737','hold_uri':'https://startos.local:39738'}}
   apply_mapping(c,p);first=p.read_text();apply_mapping(c,p);self.assertEqual(first,p.read_text())
   self.assertIn('192.168.1.111 startos.local',first)
   apply_mapping({},p);self.assertEqual(p.read_text(),'127.0.0.1 localhost\n')
 def test_invalid_mapping_cannot_inject_hosts(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'hosts';p.write_text('127.0.0.1 localhost\n')
   with self.assertRaises(ValueError):apply_mapping({'cln_connect_ip':'192.168.1.111\nevil'},p)
   self.assertEqual(p.read_text(),'127.0.0.1 localhost\n')
