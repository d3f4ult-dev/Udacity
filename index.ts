const PORT = process.env.PORT ? Number(process.env.PORT) : 3000;

function getContentType(filename: string): string {
  if (filename.endsWith(".svg")) return "image/svg+xml";
  if (filename.endsWith(".css")) return "text/css";
  if (filename.endsWith(".js")) return "application/javascript";
  return "application/octet-stream";
}

const server = Bun.serve({
  port: PORT,
  fetch(req: Request) {
    const url = new URL(req.url);

    // Serve static CSS
    if (url.pathname === "/styles.css") {
      const file = Bun.file("styles.css");
      return new Response(file, {
        headers: { "Content-Type": "text/css" }
      });
    }

    
    // Serve static JS
    if (url.pathname === "/script.js") {
        const file = Bun.file("script.js");
        return new Response(file, {
            headers: { "Content-Type": "application/javascript" }
        });
    }
    
    // Serve pixel-art assets
    if (url.pathname.startsWith("/pixel-art/")) {
        const filename = url.pathname.replace(/^\/pixel-art\//, "");
        const file = Bun.file(`pixel-art/${filename}`);
        const contentType = getContentType(filename);
        return new Response(file, {
            headers: { "Content-Type": contentType }
        });
    }
    
    // Serve Static installing.htm
    if (url.pathname === "/installing.htm") {
      const file = Bun.file("installing.htm");
      return new Response(file, {
        headers: { "Content-Type": "text/html" }
      });
    }

    // Fallback: serve index.html
    const file = Bun.file("index.html");
    return new Response(file, {
      headers: { "Content-Type": "text/html" }
    });
  }
});

console.log(`🚀 Server running at http://localhost:${server.port}`);
