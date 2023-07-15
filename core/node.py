class Node:
  """
  A node in a paragraph.
  
  It can be a text, an image, or an inline image.
  """

  def __init__(self):
    self.text = None
    self.image = None
    self.inline_image = None
    self.italic = None
    self.bold = None
    self.underline = None
    self.color = None
    self.super_script = None
    self.sub_script = None

  def is_concatable_with(self, other):
    """Check if this node is concatable with the other node."""
    if self.text is None:
      return False
    
    return self.italic == other.italic and self.bold == other.bold and self.underline == other.underline and self.color == other.color and self.super_script == other.super_script and self.sub_script == other.sub_script
  
  def concat(self, other):
    """Concat the other node to this node."""
    self.text += other.text
  
  def __str__(self):
    if self.image is not None:
      return "[image:{}]".format(self.image)
    
    if self.inline_image is not None:
      return "[inline_image:{}]".format(self.inline_image)
    
    return self.text