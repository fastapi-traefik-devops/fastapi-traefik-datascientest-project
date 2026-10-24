#!/usr/bin/env node
'use strict';
// Runs only the fixed credential-free GET collection; never executes the examples collection.
const fs = require('fs'), path = require('path'), https = require('https'), dns = require('dns');
const root = path.resolve(__dirname, '..');
const modulePath = process.env.LIORA_API_TOOLS || path.resolve(__dirname, '../../../../.api-tools');
const newman = require(require.resolve('newman', {paths:[modulePath, process.cwd()]}));
const [environment, route, output] = process.argv.slice(2);
if (!['dev','stage','prod'].includes(environment) || !['public','private'].includes(route) || !output) {
  throw new Error('Usage: run-newman.cjs dev|stage|prod public|private NEW_OUTPUT_DIRECTORY');
}
const outputDir = path.resolve(output);
if (outputDir === root || outputDir.startsWith(root+path.sep)) throw new Error('Use a new output directory outside the evidence tree.');
fs.mkdirSync(outputDir,{recursive:false,mode:0o700}); // Refuse overwriting existing evidence.
const collection = JSON.parse(fs.readFileSync(path.join(root,'collections/liora-readonly.postman_collection.json')));
const env = JSON.parse(fs.readFileSync(path.join(root,'environments',`${environment}.postman_environment.json`)));
const host = new URL(env.values.find(x=>x.key==='base_url').value).hostname;
for (const folder of collection.item) for (const item of folder.item) {
  if (item.request.method!=='GET' || !item.request.url.startsWith('{{base_url}}/api/v1/')) throw new Error('Unexpected request rejected');
}
// Map only this run's documented hostname; keep HTTPS hostname, Host and certificate/SNI verification.
const lookup = (hostname,options,callback) => {
  if (typeof options==='function') {callback=options;options={};}
  if (route==='private' && hostname===host) {
    if (options?.all) return callback(null,[{address:'192.168.77.240',family:4}]);
    return callback(null,'192.168.77.240',4);
  }
  return dns.lookup(hostname,options,callback);
};
const agent = new https.Agent({lookup,keepAlive:true,rejectUnauthorized:true});
const started = new Date().toISOString();
newman.run({collection,environment:env,reporters:['cli'],timeoutRequest:12000,timeoutScript:3000,delayRequest:100,
  ignoreRedirects:true,insecure:false,requestAgents:{https:agent}}, (error,summary)=>{
  agent.destroy();
  if(error){console.error(error.message);process.exitCode=1;return;}
  const executions = summary.run.executions.map(e=>({
    request:e.item.name,method:e.request.method,url:e.request.url.toString(),
    http_status:e.response?.code || null,response_ms:e.response?.responseTime || null,
    response_body:e.response?.stream?.toString('utf8') || null,
    response_headers:e.response?.headers?.toJSON().filter(h=>['content-type','www-authenticate','server'].includes(h.key.toLowerCase())) || [],
    assertions:(e.assertions||[]).map(a=>({name:a.assertion,passed:!a.error,error:a.error?.message || null})),
    transport_error:e.requestError ? {code:e.requestError.code,message:e.requestError.message} : null
  }));
  const result={started_utc:started,finished_utc:new Date().toISOString(),origin:'user local PC',environment,route,
    host,connect_ip:route==='private'?'192.168.77.240':'normal DNS',tls_verification:true,
    newman_version:require(require.resolve('newman/package.json',{paths:[modulePath]})).version,
    collection:'liora-readonly.postman_collection.json',stats:summary.run.stats,
    failure_count:summary.run.failures.length,executions};
  // OpenAPI is public configuration; no login tokens, private users/items or credential headers are requested.
  fs.writeFileSync(path.join(outputDir,'results.json'),JSON.stringify(result,null,2)+'\n',{flag:'wx'});
  console.log(`RESULT: ${environment}/${route}, ${executions.length} GET requests, ${result.failure_count} failures; TLS verification enabled`);
  if(result.failure_count)process.exitCode=1;
});
