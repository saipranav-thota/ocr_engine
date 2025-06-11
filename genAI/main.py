from extract import content, doc_id
from transform import pipeline
from text_extraction import extract_flashcards, extract_mcq_data
from load import loader_data

result = pipeline(content)

summary = result["summary"]
flashcards = extract_flashcards(result["flashcard"])
questions = extract_mcq_data(result["quiz"])

loader_data(doc_id, "reinforcement_content", ["summary", "flashcards", "mcqs"], [summary, flashcards, questions]) 