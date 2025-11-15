import os
from pathlib import Path


def _ensure_dyld_path():
    """Make sure libmagic can be located on macOS installs."""
    if os.name != "posix":
        return

    brew_lib = "/opt/homebrew/lib"
    current = os.environ.get("DYLD_LIBRARY_PATH")
    if current and brew_lib in current.split(":"):
        return

    new_value = brew_lib if not current else f"{brew_lib}:{current}"
    os.environ["DYLD_LIBRARY_PATH"] = new_value


def _squelch_libressl_warning():
    """Silence the noisy urllib3 warning raised on LibreSSL builds."""
    try:
        import warnings
        from urllib3.exceptions import NotOpenSSLWarning

        warnings.filterwarnings("ignore", category=NotOpenSSLWarning)
    except Exception:
        pass


_ensure_dyld_path()
_squelch_libressl_warning()
