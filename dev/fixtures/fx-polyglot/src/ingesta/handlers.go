// Handlers `current` y vacio. Compilados por defecto.
//go:build !legacy
// +build !legacy

package main

import (
	"fmt"
	"strings"
)

func init() {
	handlers["current"] = func(line string) (map[string]interface{}, error) {
		parts := strings.SplitN(line, "|", 3)
		if len(parts) < 3 {
			return nil, fmt.Errorf("formato invalido: esperado id|ts|raw")
		}
		return map[string]interface{}{
			"id":  parts[0],
			"ts":  parts[1],
			"raw": parts[2],
			"tag": "current",
		}, nil
	}
}