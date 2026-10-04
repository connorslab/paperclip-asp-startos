import {sdk} from './sdk'
import {store} from './fileModels/store'
import {i18n} from './i18n'
export const main=sdk.setupMain(async({effects})=>{const saved=await store.read().const(effects);if(!saved?.configuration)throw new Error(i18n('Configure the backend before starting'));
await sdk.volumes.main.writeFile('settings.json',saved.configuration,{mode:0o600});

const pg=sdk.SubContainer.of(effects,{imageId:'postgres'},sdk.Mounts.of().mountVolume({volumeId:'postgres',subpath:null,mountpoint:'/var/lib/postgresql/data',readonly:false}),'postgres')
const daemons=sdk.Daemons.of(effects).addDaemon('postgres',{subcontainer:pg,exec:{command:['/usr/local/bin/docker-entrypoint.sh','postgres','-c','listen_addresses=127.0.0.1'],env:{POSTGRES_DB:'paperclip_asp',POSTGRES_USER:'paperclip',POSTGRES_PASSWORD:saved.postgres},user:'root',runAsInit:true},ready:{display:i18n('Database'),fn:()=>sdk.healthCheck.checkPortListening(effects,5432,{successMessage:i18n('Ready'),errorMessage:i18n('Starting')})},requires:[]})
return daemons.addDaemon('app',{subcontainer:sdk.SubContainer.of(effects,{imageId:'app'},sdk.Mounts.of().mountVolume({volumeId:'main',subpath:null,mountpoint:'/data',readonly:false}).mountVolume({volumeId:'asp',subpath:null,mountpoint:'/var/lib/paperclip-asp',readonly:false}).mountVolume({volumeId:'config',subpath:null,mountpoint:'/config',readonly:false}),'app'),exec:{command:['/usr/bin/tini','--','python3','/opt/startos/start.py'],user:'root',runAsInit:true,env:{STARTOS_TOKEN:saved.token,APP_PASSWORD:saved.token,POSTGRES_PASSWORD:saved.postgres}},ready:{display:i18n('Service'),fn:()=>sdk.healthCheck.checkPortListening(effects,3000,{successMessage:i18n('Ready'),errorMessage:i18n('Starting')})},requires:["postgres"]})
})
