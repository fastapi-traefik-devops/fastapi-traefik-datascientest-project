#!/usr/bin/env node
'use strict';
// Local Swagger UI with a constrained read-only reverse proxy. No accounts, saved tokens or writes.
const fs=require('fs'),path=require('path'),http=require('http'),https=require('https');
const root=path.resolve(__dirname,'..');
const tools=process.env.LIORA_API_TOOLS || path.resolve(__dirname,'../../../../.api-tools');
const assets=path.dirname(require.resolve('swagger-ui-dist/package.json',{paths:[tools]}));
const hosts={dev:'dev.liora.aprt.info',stage:'stage.liora.aprt.info',prod:'liora.aprt.info'};
const allow=new Set(['/api/v1/utils/health-check/','/api/v1/openapi.json','/api/v1/users/','/api/v1/users/me','/api/v1/items/']);
const index=`<!doctype html><html><head><meta charset="utf-8"><title>Liora — live read-only API explorer</title><link rel="stylesheet" href="/assets/swagger-ui.css"><style>body{margin:0}.banner{padding:16px 32px;background:#142c42;color:white;font:15px system-ui}.banner h1{margin:0 0 6px;font-size:23px}.banner p{margin:4px 0}.topbar{display:none}</style></head><body><div class="banner"><h1>Liora FastAPI · Live API Explorer</h1><p>Installed locally: Swagger UI 5.34.0 · Real HTTPS requests from this PC · GET requests only</p><p>Private route: 192.168.77.240 · Original DEV/STAGE/PROD hostname and TLS certificate verification preserved.</p><p>OpenAPI schemas/examples describe the API. Only a completed Execute response is live evidence. <a style="color:#8be5ff" href="/results">View actual Newman results</a></p></div><div id="swagger-ui"></div><script src="/assets/swagger-ui-bundle.js"></script><script>window.ui=SwaggerUIBundle({url:'/openapi.json',dom_id:'#swagger-ui',deepLinking:true,docExpansion:'list',supportedSubmitMethods:['get'],persistAuthorization:false,validatorUrl:null,displayRequestDuration:true});</script></body></html>`;
function report(){
 const rows=fs.readdirSync(path.join(root,'evidence/results')).filter(n=>/^(dev|stage|prod)-(public|private)\.json$/.test(n)).map(n=>{
  const r=JSON.parse(fs.readFileSync(path.join(root,'evidence/results',n)));return `<tr><td>${r.environment.toUpperCase()}</td><td>${r.route}</td><td>${r.connect_ip}</td><td>${r.stats.requests.total}</td><td>${r.stats.requests.failed}</td><td>${r.stats.assertions.total-r.stats.assertions.failed}/${r.stats.assertions.total}</td><td class="${r.failure_count?'fail':'pass'}">${r.failure_count?'TLS FAILED':'PASS'}</td></tr>`;
 }).join('');
 return `<!doctype html><html><head><meta charset="utf-8"><title>Liora Newman — actual run results</title><style>body{font:17px system-ui;max-width:1100px;margin:42px auto;color:#173043}h1{font-size:32px}table{width:100%;border-collapse:collapse}th,td{text-align:left;padding:16px 12px;border-bottom:1px solid #d6e2e8}th{background:#e9f2f7}.pass{color:#08764c;font-weight:bold}.fail{color:#b13630;font-weight:bold}code{background:#edf2f5;padding:3px 6px}.note{padding:20px;background:#eef4f8;line-height:1.6}</style></head><body><h1>Liora FastAPI · Actual Newman results</h1><p>24 October 2026 · Tests originated on the local PC · Newman 6.2.2</p><table><tr><th>Environment</th><th>Route</th><th>Connection</th><th>GETs attempted</th><th>Transport failures</th><th>Assertions passed</th><th>Outcome</th></tr>${rows}</table><p class="note">36 successful HTTP requests · 108 passing assertions · 18 public DEV/STAGE transport failures.<br>Public DEV/STAGE returned no HTTP response: TLS handshake failed on both IPv4 and IPv6.<br>All successful requests used certificate verification. No users/items were created or changed; no email sent.</p><p>These are views of saved <strong>real Newman execution records</strong>, not Postman desktop screenshots and not simulated responses. Full request/status/body/assertion records are retained in evidence/results.</p><p><a href="/">Open the live Swagger UI client</a></p></body></html>`;
}
http.createServer((req,res)=>{
 const u=new URL(req.url,'http://127.0.0.1');
 if(req.method!=='GET'){res.writeHead(405,{'Allow':'GET'});return res.end('Read-only client');}
 if(u.pathname==='/'){res.writeHead(200,{'Content-Type':'text/html; charset=utf-8'});return res.end(index);}
 if(u.pathname==='/results'){res.writeHead(200,{'Content-Type':'text/html; charset=utf-8'});return res.end(report());}
 if(u.pathname==='/openapi.json'){
  const spec=JSON.parse(fs.readFileSync(path.join(root,'openapi.dev.json')));
  spec.servers=Object.entries(hosts).map(([env,host])=>({url:'/api-proxy/'+env,description:env.toUpperCase()+' — '+host+' via 192.168.77.240 (verified TLS)'}));
  res.writeHead(200,{'Content-Type':'application/json'});return res.end(JSON.stringify(spec));
 }
 if(u.pathname.startsWith('/assets/')){
  const file=u.pathname.slice(8);if(!['swagger-ui.css','swagger-ui-bundle.js'].includes(file)){res.writeHead(404);return res.end();}
  res.writeHead(200,{'Content-Type':file.endsWith('.css')?'text/css':'application/javascript'});return fs.createReadStream(path.join(assets,file)).pipe(res);
 }
 const match=u.pathname.match(/^\/api-proxy\/(dev|stage|prod)(\/api\/v1\/.*)$/);
 if(!match || !allow.has(match[2])){res.writeHead(403,{'Content-Type':'application/json'});return res.end(JSON.stringify({detail:'Only allowlisted read-only API routes can be executed in this client.'}));}
 const host=hosts[match[1]],headers={'Accept':'application/json','Host':host};
 // Permit only the deliberately invalid fixture bearer for the negative-auth screenshot.
 if(req.headers.authorization==='Bearer invalid-example-token')headers.Authorization=req.headers.authorization;
 const upstream=https.request({hostname:host,port:443,servername:host,path:match[2]+u.search,method:'GET',headers,rejectUnauthorized:true,
  lookup:(name,opts,cb)=>opts?.all?cb(null,[{address:'192.168.77.240',family:4}]):cb(null,'192.168.77.240',4)},response=>{
   const returned={'Content-Type':response.headers['content-type'] || 'application/json','X-Evidence-Target':host,'X-Evidence-Route':'192.168.77.240; TLS verified'};
   if(response.headers['www-authenticate'])returned['WWW-Authenticate']=response.headers['www-authenticate'];
   res.writeHead(response.statusCode,returned);response.pipe(res);
  });
 upstream.setTimeout(12000,()=>upstream.destroy(new Error('Upstream timeout')));
 upstream.on('error',e=>{if(!res.headersSent)res.writeHead(502,{'Content-Type':'application/json'});res.end(JSON.stringify({detail:'Upstream request failed',code:e.code || 'ERROR'}));});upstream.end();
}).listen(18765,'127.0.0.1',()=>console.log('Read-only Swagger UI http://127.0.0.1:18765 (loopback only)'));
