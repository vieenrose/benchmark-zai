import { tool } from "@opencode-ai/plugin"
import path from "path"

export default tool({
    description: "List available Z.AI models that can be benchmarked",
    args: {},
    async execute(args, context) {
        const venvPath = path.join(context.worktree, ".venv", "bin", "benchmark-zai")
        
        try {
            const result = await Bun.$`${venvPath} --list-models`.text()
            return result
        } catch (error: any) {
            if (error.message?.includes("API key")) {
                return "Error: ZAI_API_KEY environment variable not set. Please set it first:\n\nexport ZAI_API_KEY=your_key"
            }
            return `Error listing models: ${error.message}`
        }
    },
})
