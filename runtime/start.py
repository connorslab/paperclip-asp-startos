import os,json,secrets,subprocess,tomllib
from pathlib import Path
from common import config,write,verify_chain
os.umask(0o077); c=config('ark');verify_chain(c)
from hostname import apply_mapping
apply_mapping(c)
data=Path('/var/lib/paperclip-asp');data.mkdir(exist_ok=True,mode=0o700)
configdir=Path('/config');configdir.mkdir(exist_ok=True,mode=0o700)
backend={'url':c['rpc_url'],'rpc_user':c['rpc_user'],'rpc_pass':c['rpc_password']}
if c.get('pruned',False):
    root=data/'chain';root.mkdir(exist_ok=True,mode=0o700)
    write(root/'backend.json',json.dumps({'network':'main' if c['network']=='bitcoin' else 'regtest','rpc_url':c['rpc_url']}))
    write(root/'backend.cookie',c['rpc_user']+':'+c['rpc_password'])
    if not (root/'client.cookie').exists(): write(root/'client.cookie','paperclip:'+secrets.token_hex(32))
    backend={'url':'http://127.0.0.1:18336','cookie':str(root/'client.cookie')}
for watch in [False,True]:
    name='watchmand' if watch else 'captaind'
    cfg=tomllib.loads(Path('/opt/paperclip/server/'+name+'.default.toml').read_text())
    cfg.update(data_dir=str(data),network=c['network'],bitcoind=backend,otel_tracing_sampler=0.0)
    cfg['postgres'].update(host='127.0.0.1',port=5432,name='paperclip_asp',user='paperclip',password=os.environ['POSTGRES_PASSWORD'])
    cfg['fee_estimator'].update(fallback_fee_rate_fast='2sat/vb',fallback_fee_rate_regular='1sat/vb',fallback_fee_rate_slow='1sat/vb')
    if not watch:
        cfg.update(experimental_sideflash_auto_register=c.get('auto_register',True),experimental_funded_lightning=bool(c.get('cln')),experimental_bolt12_receive=bool(c.get('cln')),sideflash_recipient_allowlist=c.get('recipient_allowlist',[]),require_board_funding_tx=True,handshake_psa='Sideflash isolated test ASP. Experimental and unaudited.',max_ln_receive_amount='50000 sat',max_ln_send_amount='50000 sat',cln_array=[])
        cfg['rpc']={'public_address':'0.0.0.0:3535','admin_address':'127.0.0.1:3536'}
        cfg['vtxopool'].update(vtxo_targets=['50000sat:2'] if c.get('cln') else [],onchain_reserve_sat=20000)
        if c.get('cln'):
            tls=c['cln'];td=configdir/'tls';td.mkdir(exist_ok=True,mode=0o700)
            for key,file in [('ca','ca.pem'),('client_cert','client.pem'),('client_key','client-key.pem')]:write(td/file,tls[key])
            common={'server_cert_path':str(td/'ca.pem'),'client_cert_path':str(td/'client.pem'),'client_key_path':str(td/'client-key.pem')}
            cfg['cln_array']=[dict(common,uri=tls['uri'],priority=0,hold_invoice=dict(common,uri=tls['hold_uri']))]
    else:
        cfg['watchman']['incremental_relay_fee']='1000 sat/kvb'
        cfg['sweep_address']=c['sweep_address']
    write(configdir/('watchman.json' if watch else 'asp.json'),json.dumps(cfg))
os.environ['PAPERCLIP_XBT_MAINNET']='1';os.environ['PAPERCLIP_PRUNED_RPC']='1'
os.execvp('python3',['python3','/opt/paperclip/deployment/managed-chain.py','run'])
