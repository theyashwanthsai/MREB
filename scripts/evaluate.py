import json
from utils import *

# models_to_test = ["llama3.2:1b"] # testing
models_to_test = ["llama3.2:1b", "llama3.2:3b", "phi3.5:latest", "deepseek-r1:8b"]
json_file_path = "../mreb/tasks/ethics/tasks.json"  

def main():
    questions = load_questions(json_file_path)
    if not questions:
        return

    results = initialize_results(models_to_test)

    for question in questions:
        prompt = generate_question_prompt(question)
        q_id = question["id"]
        correct_answer = question["answer"]

        for model in models_to_test:
            model_answer = get_model_answer(model, prompt, q_id)
            if model_answer is not None:
                update_results(results, model, question, model_answer, correct_answer)

    print_evaluation_results(results)

if __name__ == "__main__":
    main()