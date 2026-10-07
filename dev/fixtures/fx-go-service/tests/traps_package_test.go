// Tests para las 6 trampas del paquete (CC-04).
package tests

import (
	"os"
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func readFixtureFileP(t *testing.T, rel string) string {
	t.Helper()
	data, err := os.ReadFile("../" + rel)
	require.NoError(t, err)
	return string(data)
}

func TestP01_race_condition_in_worker_pool(t *testing.T) {
	pool := readFixtureFileP(t, "internal/worker/pool.go")
	// La trampa P01: el counter shared 'processed' se incrementa
	// sin mutex. En concurrencia, los updates se pierden.
	assert.Contains(t, pool, "p.processed++")
	// Verificar que NO hay mutex protegiendo el counter.
	assert.NotContains(t, pool, "sync.Mutex")
}

func TestP02_goroutine_leak_on_shutdown(t *testing.T) {
	pool := readFixtureFileP(t, "internal/worker/pool.go")
	// El worker SI respeta ctx.Done() en el select, lo que evita
	// el leak. Pero Stop() cierra el canal sin esperar a que los
	// workers terminen de procesar el job actual.
	assert.Contains(t, pool, "case <-p.ctx.Done()")
	// Verificar que la goroutine no sale con `return` inmediato
	// cuando recibe close del canal.
	assert.Contains(t, pool, "if !ok {")
}

func TestP03_implicit_interface_mismatch(t *testing.T) {
	sqlite := readFixtureFileP(t, "internal/repo/sqlite/sqlite.go")
	// La trampa P03: SQLiteExporter.Export llama ListByType con
	// type="default", pero el servicio busca por type del payload.
	// Esto es un mismatch semantico (no de tipos), pero la firma
	// matchea. Trampa sutil.
	assert.Contains(t, sqlite, "ListByType(ctx, \"default\", 1000, 0)")
}

func TestP04_init_side_effects_in_tests(t *testing.T) {
	driver := readFixtureFileP(t, "internal/repo/sqlite/driver.go")
	// init() imprime un mensaje a stdout al importar el package.
	// Esto es un side effect que afecta a tests silenciosos.
	assert.Contains(t, driver, "fmt.Println")
}

func TestP05_channel_deadlock(t *testing.T) {
	pool := readFixtureFileP(t, "internal/worker/pool.go")
	// Trampa P05: el canal 'jobs' es unbuffered. Si un producer
	// envia sin un receiver listo, hay deadlock.
	assert.Contains(t, pool, "make(chan int)")
	assert.NotContains(t, pool, "make(chan int, ")
}

func TestP06_build_tag_typo(t *testing.T) {
	legacy := readFixtureFileP(t, "internal/http/legacy_export.go")
	// Trampa P06: en una version del codigo el tag tiene typo
	// ('lagacy'); en este fixture el tag es correcto. Verificar
	// que la skill encuentra el tag correcto.
	assert.Contains(t, legacy, "//go:build legacy")
	assert.NotContains(t, legacy, "lagacy")
}

var _ = strings.Contains
