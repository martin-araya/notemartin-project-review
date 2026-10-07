// Tests para las 3 trampas superficiales (CC-05).
package tests

import (
	"os"
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func readFixtureFileS(t *testing.T, rel string) string {
	t.Helper()
	data, err := os.ReadFile("../" + rel)
	require.NoError(t, err)
	return string(data)
}

func TestS01_dead_legacy_export_go(t *testing.T) {
	legacy := readFixtureFileS(t, "internal/http/legacy_export.go")
	assert.Contains(t, legacy, "//go:build legacy")
	assert.Contains(t, legacy, "LegacyExportHandler")
}

func TestS02_dead_legacy_binary(t *testing.T) {
	legacy := readFixtureFileS(t, "cmd/legacy/main.go")
	assert.Contains(t, legacy, "fx-go-service legacy binary - deprecated")
}

func TestS03_dead_debug_helper(t *testing.T) {
	debug := readFixtureFileS(t, "internal/debug.go")
	assert.Contains(t, debug, "func DebugPrintln")
	// Verificar que no se invoca en produccion.
	main := readFixtureFileS(t, "cmd/server/main.go")
	assert.NotContains(t, main, "DebugPrintln",
		"DebugPrintln no debe invocarse en el entry point de produccion")
}

var _ = strings.Contains
