# Executable Scripts

This folder contains executable scripts for running the Hash Cracker project.

## Scripts

### `run.py`
Quick start script for command-line interface.

**Usage:**
```bash
python bin/run.py
```

### `demo_parallel.py`
Demonstration of parallel processing with visible Process IDs.

**Usage:**
```bash
python bin/demo_parallel.py
```

Shows:
- Each worker's Process ID (PID)
- Parent process PID
- Proof of parallel execution

### `start_web.command` (macOS/Linux)
Double-click launcher for web interface on macOS.

**Usage:**
- Double-click the file in Finder (macOS)
- Or run in terminal: `./bin/start_web.command`

### `start_web.bat` (Windows)
Double-click launcher for web interface on Windows.

**Usage:**
- Double-click the file in File Explorer
- Or run in Command Prompt: `bin\start_web.bat`

Both launchers automatically:
- Kill any existing server on port 8080
- Start web server at http://localhost:8080
- Show server logs in terminal/command prompt
