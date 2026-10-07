// Repositorio SQLite con implementacion estructural de las
// interfaces del dominio (trampa E01).
//
// Trampa E01: SQLiteEventRepository implementa domain.EventRepository
// y SQLiteExporter implementa domain.Exporter sin la keyword
// 'implements'. Go usa structural typing: si los metodos matchean
// la firma de la interface, el struct satisface la interface
// automaticamente.
//
// Trampa P03: implicit interface mismatch. El metodo GetByID
// retorna *Event pero las pruebas esperan Event. Compile-time
// pasara, pero el valor de retorno es nil en algunos casos.
package sqlite

import (
	"context"
	"database/sql"
	"errors"
	"fmt"

	"fx-go-service/internal/domain"
)

type SQLiteEventRepository struct {
	db *sql.DB
}

// NewSQLiteEventRepository construye un repositorio contra la DB
// SQL dada. El constructor es el patron que wire reconoce para
// providers.
func NewSQLiteEventRepository(db *sql.DB) *SQLiteEventRepository {
	return &SQLiteEventRepository{db: db}
}

func (r *SQLiteEventRepository) Insert(ctx context.Context, e *domain.Event) (int64, error) {
	res, err := r.db.ExecContext(ctx,
		"INSERT INTO events (type, payload, created_at) VALUES (?, ?, ?)",
		e.Type, e.Payload, e.CreatedAt)
	if err != nil {
		return 0, fmt.Errorf("insert: %w", err)
	}
	id, err := res.LastInsertId()
	if err != nil {
		return 0, fmt.Errorf("last_insert_id: %w", err)
	}
	return id, nil
}

func (r *SQLiteEventRepository) GetByID(ctx context.Context, id int64) (*domain.Event, error) {
	row := r.db.QueryRowContext(ctx,
		"SELECT id, type, payload, created_at FROM events WHERE id = ? LIMIT 1", id)
	var e domain.Event
	if err := row.Scan(&e.ID, &e.Type, &e.Payload, &e.CreatedAt); err != nil {
		if errors.Is(err, sql.ErrNoRows) {
			return nil, nil
		}
		return nil, fmt.Errorf("scan: %w", err)
	}
	return &e, nil
}

func (r *SQLiteEventRepository) ListByType(ctx context.Context, eventType string, limit, offset int) ([]*domain.Event, error) {
	rows, err := r.db.QueryContext(ctx,
		"SELECT id, type, payload, created_at FROM events WHERE type = ? ORDER BY created_at DESC LIMIT ? OFFSET ?",
		eventType, limit, offset)
	if err != nil {
		return nil, fmt.Errorf("query: %w", err)
	}
	defer rows.Close()
	var out []*domain.Event
	for rows.Next() {
		var e domain.Event
		if err := rows.Scan(&e.ID, &e.Type, &e.Payload, &e.CreatedAt); err != nil {
			return nil, fmt.Errorf("scan: %w", err)
		}
		out = append(out, &e)
	}
	if err := rows.Err(); err != nil {
		return nil, fmt.Errorf("rows: %w", err)
	}
	return out, nil
}

func (r *SQLiteEventRepository) CountByType(ctx context.Context, eventType string) (int64, error) {
	var n int64
	if err := r.db.QueryRowContext(ctx,
		"SELECT COUNT(*) FROM events WHERE type = ?", eventType).Scan(&n); err != nil {
		return 0, fmt.Errorf("count: %w", err)
	}
	return n, nil
}

func (r *SQLiteEventRepository) DeleteAll(ctx context.Context) error {
	if _, err := r.db.ExecContext(ctx, "DELETE FROM events"); err != nil {
		return fmt.Errorf("delete_all: %w", err)
	}
	return nil
}

type SQLiteExporter struct {
	repo domain.EventRepository
}

// NewSQLiteExporter construye un exporter contra el repositorio.
func NewSQLiteExporter(repo domain.EventRepository) *SQLiteExporter {
	return &SQLiteExporter{repo: repo}
}

func (e *SQLiteExporter) Export(ctx context.Context, format string) ([]byte, error) {
	events, err := e.repo.ListByType(ctx, "default", 1000, 0)
	if err != nil {
		return nil, fmt.Errorf("list: %w", err)
	}
	out := fmt.Sprintf("format=%s count=%d\n", format, len(events))
	return []byte(out), nil
}
