from core.quiz_converter import QuizConverter

converter = QuizConverter('assets/example.docx')

print(converter.get_json())
print(converter.id)
  