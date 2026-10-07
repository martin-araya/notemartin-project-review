// Trampa E02: blank import para registrar el driver sqlite3.
//
// El blank import ejecuta el init() del driver y lo registra en
// database/sql. La skill debe notar la linea de blank import que
// no usa el paquete pero lo carga como side effect.
package sqlite

import (
	"context"
	"database/sql"

	_ "github.com/mattn/go-sqlite3"
)

// OpenDB abre la DB SQLite con el driver registrado via init().
func OpenDB(_ context.Context, dsn string) (*sql.DB, error) {
	db, err := sql.Open("sqlite3", dsn)
	if err != nil {
		return nil, err
	}
	return db, nil
}
