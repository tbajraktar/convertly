class TerminalHelper {
    constructor() {
        this.os = 'unix'; // Default to unix (bash/zsh), toggleable to 'windows' (powershell)

        this.dangerousPatterns = [
            { pattern: /rm\s+-rf\s+\//, message: "Attempted root directory deletion." },
            { pattern: /mkfs/, message: "Attempted disk formatting." },
            { pattern: /:\(\)\{\s*:\|:&\s*\};:/, message: "Fork bomb detected (will freeze system)." },
            { pattern: /chmod\s+-R\s+777/, message: "Dangerous global permission change." },
            { pattern: /dd\s+if=/, message: "Raw disk writing operation." }
        ];

        // Heuristic Mapping (Enhance with AI API in future)
        this.commandMap = [
            // Safe
            { triggers: ['list file', 'show file', 'dir'], cmd: { unix: 'ls -la', windows: 'Get-ChildItem -Force' }, risk: 'LOW', desc: 'Lists all files in the current directory.' },
            { triggers: ['current directory', 'where am i'], cmd: { unix: 'pwd', windows: 'Get-Location' }, risk: 'LOW', desc: 'Shows the current working path.' },
            { triggers: ['print', 'echo', 'say'], cmd: { unix: 'echo "message"', windows: 'Write-Host "message"' }, risk: 'LOW', desc: 'Prints text to the console.' },

            // Medium
            { triggers: ['make folder', 'create directory', 'new folder'], cmd: { unix: 'mkdir new_folder', windows: 'New-Item -ItemType Directory -Name "new_folder"' }, risk: 'MEDIUM', desc: 'Creates a new directory.' },
            { triggers: ['create file', 'touch'], cmd: { unix: 'touch new_file.txt', windows: 'New-Item -ItemType File -Name "new_file.txt"' }, risk: 'MEDIUM', desc: 'Creates a new empty file.' },
            { triggers: ['git commit', 'save changes'], cmd: { unix: 'git commit -m "update"', windows: 'git commit -m "update"' }, risk: 'MEDIUM', desc: 'Commits staged changes to git.' },

            // High
            { triggers: ['delete folder', 'remove folder'], cmd: { unix: 'rm -rf folder_name', windows: 'Remove-Item -Recurse -Force folder_name' }, risk: 'HIGH', desc: 'Recursively deletes a folder and its contents.' },
            { triggers: ['delete file', 'remove file'], cmd: { unix: 'rm file.txt', windows: 'Remove-Item file.txt' }, risk: 'HIGH', desc: ' permanently deletes a file.' },
            { triggers: ['admin', 'sudo', 'root'], cmd: { unix: 'sudo command', windows: 'Start-Process powershell -Verb RunAs' }, risk: 'HIGH', desc: 'Executes command with elevated privileges.' },
            { triggers: ['kill', 'stop process'], cmd: { unix: 'kill -9 PID', windows: 'Stop-Process -Id PID -Force' }, risk: 'HIGH', desc: 'Forcefully terminates a process.' }
        ];
    }

    setOS(os) {
        this.os = os;
    }

    translate(input) {
        const lowerInput = input.toLowerCase();

        // 1. Direct Pattern Matching (Simple Implementation)
        const match = this.commandMap.find(item => item.triggers.some(t => lowerInput.includes(t)));

        if (match) {
            return {
                command: match.cmd[this.os] || match.cmd.unix,
                risk: match.risk,
                description: match.desc
            };
        }

        // Fallback for demo
        return {
            command: `# Unknown command: "${input}"\n# Try "list files", "delete folder", or "git commit"`,
            risk: 'LOW',
            description: 'Could not confidently translate. Please try a simpler phrase.'
        };
    }

    analyzeSafety(command) {
        for (const danger of this.dangerousPatterns) {
            if (danger.pattern.test(command)) {
                return {
                    safe: false,
                    warning: `CRITICAL WARNING: ${danger.message}`
                };
            }
        }
        return { safe: true };
    }
}

// Export
window.TerminalHelper = new TerminalHelper();
