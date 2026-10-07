// Tests para las 6 trampas del ecosistema (CC-06).
package tests

import (
	"os"
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func readFixtureFile(t *testing.T, rel string) string {
	t.Helper()
	data, err := os.ReadFile("../" + rel)
	require.NoError(t, err)
	return string(data)
}

func TestE01_implicit_interfaces_no_implements_keyword(t *testing.T) {
	// Trampa E01: las interfaces se implementan estructuralmente.
	// Verificamos: (a) la interface existe en domain, (b) el struct
	// en sqlite NO tiene la keyword 'implements ' (con espacio)
	// antes del nombre de la interface. La palabra "implements"
	// puede aparecer en comentarios pero no como keyword.
	domain := readFixtureFile(t, "internal/domain/repo.go")
	repo := readFixtureFile(t, "internal/repo/sqlite/sqlite.go")
	assert.Contains(t, domain, "type EventRepository interface")
	assert.Contains(t, domain, "type Exporter interface")
	// Buscamos el patron "implements " (con espacio) que seria la keyword
	// de Go 1.18+ (que en realidad no existe). Si aparece,
	// probablemente en un comentario. Filtramos comentarios.
	importsLine := ""
	for _, line := range strings.Split(repo, "\n") {
		if strings.HasPrefix(strings.TrimSpace(line), "//") {
			continue
		}
		if strings.Contains(line, "implements ") {
			importsLine = line
			break
		}
	}
	assert.Empty(t, importsLine, "SQLiteEventRepository NO debe usar 'implements'; Go usa structural typing")
}

func TestE02_init_function_and_blank_imports(t *testing.T) {
	driver := readFixtureFile(t, "internal/repo/sqlite/driver.go")
	init_ := readFixtureFile(t, "internal/repo/sqlite/init.go")
	main := readFixtureFile(t, "cmd/server/main.go")
	assert.Contains(t, driver, "func init()")
	// Blank import: Go format es `_ "package"` (underscore + quoted).
	assert.Contains(t, init_, `_ "github.com/mattn/go-sqlite3"`,
		"init.go debe tener blank import del driver sqlite3")
	// main.go tiene su propio blank import (o una asignacion equivalente).
	assert.Contains(t, main, "github.com/mattn/go-sqlite3",
		"main.go debe referenciar el driver sqlite3")
}

func TestE03_go_generate_code(t *testing.T) {
	// Trampa E03: codigo generado por sqlc con //go:generate.
	sqlcYaml := readFixtureFile(t, "sqlc.yaml")
	dbStub := readFixtureFile(t, "internal/repo/sqlc/db.go")
	assert.Contains(t, sqlcYaml, "version:")
	assert.Contains(t, dbStub, "sqlc")
	assert.Contains(t, dbStub, "NO EDITAR A MANO",
		"el stub debe documentar que se regenera con sqlc")
}

func TestE04_goroutines_channels_select(t *testing.T) {
	pool := readFixtureFile(t, "internal/worker/pool.go")
	assert.Contains(t, pool, "go p.worker()")
	assert.Contains(t, pool, "chan int")
	assert.Contains(t, pool, "select {")
	assert.Contains(t, pool, "case <-p.ctx.Done()")
	assert.Contains(t, pool, "case jobID, ok := <-p.jobs")
}

func TestE05_build_tags(t *testing.T) {
	legacy := readFixtureFile(t, "internal/http/legacy_export.go")
	assert.Contains(t, legacy, "//go:build legacy",
		"legacy_export.go debe tener build tag 'legacy'")
}

func TestE06_go_embed(t *testing.T) {
	exportSvc := readFixtureFile(t, "internal/service/export_service.go")
	assert.Contains(t, exportSvc, "//go:embed",
		"export_service.go debe usar //go:embed para templates/*.tmpl")
	assert.Contains(t, exportSvc, "templates/*.tmpl")
	assert.Contains(t, exportSvc, "embed.FS")
}

var _ = strings.Contains
