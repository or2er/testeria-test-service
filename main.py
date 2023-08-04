from core.v2.quiz2quiz_converter import Quiz2QuizConverter
from core.v2.scanner import DocxScanner

scanner = DocxScanner('assets/gdcd.docx')
scanner.scan_elements()

full_text = scanner.text()
print(full_text)
converter = Quiz2QuizConverter(full_text)
converter.convert()

print(converter.questions)
