import { describe, it, expect, beforeEach } from "vitest";
import { t, setLocale, getLocale, hasKey, resetI18n } from "../src/host/i18n.js";

describe("i18n", () => {
  beforeEach(() => {
    resetI18n();
  });

  it("locale por defecto es en", () => {
    expect(getLocale()).toBe("en");
  });

  it("t() devuelve el valor en en por defecto", () => {
    expect(t("mode.plan.title")).toBe("Plan");
  });

  it("t() cambia con setLocale('es')", () => {
    setLocale("es");
    expect(t("mode.plan.title")).toBe("Plan"); // "Plan" en ambos idiomas
    expect(t("error.tool_denied")).toContain("denego"); // en espanol
  });

  it("t() con clave inexistente devuelve la clave", () => {
    expect(t("nonexistent.key")).toBe("nonexistent.key");
  });

  it("t() reemplaza variables {var}", () => {
    const r = t("context.condensed", { removed: 5 });
    expect(r).toContain("5");
  });

  it("hasKey reconoce claves existentes", () => {
    expect(hasKey("mode.plan.title")).toBe(true);
    expect(hasKey("nonexistent.key")).toBe(false);
  });

  it("resetI18n vuelve a en", () => {
    setLocale("es");
    resetI18n();
    expect(getLocale()).toBe("en");
  });

  it("t() soporta dot-path completo", () => {
    expect(t("tool.read_file.label")).toBe("Read file");
  });

  it("t() en es devuelve etiquetas en espanol", () => {
    setLocale("es");
    expect(t("tool.read_file.label")).toBe("Leer archivo");
  });
});

describe("ecosystem trap #5: claves i18n construidas en runtime", () => {
  it("t(`mode.${id}.title`) funciona para los 3 modos", () => {
    for (const id of ["plan", "code", "ask"]) {
      const key = `mode.${id}.title`;
      const value = t(key);
      expect(value.length).toBeGreaterThan(0);
    }
  });

  it("t(`tool.${name}.label`) funciona para los 6 tools", () => {
    for (const name of ["read_file", "list_dir", "search_code", "run_terminal_cmd", "ask_user", "propose_plan"]) {
      const key = `tool.${name}.label`;
      const value = t(key);
      expect(value.length).toBeGreaterThan(0);
    }
  });

  it("t() no aparece como literal en el codigo (el scanner no las encuentra)", () => {
    // Las claves construidas como ``t(`mode.${id}.title`)`` no son strings
    // literales; un grep sobre el codigo fuente no las encuentra.
    // Este test documenta la trampa: el scanner debe ver el patron
    // template literal y razonar sobre el.
    expect(typeof t("mode.plan.title")).toBe("string");
  });
});
