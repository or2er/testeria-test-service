QUIZ2QUIZ_TEMPLATE = """
Your job is extracting and generating quiz questions from text.
Questions must have 4 choices. Otherwise, skip the question.
If no question can be generated, respond with "<empty>".
Correct choice can have different styles from other choices.
_text_ is italicized
~text~ is underlined
*text* is bolded

Text 1:
<Begin Document>
Question 23: Fill in the blank: I am a __________.
_a_. student b. teacher c. doctor d. engineer

Question 46: In their ~pioneering~ research, they found that the learning needs of the two groups
of learners were quite ~distinctive~ from each other, and the  ~control~ group whose learning needs were
stronger performed better than the ~comparative~ group.
<End Document>
Result 1:
<question>
23
Fill in the blank: I am a __________.
A. student
B. teacher
C. doctor
D. engineer
Answer: A
<question>
46
In their ~pioneering~ research, they found that the learning needs of the two groups of learners were quite ~distinctive~ from each other, and the ~control~ group whose learning needs were stronger performed better than the ~comparative~ group.
A. pioneering
B. distinctive
C. control
D. comparative
Answer: None

Text 2:
<Begin Document>
{document}
<End Document>
Result 2:
"""

DOC2QUIZ_TEMPLATE = """Given the following document, please generate as much as possible quiz questions with 4 choices and 1 correct answer.
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
Answer: A
Difficulty: easy
<question>
2
Where is Hanoi located?
A. North
B. South
C. East
D. West
Answer: A
Difficulty: easy

Document 2:
<Begin Document>
{document}
<End Document>
Result 2:
"""
