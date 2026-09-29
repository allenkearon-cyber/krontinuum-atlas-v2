const http=require("http");
const fs=require("fs");
const path=require("path");
const port=process.env.PORT||3000;
const index=path.join(__dirname,"index.html");
const server=http.createServer((req,res)=>{
  const u=(req.url||"/").split("?")[0];
  const headers={
    "X-Content-Type-Options":"nosniff",
    "Referrer-Policy":"no-referrer",
    "Permissions-Policy":"camera=(), microphone=(), geolocation=()",
    "Cross-Origin-Resource-Policy":"same-origin",
    "Cache-Control":"public, max-age=300"
  };
  if(u==="/healthz"){res.writeHead(200,{...headers,"Content-Type":"text/plain"});return res.end("ok");}
  if(u!=="/"&&u!=="/index.html"){res.writeHead(404,{...headers,"Content-Type":"text/plain"});return res.end("not found");}
  fs.readFile(index,(err,data)=>{
    if(err){res.writeHead(500,{...headers,"Content-Type":"text/plain"});return res.end("server error");}
    res.writeHead(200,{...headers,"Content-Type":"text/html; charset=utf-8","Content-Disposition":"inline"});
    res.end(data);
  });
});
server.listen(port,"0.0.0.0",()=>console.log("Atlas v2 listening on",port));