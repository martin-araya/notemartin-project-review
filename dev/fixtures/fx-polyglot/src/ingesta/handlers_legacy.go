// Handler `legacy` con campos distintos: {id, ts_raw, body} en lugar de {id, ts, raw, tag}.
// Compilado solo con `-tags legacy` (trampa #2 del ecosistema: //go:build tags).
//go:build legacy
// +build legacy

package main

import (
	"fmt"
	"strings"
)

func init() {
	handlers["legacy"] = func(line string) (map[string]interface{}, error) {
		parts := strings.SplitN(line, "|", 3)
		if len(parts) < 3 {
			return nil, fmt.Errorf("formato invalido: esperado id|ts|raw")
		}
		return map[string]interface{}{
			"id":     parts[0],
			"ts_raw": parts[1],
			"body":   parts[2],
		}, nil
	}
}