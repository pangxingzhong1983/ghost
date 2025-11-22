# Minimal pure-Python stub for pylzma on macOS arm64 where the native
# extension fails to build on Python 3.11+. We proxy to the stdlib
# lzma implementation to keep Ghost tooling runnable. Compression
# format differs from the original pylzma but is sufficient for
# local build workflows that only require a callable interface.
import lzma

__all__ = ["compress", "decompress", "compressobj", "decompressobj"]
__version__ = "stub-lzma"


def compress(data, eos=1, *_, **__):
    """
    pylzma.compress(data, eos=1, ...) -> bytes
    """
    # pylzma ignores eos when using raw LZMA; stdlib lzma always writes EOS.
    # We simply compress with default settings.
    if isinstance(data, str):
        data = data.encode()
    return lzma.compress(data)


def decompress(data, *_, **__):
    """
    pylzma.decompress(data, ...) -> bytes
    """
    return lzma.decompress(data)


class _CompressObj:
    def __init__(self, *_, **__):
        self._comp = lzma.LZMACompressor()

    def compress(self, data):
        if isinstance(data, str):
            data = data.encode()
        return self._comp.compress(data)

    def flush(self):
        return self._comp.flush()


class _DecompressObj:
    def __init__(self, *_, **__):
        self._dec = lzma.LZMADecompressor()

    def decompress(self, data, max_length=None):
        return self._dec.decompress(data, max_length or 0)

    def flush(self):
        # stdlib LZMADecompressor has no flush; return empty for API parity.
        return b""


def compressobj(*args, **kwargs):
    return _CompressObj(*args, **kwargs)


def decompressobj(*args, **kwargs):
    return _DecompressObj(*args, **kwargs)
