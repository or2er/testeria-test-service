from .template import DOC2QUIZ_TEMPLATE
from .openai import llm, tiktoken_len
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain import PromptTemplate
from time import time
from uuid import uuid4


class Doc2QuizConverter:

    def __init__(self, document):
        self.id = str(uuid4())
        self.document = document
        self.prompt = PromptTemplate(
            input_variables=["document"], template=DOC2QUIZ_TEMPLATE
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=512,
            chunk_overlap=128,
            length_function=tiktoken_len
        )
        self.chain = LLMChain(llm=llm, prompt=self.prompt)
        self.questions = []

    def convert(self):
        start = time()
        questions = []

        chunks = self.text_splitter.create_documents([self.document])

        print("Start tool 2 ...")
        print("Total chunks:", len(chunks))
        print("Converting document to questions...")

        for i, chunk in enumerate(chunks):
            response = self.chain.run(chunk.page_content)

            print(f"Chunk {i+1}/{len(chunks)}")

            if response == '<empty>':
                continue

            questions += self._extract_questions(response)

        print("Done in", time() - start, "s.")

        return questions
    

