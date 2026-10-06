"""fxnotes: a small notes CLI (fixture for notemartin-project-review F06a)."""
__version__ = "1.0.0"


class FXNotesError(Exception):
    """Base class for fxnotes errors."""


class ValidationError(FXNotesError):
    """Raised when user input fails validation."""


class NotFoundError(FXNotesError):
    """Raised when a note does not exist."""


class DatabaseError(FXNotesError):
    """Raised when the underlying SQLite call fails irrecoverably."""


class CancelledError(FXNotesError):
    """Raised when the user cancels an interactive operation."""