import { tool } from "@opencode-ai/plugin"
import path from "path"
import { existsSync } from "fs"

export default tool({
    description: "Run Z.AI model benchmark to measure TTFT, generation speed, and latency",
    args: {
        models: tool
            .schema
            .string()
            .optional()
            .describe("Comma-separated model list (e.g., 'glm-5,glm-4.7'). Default: all available models"),
        runs: tool
            .schema
            .number()
            .optional()
            .describe("Number of benchmark runs per model. Default: 3"),
        max_tokens: tool
            .schema
            .number()
            .optional()
            .describe("Maximum tokens to generate. Default: 256"),
        output: tool
            .schema
            .enum(["table", "json"])
            .optional()
            .describe("Output format. Default: table"),
    },
    async execute(args, context) {
        // Try to find benchmark-zai in multiple locations
        let cmd = "benchmark-zai"
        const possiblePaths = [
            path.join(context.worktree, ".venv", "bin", "benchmark-zai"),
            path.join(context.directory, ".venv", "bin", "benchmark-zai"),
            "/usr/local/bin/benchmark-zai",
            path.join(process.env.HOME || "", ".local", "bin", "benchmark-zai"),
        ]
        
        for (const p of possiblePaths) {
            if (existsSync(p)) {
                cmd = p
                break
            }
        }
        
        const cmdArgs: string[] = []
        
        if (args.models) {
            cmdArgs.push("--models", args.models)
        }
        if (args.runs) {
            cmdArgs.push("--runs", String(args.runs))
        }
        if (args.max_tokens) {
            cmdArgs.push("--max-tokens", String(args.max_tokens))
        }
        if (args.output) {
            cmdArgs.push("--output", args.output)
        }
        
        try {
            const result = await Bun.$`${cmd} ${cmdArgs}`.text()
            return result
        } catch (error: any) {
            const errorMsg = error.message || ""
            if (errorMsg.includes("API key")) {
                return "Error: ZAI_API_KEY environment variable not set.\n\nSet it with:\nexport ZAI_API_KEY=your_key"
            }
            if (errorMsg.includes("not found") || errorMsg.includes("ENOENT")) {
                return `Error: benchmark-zai not found.\n\nInstall it with:\ngit clone https://github.com/vieenrose/benchmark-zai.git\ncd benchmark-zai\npython -m venv .venv && source .venv/bin/activate\npip install -e ".[dev]"\n\nOr run from the benchmark-zai project directory.`
            }
            return `Error running benchmark: ${errorMsg}`
        }
    },
})
