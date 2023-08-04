from core.v2.doc2quiz_converter import Doc2QuizConverter
from core.v2.scanner import DocxScanner

# scanner = DocxScanner('assets/gdcd.docx')
# scanner.scan_elements()

# full_text = scanner.text()

with open('assets/ethereum.txt', 'r', encoding='utf-8') as f:
    full_text = f.read()

converter = Doc2QuizConverter(full_text)
converter.convert()

for question in converter.questions:
    print(question["content"])
