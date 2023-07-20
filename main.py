from core.quiz_converter import QuizConverter

converter = QuizConverter('assets/math.docx')

print(converter.get_json())
print(converter.id)
  