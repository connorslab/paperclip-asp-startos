import json,sys,re
from urllib.parse import urlsplit
from common import validate
def apply(configuration,bundle):
 if not isinstance(bundle,str) or len(bundle)>65536:raise ValueError('Invalid bundle size')
 b=json.loads(bundle)
 if b.get('format')!='paperclip-cln-connection' or b.get('version')!=1:raise ValueError('Unsupported CLN bundle')
 if b.get('network')!=configuration.get('network'):raise ValueError('CLN and Ark networks must match')
 if not re.fullmatch(r'0[23][0-9a-fA-F]{64}',b.get('node_id','')):raise ValueError('Invalid CLN identity')
 cln={k:b[k] for k in ['uri','hold_uri','ca','client_cert','client_key']}
 for k in ['uri','hold_uri']:
  u=urlsplit(cln[k])
  if u.scheme!='https' or not u.hostname or not u.port or u.username or u.password or u.path not in ('','/') or u.query or u.fragment:raise ValueError('Invalid gRPC endpoint')
 for k,marker in [('ca','CERTIFICATE'),('client_cert','CERTIFICATE'),('client_key','PRIVATE KEY')]:
  if not isinstance(cln[k],str) or '-----BEGIN '+marker+'-----' not in cln[k]:raise ValueError('Invalid certificate or client key')
 result={**configuration,'cln':cln};validate('ark',result);return result
if __name__=='__main__':
 try:
  i=json.load(sys.stdin);print(json.dumps(apply(i['configuration'],i['bundle'])))
 except Exception:
  raise SystemExit('Invalid CLN bundle: copy the complete export from your CLN package and check that both apps use the same network. Existing settings were not changed.')
