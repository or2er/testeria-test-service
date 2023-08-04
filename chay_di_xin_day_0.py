from dotenv import load_dotenv
from langchain import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains import LLMChain
import tiktoken

load_dotenv()

tokenize = tiktoken.get_encoding('p50k_base')
llm = OpenAI(temperature=0, max_tokens=2048)


def tiktoken_len(text):
    tokens = tokenize.encode(text, disallowed_special=())
    return len(tokens)


quiz_template = """Given the following document, please generate as much as possible quiz questions with 4 choices and 1 correct answer.
You should have variety of difficulty levels (easy, medium, hard).
Easy questions should be directly stated in the document.
Medium questions should be based on the information in the document but not directly stated.
Hard questions likely require some inference and require outside knowledge.

Document 1:
<Begin Document>
Hanoi is the capital of Vietname. It is located in the North of Vietnam.
<End Document>
Result 1:
<question>
1
What is the capital of Vietnam?
A. Hanoi
B. Ho Chi Minh City
C. Da Nang
D. Can Tho
<answer>
A
<difficulty>
easy
<question>
2
Where is Hanoi located?
A. North
B. South
C. East
D. West
<answer>
A
<difficulty>
easy

Document 2:
<Begin Document>
{document}
<End Document>
Result 2:
"""

quiz_prompt = PromptTemplate(
    input_variables=["document"], template=quiz_template
)

chain = LLMChain(llm=llm, prompt=quiz_prompt)

document = """Moore's law is the observation that the number of transistors in an integrated circuit (IC) doubles about every two years. Moore's law is an observation and projection of a historical trend. Rather than a law of physics, it is an empirical relationship linked to gains from experience in production.
The observation is named after Gordon Moore, the co-founder of Fairchild Semiconductor and Intel (and former CEO of the latter), who in 1965 posited a doubling every year in the number of components per integrated circuit,[a] and projected this rate of growth would continue for at least another decade. In 1975, looking forward to the next decade, he revised the forecast to doubling every two years, a compound annual growth rate (CAGR) of 41%. While Moore did not use empirical evidence in forecasting that the historical trend would continue, his prediction held since 1975 and has since become known as a "law".
Moore's prediction has been used in the semiconductor industry to guide long-term planning and to set targets for research and development, thus functioning to some extent as a self-fulfilling prophecy. Advancements in digital electronics, such as the reduction in quality-adjusted microprocessor prices, the increase in memory capacity (RAM and flash), the improvement of sensors, and even the number and size of pixels in digital cameras, are strongly linked to Moore's law. These ongoing changes in digital electronics have been a driving force of technological and social change, productivity, and economic growth.
Industry experts have not reached a consensus on exactly when Moore's law will cease to apply. Microprocessor architects report that semiconductor advancement has slowed industry-wide since around 2010, slightly below the pace predicted by Moore's law. In September 2022 Nvidia CEO Jensen Huang considered Moore's law dead,[2] while Intel CEO Pat Gelsinger was of the opposite view."""

print(chain.run(document))
