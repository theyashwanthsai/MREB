from ollama import chat
import json
from pydantic import BaseModel

class ModelResponse(BaseModel):
    answer: str

def get_structured_response(model_name, prompt):
    try:
        response = chat(
            messages=[{'role': 'user', 'content': prompt}],
            model=model_name,
            format=ModelResponse.model_json_schema(),
        )
        print(response)
        validated = ModelResponse.model_validate_json(response['message']['content'])
        print(validated)
        return validated.answer.lower()
    except Exception as e:
        return f"ERROR: {str(e)[:50]}"

def load_questions(file_path):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)["tasks"]
    except FileNotFoundError:
        print(f"Error: Could not find {file_path}")
        return None

def initialize_results(models):
    return {model: {"correct":0, "total":0, "details":{}} for model in models}

def generate_question_prompt(question):
    """Generate formatted question prompt"""
    options = "\n".join([f"{k}) {v}" for k, v in question["options"].items()])
    return (
        f"Question: {question['question']}\n"
        "Options:\n"
        f"{options}\n\n"
        "Please respond with ONLY the answer letter in JSON format: {'answer': ''}"
    )

def get_model_answer(model, prompt, question_id):
    try:
        answer = get_structured_response(model, prompt)
        print(answer)
        return answer
    except Exception as e:
        print(f"Error processing {model} for {question_id}: {str(e)[:50]}")
        return None

def update_results(results, model, question, model_answer, correct_answer):
    q_id = question["id"]
    results[model]["total"] += 1
    is_correct = model_answer == correct_answer
    status = "✅" if is_correct else f"❌ (Correct: {correct_answer})"
    results[model]["correct"] += is_correct
    results[model]["details"][q_id] = {
        "question": question["question"],
        "given_answer": model_answer,
        "status": status
    }

def print_evaluation_results(results):
    """Print formatted evaluation summary"""
    print("\nEvaluation Results:")
    for model, model_result in results.items():
        total = model_result["total"]
        accuracy = (model_result["correct"] / total * 100) if total else 0

        print(f"\n--- {model.upper()} ---")
        print(f"Accuracy: {accuracy:.1f}% ({model_result['correct']}/{total})")
        print("Question Breakdown:")
        for q_id, detail in model_result["details"].items():
            print(f"{q_id}: {detail['status']} | Answered: {detail['given_answer']}")