// Cliente MCP simulado en proceso.
// En produccion usaria el SDK real; aqui expone 2 herramientas fake
// (``fs.read`` y ``fs.list``) sin red.

export interface MCPToolDef {
  name: string;
  description: string;
  parameters: Record<string, string>;
}

export interface MCPClient {
  connect(url: string): Promise<void>;
  listTools(): MCPToolDef[];
  callTool(name: string, args: Record<string, unknown>): Promise<unknown>;
  close(): void;
}

class SimulatedMCPClient implements MCPClient {
  private _connected = false;
  private _url = "";
  private _tools: MCPToolDef[] = [
    {
      name: "fs.read",
      description: "Read a file (simulated MCP).",
      parameters: { path: "string" },
    },
    {
      name: "fs.list",
      description: "List a directory (simulated MCP).",
      parameters: { path: "string" },
    },
  ];

  async connect(url: string): Promise<void> {
    this._url = url;
    this._connected = true;
  }

  listTools(): MCPToolDef[] {
    if (!this._connected) throw new Error("MCP client not connected");
    return [...this._tools];
  }

  async callTool(name: string, args: Record<string, unknown>): Promise<unknown> {
    if (!this._connected) throw new Error("MCP client not connected");
    switch (name) {
      case "fs.read":
        return { content: `<simulated read of ${args.path}>` };
      case "fs.list":
        return { entries: ["a.txt", "b.md"] };
      default:
        throw new Error(`MCP tool not found: ${name}`);
    }
  }

  close(): void {
    this._connected = false;
    this._url = "";
  }
}

export function createMCPClient(): MCPClient {
  return new SimulatedMCPClient();
}
