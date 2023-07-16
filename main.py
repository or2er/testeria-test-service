from core.quiz_converter import QuizConverter

converter = QuizConverter('assets/example.docx')

for i, question in enumerate(converter.questions):
  print(i, [str(node) for node in question['content']])
  for choice in question['choices']:
    print([str(node) for node in choice])
  print("Answer: ", question['answer'])
  
print(converter.question_labels)
  