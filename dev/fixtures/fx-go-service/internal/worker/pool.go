// Package worker implementa un pool de workers concurrentes
// (trampa E04: goroutines, channels, select con timeout).
//
// Trampa P01: el counter shared 'processed' se incrementa sin
// proteccion de mutex. En concurrencia, los updates se pierden.
//
// Trampa P02: si los workers no respetan ctx.Done() en el select,
// las goroutines nunca terminan (goroutine leak).
//
// Trampa P05: el canal 'jobs' es unbuffered. Si un producer envia
// sin un receiver listo, hay deadlock.
package worker

import (
	"context"
	"sync"
	"sync/atomic"

	"fx-go-service/internal/service"
)

type Pool struct {
	jobs     chan int
	workers  int
	processed int64
	ctx      context.Context
	cancel   context.CancelFunc
	wg       sync.WaitGroup
	svc      *service.IngestService
}

func NewPool(workers int, svc *service.IngestService) *Pool {
	ctx, cancel := context.WithCancel(context.Background())
	p := &Pool{
		jobs:    make(chan int),
		workers: workers,
		ctx:    ctx,
		cancel: cancel,
		svc:     svc,
	}
	return p
}

func (p *Pool) Start() {
	for i := 0; i < p.workers; i++ {
		p.wg.Add(1)
		go p.worker()
	}
}

func (p *Pool) worker() {
	defer p.wg.Done()
	for {
		select {
		case <-p.ctx.Done():
			return
		case jobID, ok := <-p.jobs:
			if !ok {
				return
			}
			// Trampa P01: race condition en counter shared.
			p.processed++
			_ = jobID
		}
	}
}

func (p *Pool) Stop() {
	p.cancel()
	close(p.jobs)
	p.wg.Wait()
}

func (p *Pool) Submit(jobID int) {
	// Trampa P05: unbuffered channel puede causar deadlock si
	// no hay receiver. Aqui asumimos que los workers estan corriendo.
	p.jobs <- jobID
}

func (p *Pool) Processed() int64 {
	return atomic.LoadInt64(&p.processed)
}
