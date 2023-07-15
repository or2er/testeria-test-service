import os, docx
from utils import *
from .node import Node

class QuizConverter:

  # The maximum length of a question label
  # Example: 
  #   "Question 1" has a label length of 2
  #   "Câu hỏi 2" has a label length of 3
  MAX_LABEL_LENGTH = 5

  def __init__(self, file_path):
    self.file_path = file_path
    self.document = docx.Document(file_path)
    self.question_labels = []
    self.questions = []
    self.paragraphs = []
    
    # mapping from relationship id to image file name
    self.rels = {}

    self._scan()
  
  def _scan(self):
    """Scan and parse the document."""
    
    self._scan_paragraphs()
    self._scan_label()

    current_question = None
    scanning_target = None

    for paragraph in self.paragraphs:
      i = 0

      if self._is_start_of_question(paragraph):
        current_question = {
          'content': [],
          'choices': [[], [], [], []],
        }
        self.questions.append(current_question)
        i = len(self.question_labels)
        scanning_target = "<content>"

      elif self._is_start_of_choice(paragraph):
        # start scanning choices
        node = paragraph[0]
        letter = extract_index_letter(node.text) 
        scanning_target = ord(letter.lower()) - ord('a')
        i = 1
      elif scanning_target != "<content>":
        continue

      while i < len(paragraph):
        node = paragraph[i]

        if node.text is None:
          if scanning_target == "<content>":
            current_question['content'].append(node)
          else:
            current_question['choices'][scanning_target].append(node)
        elif is_index_letter(node.text):
          # start scanning choices
          letter = extract_index_letter(node.text) 
          scanning_target = ord(letter.lower()) - ord('a')
          
        elif scanning_target == "<content>":
          if len(current_question['content']) > 0 and current_question['content'][-1].is_concatable_with(node):
            current_question['content'][-1].concat(node)
          else:
            current_question['content'].append(node)
        else:
          if len(current_question['choices'][scanning_target]) > 0 and current_question['choices'][scanning_target][-1].is_concatable_with(node):
            current_question['choices'][scanning_target][-1].concat(node)
          else:
            current_question['choices'][scanning_target].append(node)

        i += 1
      
      if scanning_target != "<content>":
        scanning_target = None

  def _scan_paragraphs(self):
    """Scan all paragraphs in the document then convert them to nodes."""
    
    # get relationship id of each image from the document
    for run in self.document.part.rels.values():
      if isinstance(run._target, docx.parts.image.ImagePart):
        self.rels[run.rId] = os.path.basename(run._target.partname)

    for paragraph in self.document.paragraphs:
      paragraph_ = []

      for run in paragraph.runs:
        text = run.text
        
        # check if the run contains an inline image
        if 'v:imagedata' in run._element.xml:
          for key, value in self.rels.items():
            if 'r:id="{}"'.format(key) in run._element.xml:
              node = Node()
              node.inline_image = value
              paragraph_.append(node)
              break
        # check if the run contains a drawing image
        elif 'w:drawing' in run._element.xml:
          for key, value in self.rels.items():
            if 'r:embed="{}"'.format(key) in run._element.xml:
              node = Node()
              node.image = value
              paragraph_.append(node)
              break
        else:
          super_script = 'superscript' in run._element.xml
          sub_script = 'subscript' in run._element.xml
          
          subtexts = text.split(' ')
          for j, text_ in enumerate(subtexts):          
            node = Node()
            node.italic = run.italic
            node.bold = run.bold
            node.underline = run.underline
            node.color = run.font.color.rgb
            node.super_script = super_script
            node.sub_script = sub_script
            
            node.text = text_
            if j != len(subtexts) - 1:
              node.text += ' '
            
            paragraph_.append(node)

      self.paragraphs.append(paragraph_)

  def _scan_label(self):
    """Scan the nodes and extract the question labels."""
    
    # Count the number of each word in the first `MAX_LABEL_LENGTH` nodes of each paragraph
    counters = [{} for _ in range(self.MAX_LABEL_LENGTH)]

    for paragraph in self.paragraphs:
      if len(paragraph) < self.MAX_LABEL_LENGTH:
        continue
      
      for i in range(self.MAX_LABEL_LENGTH):
        node = paragraph[i]
        name = node.text
        
        if node.text is None:
          continue

        if is_index_number(node.text):
          name = "<number>"
        elif is_index_letter(node.text):
          name = "<letter>"

        if name not in counters[i]:
          counters[i][name] = 0

        counters[i][name] += 1

    i = 0
    previous_label_count = None

    # Find the question labels
    while i < self.MAX_LABEL_LENGTH:
      total = 0

      for key, value in counters[i].items():
        if key != "<letter>":
          total += value

      for key, value in counters[i].items():
        if key == "<letter>":
          continue
        
        # current node is a question label if it has a frequency of more than 50%
        # and its number of occurrences is close to the previous node
        if value / total > 0.5 and (previous_label_count is None or is_close(value, previous_label_count, 0.2)):
          self.question_labels.append(key)
          previous_label_count = value
          break

      i += 1

  def _is_start_of_question(self, paragraph):
    """Check if the given paragraph starts with question labels."""
    
    if len(paragraph) < len(self.question_labels):
      return False

    i = 0
    while i < len(self.question_labels):
      node = paragraph[i]

      if self.question_labels[i] == "<number>":
        if not is_index_number(node.text):
          break
      elif self.question_labels[i] != node.text:
        break

      i += 1

    return i == len(self.question_labels)

  def _is_start_of_choice(self, paragraph):
    """Check if the given paragraph starts with a choice label."""
    
    if len(paragraph) < 1:
      return False

    node = paragraph[0]
    
    if node.text is None:
      return False

    return is_index_letter(node.text)

    