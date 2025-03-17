from utils import *

# models_to_test = ["llama3.2:1b"] # testing
models_to_test = ["llama3.2:1b", "llama3.2:3b", "phi3.5:latest", "deepseek-r1:8b"]
ethics_file_path = "../mreb/tasks/ethics/tasks.json"
coding_file_path = "../mreb/tasks/code/tasks.json"
logic_file_path = "../mreb/tasks/logical/tasks.json"

def main():
    # Run evaluation for ethics (MCQ) questions
    print("\n=== EVALUATING ETHICS QUESTIONS ===")
    ethics_questions = load_questions(ethics_file_path)
    if ethics_questions:
        evaluate_questions(ethics_questions, models_to_test)

    # Run evaluation for ethics (MCQ) questions
    print("\n=== EVALUATING LOGICAL QUESTIONS ===")
    logic_questions = load_questions(logic_file_path)
    if logic_questions:
        evaluate_questions(logic_questions, models_to_test)
    
    # Run evaluation for coding questions
    print("\n=== EVALUATING CODING QUESTIONS ===")
    coding_questions = load_questions(coding_file_path)
    if coding_questions:
        evaluate_questions(coding_questions, models_to_test)

if __name__ == "__main__":
    main()