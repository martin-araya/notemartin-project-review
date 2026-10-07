// Package config carga la configuracion desde env vars.
package config

import (
	"fmt"
	"os"
	"strconv"
)

type Config struct {
	DatabaseURL string
	HTTPPort     int
	WorkerCount  int
}

// Load lee la configuracion desde env vars (con defaults).
func Load() *Config {
	c := &Config{
		DatabaseURL: getenv("DATABASE_URL", ":memory:"),
		HTTPPort:    getenvInt("HTTP_PORT", 8080),
		WorkerCount: getenvInt("WORKER_COUNT", 2),
	}
	return c
}

func getenv(key, def string) string {
	if v, ok := os.LookupEnv(key); ok {
		return v
	}
	return def
}

func getenvInt(key string, def int) int {
	v, ok := os.LookupEnv(key)
	if !ok {
		return def
	}
	n, err := strconv.Atoi(v)
	if err != nil {
		fmt.Printf("config: invalid %s=%q, using default %d\n", key, v, def)
		return def
	}
	return n
}
