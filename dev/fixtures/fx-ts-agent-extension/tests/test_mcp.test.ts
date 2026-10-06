import { describe, it, expect, beforeEach } from "vitest";
import { createMCPClient, type MCPClient } from "../src/host/mcp/client.js";

describe("MCP client simulado", () => {
  let mcp: MCPClient;

  beforeEach(() => {
    mcp = createMCPClient();
  });

  it("lanza si se llama sin connect", () => {
    expect(() => mcp.listTools()).toThrow();
  });

  it("listTools devuelve 2 herramientas despues de connect", async () => {
    await mcp.connect("mcp://localhost:9999");
    const tools = mcp.listTools();
    expect(tools.length).toBe(2);
  });

  it("expone fs.read y fs.list", async () => {
    await mcp.connect("mcp://x");
    const names = mcp.listTools().map((t) => t.name);
    expect(names).toContain("fs.read");
    expect(names).toContain("fs.list");
  });

  it("callTool fs.read devuelve contenido simulado", async () => {
    await mcp.connect("mcp://x");
    const r = await mcp.callTool("fs.read", { path: "/etc/passwd" });
    expect((r as any).content).toContain("/etc/passwd");
  });

  it("callTool fs.list devuelve entradas", async () => {
    await mcp.connect("mcp://x");
    const r = await mcp.callTool("fs.list", { path: "/" });
    expect((r as any).entries).toEqual(["a.txt", "b.md"]);
  });

  it("callTool con tool desconocida lanza", async () => {
    await mcp.connect("mcp://x");
    await expect(mcp.callTool("nope", {})).rejects.toThrow();
  });

  it("callTool sin connect lanza", async () => {
    await expect(mcp.callTool("fs.read", { path: "/" })).rejects.toThrow();
  });

  it("close desactiva la conexion", async () => {
    await mcp.connect("mcp://x");
    mcp.close();
    expect(() => mcp.listTools()).toThrow();
  });

  it("cada herramienta tiene name, description, parameters", async () => {
    await mcp.connect("mcp://x");
    for (const t of mcp.listTools()) {
      expect(t.name).toBeDefined();
      expect(t.description.length).toBeGreaterThan(0);
      expect(typeof t.parameters).toBe("object");
    }
  });

  it("los parametros son strings (tipos)", async () => {
    await mcp.connect("mcp://x");
    const t = mcp.listTools().find((x) => x.name === "fs.read");
    expect(t?.parameters.path).toBe("string");
  });
});
