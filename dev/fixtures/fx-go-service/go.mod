module fx-go-service

go 1.22

require (
	github.com/go-chi/chi/v5 v5.1.0
	github.com/google/wire v0.6.0
	github.com/mattn/go-sqlite3 v1.14.22
	github.com/stretchr/testify v1.9.0
)

require (
	github.com/davecheney/profile v1.7.27 // indirect
	github.com/dgryski/go-rendezvous v0.0.0-20200823014737-9f7001d12a5f // indirect
	github.com/google/subcommands v1.2.0 // indirect
	github.com/pmezard/go-difflib v1.0.0 // indirect
	golang.org/x/sys v0.20.0 // indirect
	gopkg.in/yaml.v3 v3.0.1 // indirect
)

// davecheney/profile es una dep transitiva de test de stretchr/testify
// via gopkg.in/check.v1. El repo original no esta accesible (404).
// Usamos un stub local para romper la cadena de dependencias.
replace github.com/davecheney/profile => ./stub-davecheney
