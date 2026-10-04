import unittest, importlib.util, sys, json
from pathlib import Path
runtime = Path(__file__).resolve().parents[1] / 'runtime'
sys.path.insert(0, str(runtime))
spec = importlib.util.spec_from_file_location('bundle_import', runtime / 'import-cln.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class ImportTests(unittest.TestCase):
    def config(self):
        return dict(network='bitcoin', rpc_url='http://127.0.0.1:9332', rpc_user='test', rpc_password='test', sweep_address='bc1q'+'q'*38, recipient_allowlist=[], custom='preserved')

    def bundle(self):
        return dict(format='paperclip-cln-connection', version=1, network='bitcoin', node_id='02'+'a'*64, uri='https://node:39737', hold_uri='https://node:39738', ca='-----BEGIN CERTIFICATE-----', client_cert='-----BEGIN CERTIFICATE-----', client_key='-----BEGIN PRIVATE KEY-----')

    def test_preserves_settings(self):
        c = self.config()
        result = m.apply(c, json.dumps(self.bundle()))
        self.assertEqual(result['custom'], 'preserved')
        self.assertEqual(result['rpc_password'], c['rpc_password'])
        self.assertNotIn('cln', c)
        self.assertEqual(result['cln']['uri'], 'https://node:39737')

    def test_rejects_wrong_network(self):
        b = self.bundle(); b['network'] = 'regtest'
        with self.assertRaises(ValueError): m.apply(self.config(), json.dumps(b))

    def test_rejects_wrong_version(self):
        b = self.bundle(); b['version'] = 2
        with self.assertRaises(ValueError): m.apply(self.config(), json.dumps(b))

    def test_rejects_invalid_endpoints(self):
        for endpoint in ['http://node:39737', 'https://u:p@node:39737', 'https://node:39737/?x=y', 'https://node:REPLACE_WITH_PORT']:
            b = self.bundle(); b['uri'] = endpoint
            with self.assertRaises(ValueError): m.apply(self.config(), json.dumps(b))

    def test_rejects_missing_key(self):
        b = self.bundle(); b['client_key'] = ''
        with self.assertRaises(ValueError): m.apply(self.config(), json.dumps(b))
