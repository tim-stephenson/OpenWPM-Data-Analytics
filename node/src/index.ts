import { Node, parse } from "acorn";
// import { static_analysis } from "./static_analysis.js";
import { createServer, ServerResponse, IncomingMessage } from "http";

const host = "localhost";
const port = 8000;

const requestListener = function (
  req: IncomingMessage,
  res: ServerResponse
): void {
  console.log(req);
  res.writeHead(200, { "Content-Type": "application/json" });
  res.end(
    JSON.stringify({
      data: "Hello World!",
    })
  );
};

const server = createServer(requestListener);
server.listen(port, host, () => {
  console.log(`Server is running on http://${host}:${port}`);
});

// const code: string = process.argv[2];

const code: string = "";
const result: Node = parse(code, {
  ecmaVersion: 2022,
  sourceType: "script",
});

// process.exitCode = static_analysis(result) ? 1 : 0;
