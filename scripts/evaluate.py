from utils import *

models_to_test = ["gemma3:latest", "llama3.2-vision:latest", "llava:latest", "llava-llama3:latest",  ]


## Todo: Add a way to test only text models and multimodal models at the same time.

ethics_file_path = "./mreb/tasks/ethics/tasks.json"
coding_file_path = "./mreb/tasks/code/tasks.json"
logic_file_path = "./mreb/tasks/logical/tasks.json"
multimodal_file_path = "./mreb/tasks/multimodal/tasks.json"

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
    
    # Run evaluation for multimodal questions
    print("\n=== EVALUATING MULTIMODAL QUESTIONS ===")
    multimodal_questions = load_questions(multimodal_file_path)
    if multimodal_questions:
        evaluate_questions(multimodal_questions, models_to_test)

        # Run evaluation for coding questions
    print("\n=== EVALUATING CODING QUESTIONS ===")
    coding_questions = load_questions(coding_file_path)
    if coding_questions:
        evaluate_questions(coding_questions, models_to_test)


if __name__ == "__main__":
    main()