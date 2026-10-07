-- name: CreateEvent :execresult
INSERT INTO events (type, payload, created_at) VALUES (?, ?, ?);

-- name: GetEvent :one
SELECT id, type, payload, created_at FROM events WHERE id = ? LIMIT 1;

-- name: ListEventsByType :many
SELECT id, type, payload, created_at FROM events WHERE type = ? ORDER BY created_at DESC LIMIT ? OFFSET ?;

-- name: CountEventsByType :one
SELECT COUNT(*) FROM events WHERE type = ?;

-- name: DeleteAllEvents :execresult
DELETE FROM events;
