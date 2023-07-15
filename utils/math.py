def is_close(a, b, percent=0.1):
  """Checks if the given values are close."""

  return abs(a - b) <= abs(a * percent)