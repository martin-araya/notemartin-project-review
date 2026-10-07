// Trampa E02: init() registra el driver sqlite3 con database/sql.
//
// El driver de mattn/go-sqlite3 ya se auto-registra via init() en
// su propio package; este init() es explicito y solo para
// documentacion. La trampa: cualquier import de este package
// (incluso via _ "...") ejecuta init() como side effect.
package sqlite

import (
	"database/sql"
	"fmt"

	_ "github.com/mattn/go-sqlite3"
)

func init() {
	// Trampa E02: el driver se auto-registra via init() del package
	// mattn/go-sqlite3 al importarse (blank import). Aqui NO es
	// necesario, pero documenta la trampa.
	drivers := sql.Drivers()
	_ = drivers // suprime warning
	fmt.Println("[fx-go-service] sqlite driver registered")
}
