# Claude Code Configuration

## MCP Servers

Configure MCP servers to extend Claude Code's capabilities with custom tools and integrations.

### AWS Documentation MCP Server Configuration

The AWS documentation MCP server has been configured in the following files:

#### `.mcp.json`
```json
{
  "mcpServers": {
    "awslabs.aws-documentation-mcp-server": {
      "command": "uvx",
      "args": ["awslabs.aws-documentation-mcp-server@latest"],
      "env": {
        "FASTMCP_LOG_LEVEL": "ERROR",
        "AWS_DOCUMENTATION_PARTITION": "aws"
      },
      "disabled": false
    }
  }
}
```

#### `.claude/settings.local.json`
```json
{
  "enabledMcpjsonServers": [
    "awslabs.aws-documentation-mcp-server"
  ]
}
```

**Setup Status**: ✅ Configured and ready to use

This MCP server provides:
- AWS documentation search and retrieval
- Content recommendations
- Service documentation access
- Perfect for your AWS Bedrock AgentCore travel planner project

**Note**: Restart Claude Code for the MCP server to become available.

## Project Context

This is a travel planning AI application built for AWS hackathon using Bedrock AgentCore.

## Commands

- Build: `npm run build` (if applicable)
- Test: `npm test` (if applicable)
- Dev: `npm run dev` (if applicable)