# Cursor-Test

## VS Code compile notification agent

This repo now includes a lightweight "compile done" agent you can run from VS Code.

### Files
- `scripts/compile_done_agent.py` — runs any compile/build command, streams output, and notifies when it ends.
- `.vscode/tasks.json` — adds a **Compile with notification agent** task that prompts for your compile command.

### How to use it
1. Open the folder in VS Code.
2. Run **Terminal → Run Task… → Compile with notification agent**.
3. Enter your compile command (for example: `cargo build`, `npm run build`, `dotnet build`).
4. Let it run. When done, the task:
   - Prints final status and duration in the terminal.
   - Sends a desktop notification (when OS notification tooling is available).
   - Rings a terminal bell.

### Notes
- macOS notifications use `osascript`.
- Linux notifications use `notify-send`.
- Windows notifications use a PowerShell message box fallback.
- The agent exits with the same exit code as your compile command, so task failures still fail correctly.
