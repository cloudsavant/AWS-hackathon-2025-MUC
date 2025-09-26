# Claude Code Configuration

## MCP Servers

Configure MCP servers to extend Claude Code's capabilities with custom tools and integrations.

### Example MCP Server Configuration

```json
{
  "mcpServers": {
    "example-server": {
      "command": "npx",
      "args": ["@example/mcp-server"],
      "env": {
        "API_KEY": "your-api-key-here"
      }
    }
  }
}
```

## Project Context

This is a travel planning AI application built for AWS hackathon using Bedrock AgentCore.

## Commands

- Build: `npm run build` (if applicable)
- Test: `npm test` (if applicable)
- Dev: `npm run dev` (if applicable)