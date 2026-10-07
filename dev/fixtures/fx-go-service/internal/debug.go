// Trampa S03: dead debug helper.
//
// DebugPrintln solo hace fmt.Println y no se invoca en runtime.
// La skill debe detectarlo via grep de "DebugPrintln".
package internal

import "fmt"

func DebugPrintln(s string) {
	// Dead code: solo para debugging local; no se invoca en runtime.
	fmt.Println("[DEBUG]", s)
}
