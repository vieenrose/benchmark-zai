import { tool } from "@opencode-ai/plugin"
import path from "path"
import { existsSync } from "fs"

export default tool({
    description: "List available Z.AI models that can be benchmarked",
    args: {},
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
        
        try {
            const result = await Bun.$`${cmd} --list-models`.text()
            return result
        } catch (error: any) {
            const errorMsg = error.message || ""
            if (errorMsg.includes("API key")) {
                return "Error: ZAI_API_KEY environment variable not set.\n\nSet it with:\nexport ZAI_API_KEY=your_key"
            }
            if (errorMsg.includes("not found") || errorMsg.includes("ENOENT")) {
                return `Error: benchmark-zai not found.\n\nInstall it with:\ngit clone https://github.com/vieenrose/benchmark-zai.git\ncd benchmark-zai\npython -m venv .venv && source .venv/bin/activate\npip install -e ".[dev]"`
            }
            return `Error listing models: ${errorMsg}`
        }
    },
})
