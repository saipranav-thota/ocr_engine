
import re

def extract_mcq_data(text):
    pattern = r"""
        (?P<qnum>\d+)\.\s+Question:\s+(?P<question>.+?)\n
        \s*A\.\s+(?P<option_a>.+?)\n
        \s*B\.\s+(?P<option_b>.+?)\n
        \s*C\.\s+(?P<option_c>.+?)\n
        \s*D\.\s+(?P<option_d>.+?)\n
        \s*Correct\s+Answer:\s+(?P<answer>[A-D])
    """

    matches = re.finditer(pattern, text, re.VERBOSE | re.MULTILINE | re.DOTALL)
    result = []

    for match in matches:
        result.append({
            "question": match.group("question").strip(),
            "options": {
                "A": match.group("option_a").strip(),
                "B": match.group("option_b").strip(),
                "C": match.group("option_c").strip(),
                "D": match.group("option_d").strip(),
            },
            "correct_answer": match.group("answer").strip()
        })

    return result


def extract_flashcards(text):
    pattern = r"(?P<qnum>\d+)\.\s+Question:\s+(?P<question>.+?)\n\s+Answer:\s+(?P<answer>.+?)(?=\n\d+\.|\Z)"
    matches = re.finditer(pattern, text, re.DOTALL)

    flashcards = []

    for match in matches:
        flashcards.append({
            "question": match.group("question").strip(),
            "answer": match.group("answer").strip()
        })

    return flashcards