// Trampa S02: dead legacy binary.
//
// Este entry point es un binario legacy que solo imprime un mensaje.
// Ningun test ni codigo de produccion lo invoca. La skill debe
// detectarlo via grep de "legacy".
package main

import "fmt"

func main() {
	fmt.Println("fx-go-service legacy binary - deprecated")
	// Dead code: nada util se hace aqui.
}
