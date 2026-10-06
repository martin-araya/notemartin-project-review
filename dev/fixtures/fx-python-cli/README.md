# fxnotes

A small notes CLI. Stores notes in a local SQLite database. Supports plugins via entry points.

## Commands

- `fxnotes add <key> <value>` — add a note.
- `fxnotes list [--tag TAG] [--sort-by KEY]` — list notes.
- `fxnotes delete <key> [--no-undo] [--archived]` — delete a note.
- `fxnotes export <path> [--format json|csv]` — export notes.

## Configuration

Reads from `~/.config/fxnotes/config.toml` (if present) and environment variables prefixed with `FXNOTES_`.

> **Note:** `delete` is currently synchronous — it returns once the note is removed from the
> database and the soft-delete flag is cleared. There is no background job that touches
> deleted notes afterwards. (This sentence is part of the fixture's documented contradictions.)

## Plugins

Third-party commands can be registered via the `fxnotes.commands` entry point group. The loader
discovers them at runtime via `importlib.import_module`.

## Development

```sh
pip install -e .
pytest
```