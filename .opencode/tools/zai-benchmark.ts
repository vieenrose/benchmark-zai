import { tool } from "@opencode-ai/plugin"
import path from "path"

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
        const venvPath = path.join(context.worktree, ".venv", "bin", "benchmark-zai")
        
        let cmd = venvPath
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
            if (error.message?.includes("API key")) {
                return "Error: ZAI_API_KEY environment variable not set. Please set it before running benchmarks:\n\nexport ZAI_API_KEY=your_key"
            }
            return `Error running benchmark: ${error.message}`
        }
    },
})
