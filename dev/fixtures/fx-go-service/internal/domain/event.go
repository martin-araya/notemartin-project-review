// Package domain contiene las entidades core y las interfaces del
// dominio para fx-go-service.
//
// Trampa E01: las interfaces (EventRepository, Exporter) son
// implementadas estructuralmente por SQLiteEventRepository y
// SQLiteExporter. Go NO tiene keyword 'implements'; cualquier
// struct con los metodos correctos satisface la interface.
package domain

import (
	"time"
)

type Event struct {
	ID        int64
	Type      string
	Payload   []byte
	CreatedAt time.Time
}

type Aggregate struct {
	Type        string
	Count       int64
	LastUpdated time.Time
}
