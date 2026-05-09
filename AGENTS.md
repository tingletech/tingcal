# Agents

## Commands

- **Run the CLI**: `uv run tingcal <start> <end> [--zodiac] [--lunar] [--server] [--port PORT]`
- **Run as module**: `uv run python -m tingcal <start> <end>`
- **Install in dev mode**: `uv sync`
- **Add dependency**: `uv add <package>`

## Code style

- No comments in code
- Follow existing patterns
- Use standard library where possible (only `ephem` as external dependency)
