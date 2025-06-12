# from extract import content
from llm_connector import run_prompt_gemini
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import Runnable
from text_extraction import extract_mcq_data, extract_flashcards

# content has the the text stored in the database
# run_prompt_gemini will send a querry to the llm


# summary generator
summary_prompt = PromptTemplate(
    input_variables=["text"],
    template="""
You are an expert academic summarizer. Your task is to read the following educational content and generate a concise, informative summary.

Content:
{text}

Instructions:
- Extract the core concepts and key points.
- Use clear and precise academic language.
- Keep it within 5-7 sentences.

Summary:
"""
)

# flashcard generator
flashcard_prompt = PromptTemplate(
    input_variables=["summary"],
    template="""
You are a flashcard generator. Based on the following summary of educational content, create flashcards that help students retain key concepts.

Summary:
{summary}

Instructions:
- Format output as a list of Q&A flashcards.
- Each card should contain one question and one concise answer.
- Focus on definitions, facts, and conceptual clarity.

Format:
1. Question: ...
   Answer: ...

Flashcards: 
"""
)

# quiz generator
quiz_prompt = PromptTemplate(
    input_variables=["summary"],
    template="""
You are an exam question creator. Based on the following summary, generate 3 multiple-choice questions to test student understanding.

Summary:
{summary}

Instructions:
- Each question should have 1 correct option and 3 distractors.
- Indicate the correct answer clearly.
- Target conceptual understanding, not memorization.

Format:
1. Question: ...
   A. ...
   B. ...
   C. ...
   D. ...
   Correct Answer: ...

Quiz:
"""
)


# # teach me back generator
# teach_me_back_prompt = PromptTemplate(
#     input_variables=["text"],
#     template="""
# Imagine you're a student who just studied the following topic. Now, explain the content in your own words to teach it back to your teacher.

# Content:
# {summary}

# Instructions:
# - Explain as if teaching a peer or your teacher.
# - Use simple, clear language.
# - Highlight the main points you understood.
# - Include examples if relevant.

# Teach Me Back:
# """
# )


summary_chain = summary_prompt | run_prompt_gemini()
flashcard_chain = flashcard_prompt | run_prompt_gemini()
quiz_chain = quiz_prompt | run_prompt_gemini()
# teach_me_back_chain = teach_me_back_prompt | run_prompt_gemini()


def pipeline(text):
    summary = summary_chain.invoke({"text":text}).content
    flashcard = flashcard_chain.invoke({"summary":summary}).content
    quiz = quiz_chain.invoke({"summary":summary}).content
    # teach_me_back = teach_me_back_chain.invoke({"summary":summary}).content


    return {
        "summary": summary,
        "flashcard": flashcard,
        "quiz": quiz,
        # "teach_me_back": teach_me_back
    }



# if __name__ == "__main__":
#     result = pipeline(content)
#     print("--- Summary ---\n", result["summary"])

#     print("\n--- Flashcards ---\n")
#     flashcards = extract_flashcards(result["flashcard"])
#     for f in flashcards:
#         print("Question:", f["question"])
#         print("Answer:", f["answer"])
#         print("-" * 40)
        
#     print("\n--- Quiz ---\n")
#     questions = extract_mcq_data(result["quiz"])
#     for q in questions:
#         print("Question:", q["question"])
#         print("Options:", q["options"])
#         print("Correct Answer:", q["correct_answer"])
#         print("-" * 40)

#     # print("\n--- Teach Me Back ---\n", result["teach_me_back"])