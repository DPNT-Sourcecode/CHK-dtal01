# noinspection PyShadowingBuiltins,PyUnusedLocal
def compute(x: int, y: int) -> int:
    if not (0 <= x <= 100):
        raise ValueError("x must be between 0 and 100")
    if not (0 <= y <= 100):
        raise ValueError("y must be between 0 and 100")
    return x + y

