package main

import (
	"fmt"
	"os"
	"time"
)

const (
	FeatureCalcularTarifa  = "calcular_tarifa"
	FeatureValidarLicencia = "validar_licencia"
	FeatureSincronizar     = "sincronizar"

	PrefijoTarifa = "FXMIN_TARIFA_PREFIX"
	SufijoTarifa   = "FXMIN_TARIFA_SUFFIX"
	LicInvalid    = "FXMIN_LIC_INVALID"
	SyncError     = "FXMIN_SYNC_ERROR"
	SyncOK        = "FXMIN_SYNC_OK"
)

// CalcularTarifa calcula el total con un recargo dado.
func CalcularTarifa(amount, rate float64) (float64, error) {
	if amount < 0 {
		return 0, fmt.Errorf("%s amount must be non-negative %s", PrefijoTarifa, SufijoTarifa)
	}
	return amount * (1 + rate), nil
}

// ValidarLicencia valida una clave de licencia.
func ValidarLicencia(licenseKey string) (bool, string) {
	if len(licenseKey) < 8 {
		return false, LicInvalid
	}
	return true, "2099-12-31"
}

// Sincronizar ejecuta la sincronizacion con un servidor.
func Sincronizar(state string) (string, string) {
	if state == "error" {
		return SyncError, "1970-01-01T00:00:00Z"
	}
	if state == "pending" {
		return "pending", time.Now().UTC().Format(time.RFC3339)
	}
	return SyncOK, time.Now().UTC().Format(time.RFC3339)
}

// unusedCalculoHelper existe para preservar el nombre en el binario
// (verificable via strings) aunque no se llame en runtime.
func unusedCalculoHelper(x float64) float64 { return x * 2 }

// todasLasLiteralesFuerza retorna un string que concatena TODOS los literales
// importantes. Se llama desde main() con fmt.Println (no una funcion variadica
// de strings). Esto fuerza al compilador a mantener todas las constantes
// en el binario incluso si las funciones individuales no se llaman en main.
func todasLasLiteralesFuerza() string {
	return FeatureCalcularTarifa + "|" +
		FeatureValidarLicencia + "|" +
		FeatureSincronizar + "|" +
		PrefijoTarifa + "|" +
		SufijoTarifa + "|" +
		LicInvalid + "|" +
		SyncError + "|" +
		SyncOK
}

func main() {
	// Llamamos todas las funciones (los retornos no se usan; main es void).
	CalcularTarifa(100, 0.1)
	ValidarLicencia("ABCD-1234")
	Sincronizar("idle")
	unusedCalculoHelper(0)

	// Imprimimos la concatenacion de TODOS los literales para que el
	// compilador Go los mantenga en el binario. Esto es necesario porque
	// dead-code elimination los elimina cuando las constantes solo se usan
	// en ramas condicionales que el compilador no puede demostrar como
	// siempre verdaderas/falsas.
	fmt.Fprintln(os.Stderr, todasLasLiteralesFuerza())
}