import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const execFileAsync = promisify(execFile);
const scriptDir = dirname(fileURLToPath(import.meta.url));

export default function (api) {
  api.registerCommand({
    name: "hello",
    description: "Returns a friendly greeting.",
    acceptsArgs: true,
    handler: async (ctx) => {
      const scriptPath = join(scriptDir, "hello.sh");
      const args = ctx.args?.trim() ? [ctx.args.trim()] : [];
      const { stdout } = await execFileAsync("bash", [scriptPath, ...args]);
      return { text: `the call to ./hello.sh returned: ${stdout.trim()}` };
    },
  });
}
