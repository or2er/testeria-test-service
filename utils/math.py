def is_close(a, b, percent=0.1):
  """Checks if the given values are close."""

  return abs(a - b) <= abs(a * percent)

def get_largest_key(dictionary):
  """Returns the key of the largest value in the given dictionary."""

  return max(dictionary, key=dictionary.get)