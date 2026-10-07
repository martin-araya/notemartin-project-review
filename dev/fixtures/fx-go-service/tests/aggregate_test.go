// Tests para el feature de aggregate.
package tests

import (
	"context"
	"testing"

	"fx-go-service/internal/domain"
	"fx-go-service/internal/service"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestAggregate_compute_with_no_events_returns_empty(t *testing.T) {
	_, repo := setupDB(t)
	svc := service.NewAggregateService(repo)
	agg, err := svc.Compute(context.Background())
	require.NoError(t, err)
	assert.Empty(t, agg)
}

func TestAggregate_compute_with_three_types_returns_three(t *testing.T) {
	_, repo := setupDB(t)
	ingest := service.NewIngestService(repo)
	svc := service.NewAggregateService(repo)
	ctx := context.Background()
	require.NoError(t, ingest.Ingest(ctx, &domain.Event{Type: "user.created", Payload: []byte(`{}`)}))
	require.NoError(t, ingest.Ingest(ctx, &domain.Event{Type: "user.deleted", Payload: []byte(`{}`)}))
	require.NoError(t, ingest.Ingest(ctx, &domain.Event{Type: "order.placed", Payload: []byte(`{}`)}))

	agg, err := svc.Compute(ctx)
	require.NoError(t, err)
	assert.Len(t, agg, 3)
}

func TestAggregate_compute_groups_by_type_correctly(t *testing.T) {
	_, repo := setupDB(t)
	ingest := service.NewIngestService(repo)
	svc := service.NewAggregateService(repo)
	ctx := context.Background()
	for i := 0; i < 5; i++ {
		require.NoError(t, ingest.Ingest(ctx, &domain.Event{Type: "page.view", Payload: []byte(`{}`)}))
	}
	agg, err := svc.Compute(ctx)
	require.NoError(t, err)
	for _, a := range agg {
		if a.Type == "page.view" {
			assert.Equal(t, int64(5), a.Count)
			return
		}
	}
	t.Fatal("page.view not found in aggregates")
}
