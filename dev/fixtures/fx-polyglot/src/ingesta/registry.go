// Registro de handlers. Trampa #4 del ecosistema: la inicializacion ocurre en
// `func init()` y el lookup se hace en main.go sin mostrar donde se registro.
package main

// handlers es el map global donde init() en handlers.go y handlers_legacy.go
// registran las funciones. Su existencia aqui y no en main.go es la trampa.
var handlers = map[string]Handler{}