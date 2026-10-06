// Package main implementa la CLI del F06f.
// Lee lineas de stdin en formato `id|ts|raw` y emite JSON por stdout, una linea
// por cada linea de entrada. El formato del JSON depende de la tag seleccionada
// (current por defecto; legacy con `-tags legacy`).
//
// La inicializacion de los handlers ocurre en registry.go (trampa #4 del ecosistema).
package main

import (
	"bufio"
	"encoding/json"
	"flag"
	"fmt"
	"os"
	"strings"
)

// Handler convierte una linea de stdin en un mapa JSON.
type Handler func(line string) (map[string]interface{}, error)

func main() {
	listTags := flag.Bool("list-tags", false, "Imprime los handlers disponibles y sale.")
	tag := flag.String("tag", "current", "Tag del handler a usar.")
	flag.Parse()

	if *listTags {
		names := make([]string, 0, len(handlers))
		for n := range handlers {
			names = append(names, n)
		}
		for _, n := range names {
			fmt.Fprintln(os.Stdout, n)
		}
		return
	}

	h, ok := handlers[*tag]
	if !ok {
		fmt.Fprintf(os.Stderr, "tag desconocida: %s (exit 4)\n", *tag)
		os.Exit(4)
	}

	sc := bufio.NewScanner(os.Stdin)
	// Permitimos lineas largas.
	sc.Buffer(make([]byte, 1024*1024), 8*1024*1024)
	for sc.Scan() {
		line := sc.Text()
		if strings.TrimSpace(line) == "" {
			fmt.Fprintln(os.Stderr, "linea vacia (exit 2)")
			os.Exit(2)
		}
		obj, err := h(line)
		if err != nil {
			fmt.Fprintf(os.Stderr, "error: %v (exit 3)\n", err)
			os.Exit(3)
		}
		b, _ := json.Marshal(obj)
		fmt.Fprintln(os.Stdout, string(b))
	}
	if sc.Err() != nil {
		fmt.Fprintf(os.Stderr, "error de lectura: %v (exit 5)\n", sc.Err())
		os.Exit(5)
	}
}