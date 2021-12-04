# Stolen from https://github.com/victorminden with some formatting changes
import contextlib
import io
import time

# Timer function taken (and cleaned a bit) from
# https://blog.usejournal.com/how-to-create-your-own-timing-context-manager-in-python-a0e944b48cf8
@contextlib.contextmanager
def solution_timing(description: str) -> None:
    """Assumes only thing printed in context is the solution"""
    with contextlib.redirect_stdout(io.StringIO()) as f:
        start = time.perf_counter()
        yield
    print(f"{description}:")
    print(f"\tTook: {time.perf_counter() - start} seconds")
    print(f"\tSolution: {f.getvalue()}")
