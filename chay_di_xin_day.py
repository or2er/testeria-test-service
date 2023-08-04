import os
import openai
from dotenv import load_dotenv

import docx
from docx.document import Document as doctwo
from docx.table import _Cell, Table
from docx.text.paragraph import Paragraph
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P

from langchain import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
import tiktoken

tokenize = tiktoken.get_encoding('p50k_base')


def tiktoken_len(text):
    tokens = tokenize.encode(text, disallowed_special=())
    return len(tokens)


load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

doc = docx.Document("assets/engrisk.docx")


def iter_block_items(parent):
    if isinstance(parent, doctwo):
        parent_elm = parent.element.body
    elif isinstance(parent, _Cell):
        parent_elm = parent._tc
    else:
        raise ValueError("something's not right")

    for child in parent_elm.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, parent)
        elif isinstance(child, CT_Tbl):
            yield Table(child, parent)


text = ""
last_text = None

print("Reading docx file...")

for block in iter_block_items(doc):
    if isinstance(block, Paragraph):
        for run in block.runs:
            rt = run.text

            if run.underline:
                rt = "<u>" + rt + "</u>"

            if run.bold:
                rt = "<b>" + rt + "</b>"

            text += rt + "\n"
    elif isinstance(block, Table):
        table = block

        for row in table.rows:
            for cell in row.cells:
                pt = ""
                for paragraph in cell.paragraphs:
                    for run in paragraph.runs:
                        rt = run.text

                        if run.underline:
                            rt = "<u>" + rt + "</u>"

                        if run.bold:
                            rt = "<b>" + rt + "</b>"

                        pt += rt

                if pt != last_text:
                    text += pt
                    last_text = pt

text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size=1024,
    chunk_overlap=256,
    length_function=tiktoken_len,
)

texts = text_splitter.create_documents([text])

for file in os.listdir("assets/engrisk"):
    os.remove(f"assets/engrisk/{file}")

if not os.path.exists("assets/engrisk"):
    os.makedirs("assets/engrisk")

for i, chunk in enumerate(texts):
    with open(f"assets/engrisk/{i}.txt", "w", encoding="utf-8") as f:
        f.write(chunk.page_content)

print("Generating...")

prompt = PromptTemplate.from_template("""
Your job is extracting and generating quiz from text.
Do not make up any information.
Question content can be html tags and must be in one line.

Text 1: ```
Question 23: Fill in the blank: I am a __________.
a. student b. teacher c. doctor d. engineer
Mark your answer on the answer sheet.
Question <b>24</b>: It is uncommon for the director to ______ power to his finance manager to make financial decisions for the company.
A. delegate	B. navigate	C. terminate	D. authorise
```
Result 1:
<question>
23
Fill in the blank: I am a __________.
A. student
B. teacher
C. doctor
D. engineer
<question>
24
It is uncommon for the director to ______ power to his finance manager to make financial decisions for the company.
A. delegate
B. navigate
C. terminate
D. authorise

Text 2: ```
Câu 1: Cho biểu thức [inline_image:32] và [inline_image:33] là hai số thực. Giá trị của biểu thức [inline_image:34] bằng:
A. [inline_image:35] B. [inline_image:36] 
C. [inline_image:37] D. [inline_image:38]

Câu 2: Tính [inline_image:39] với [inline_image:40] của đồ thị hàm số sau: [image:41]
A. [inline_image:42] B. [inline_image:43]
C. [inline_image:44] D. [inline_image:45]
                                      
Result 2:
<question>
1
Cho biểu thức [inline_image:32] và [inline_image:33] là hai số thực. Giá trị của biểu thức [inline_image:34] bằng:
A. [inline_image:35]
B. [inline_image:36]
C. [inline_image:37]
D. [inline_image:38]
<question>
2
Tính [inline_image:39] với [inline_image:40] của đồ thị hàm số sau: [image:41]
A. [inline_image:42]
B. [inline_image:43]
C. [inline_image:44]
D. [inline_image:45]

Text 3: ```
{text}
```
Result 3:
""")

response = openai.Completion.create(
    model="text-davinci-003",
    prompt=prompt.format(text=texts[8].page_content),
    temperature=0,
    max_tokens=2000,
)

print(response.choices[0].text)
