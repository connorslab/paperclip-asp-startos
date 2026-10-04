import {sdk} from './sdk'
import {i18n} from './i18n'
export const setInterfaces=sdk.setupInterfaces(async({effects})=>{
const receipts=[]
const host3000=sdk.MultiHost.of(effects,'operator-interface');const origin3000=await host3000.bindPort(3000,{protocol:'http'});receipts.push(await origin3000.export([sdk.createInterface(effects,{id:'operator-interface',name:i18n('Operator interface'),description:i18n('Operator interface'),type:'ui',masked:false,schemeOverride:null,username:null,path:'',query:{}})]))
const host3535=sdk.MultiHost.of(effects,'ark-endpoint');const origin3535=await host3535.bindPort(3535,{protocol:null,preferredExternalPort:33535,addSsl:null,secure:{ssl:false}});receipts.push(await origin3535.export([sdk.createInterface(effects,{id:'ark-endpoint',name:i18n('Ark endpoint'),description:i18n('Ark endpoint'),type:'api',masked:false,schemeOverride:null,username:null,path:'',query:{}})]))
return receipts
})
