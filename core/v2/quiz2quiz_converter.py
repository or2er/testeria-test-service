
from .template import QUIZ2QUIZ_TEMPLATE
from .openai import llm, tiktoken_len
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain import PromptTemplate
from time import time
from uuid import uuid4


class Quiz2QuizConverter:

    def __init__(self, document):
        self.id = str(uuid4())
        self.document = document
        self.prompt = PromptTemplate(
            input_variables=["document"], template=QUIZ2QUIZ_TEMPLATE
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=512,
            chunk_overlap=128,
            length_function=tiktoken_len
        )
        self.chain = LLMChain(llm=llm, prompt=self.prompt)
        self.questions = {}
        self.progress = 0

    def convert(self):
        start = time()
        questions = []

        chunks = self.text_splitter.create_documents([self.document])

        print("Start tool 1 ...")
        print("Total chunks:", len(chunks))
        print("Converting document to questions...")

        for i, chunk in enumerate(chunks):
            response = self.chain.run(chunk.page_content)

            print(f"Chunk {i+1}/{len(chunks)}")

            self.progress = (i + 1) / len(chunks)

            if response == '<empty>':
                continue

            questions += self._extract_questions(response)

        for question in questions:
            self.questions[str(question["index"])] = question

        print("Done in", time() - start, "s.")

    def _extract_questions(self, response):
        q_texts = response.split("<question>")
        questions = []

        for q_text in q_texts:
            q_text = q_text.strip()

            if q_text == "":
                continue

            lines = q_text.split("\n")

            if len(lines) < 6:
                continue

            questions.append({
                "index": int(lines[0]),
                "content": lines[1],
                "choices": [
                    lines[2][3:],
                    lines[3][3:],
                    lines[4][3:],
                    lines[5][3:]
                ],
                "answer": None if lines[6][8:] == "None" else lines[6][8:],
                "difficulty": "easy"
            })

        return questions
