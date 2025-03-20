from ollama import chat
import json
from pydantic import BaseModel
from typing import Dict, List, Any, Tuple
import os


class ModelResponse(BaseModel):
    answer: str

def get_structured_response(model_name, prompt, is_code=False, image_path=None):
    try:
        message = {'role': 'user', 'content': prompt}
        if image_path:
            message['images'] = [image_path]

        response = chat(
            messages=[message],
            model=model_name,
            format=ModelResponse.model_json_schema(),
        )
        # print(response)
        validated = ModelResponse.model_validate_json(response['message']['content'])
        # print(validated)
        if is_code:
            return validated.answer  # Return full code for code tasks
        return validated.answer.lower() # Return for mcq
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
    """Generate formatted question prompt based on question type"""
    if question.get("category") == "coding":
        return (
            f"You are a Python coding assistant. Respond with ONLY the code solution.\n"
            f"You must provide your answer in JSON format as follows:\n"
            f"{{\n  \"answer\": \"your code here\"\n}}\n\n"
            f"Task: {question['question']}\n"
            f"Function signature: {question.get('function_template', '')}\n\n"
            f"Your solution should pass all test cases. Only provide the code, no explanations."
        )
    else:
        options = "\n".join([f"{k}) {v}" for k, v in question["options"].items()])
        return (
            f"Question: {question['question']}\n"
            "Options:\n"
            f"{options}\n\n"
            "Please respond with ONLY the answer letter in JSON format: {'answer': ''}"
        )

def get_model_answer(model, prompt, question_id, image_path, is_code=False):
    try:
        answer = get_structured_response(model, prompt, is_code, image_path)
        return answer
    except Exception as e:
        print(f"Error processing {model} for {question_id}: {str(e)[:50]}")
        return None

def update_results(results, model, question, model_answer, correct_answer=None):
    """Update results for both MCQ and coding questions"""
    q_id = question["id"]
    results[model]["total"] += 1
    
    if question.get("category") == "coding":
        # Evaluate code 
        passed, test_results = evaluate_code_solution(model_answer, question)
        is_correct = passed
        passed_count = sum(1 for r in test_results if r.get('passed', False))
        total_tests = len(question["test_cases"])
        status = f"✅ ({passed_count}/{total_tests})" if is_correct else f"❌ ({passed_count}/{total_tests})"
        
        results[model]["correct"] += is_correct
        results[model]["details"][q_id] = {
            "question": question["question"][:50] + "...",  
            "tests_passed": f"{passed_count}/{total_tests}",
            "status": status,
            "test_results": test_results  
        }
    else:
        # Evaluate MCQ 
        is_correct = model_answer == correct_answer
        status = "✅" if is_correct else f"❌ (Correct: {correct_answer})"
        
        results[model]["correct"] += is_correct
        results[model]["details"][q_id] = {
            "question": question["question"],
            "given_answer": model_answer,
            "status": status
        }

def evaluate_code_solution(code: str, task: Dict[str, Any]) -> Tuple[bool, List[Dict[str, Any]]]:
    """Evaluate the code solution against test cases."""
    namespace = {}
    
    try:
        # Execute the code in the namespace
        exec(code, namespace)

        function_name = task["function_template"].split("def ")[1].split("(")[0].strip()
        
        if function_name not in namespace:
            return False, [{"error": f"Function '{function_name}' not found in solution"}]
        
        function = namespace[function_name]
        

        results = []
        all_passed = True
        
        for i, test_case in enumerate(task["test_cases"]):
            try:
                input_val = test_case["input"]
                expected = test_case["output"]
                actual = function(input_val)
                
                passed = actual == expected
                if not passed:
                    all_passed = False
                
                results.append({
                    "test_case": i+1,
                    "input": input_val,
                    "expected": expected,
                    "actual": actual,
                    "passed": passed
                })
            except Exception as e:
                all_passed = False
                results.append({
                    "test_case": i+1,
                    "input": input_val,
                    "error": str(e),
                    "passed": False
                })

        return all_passed, results
    
    except Exception as e:
        return False, [{"error": f"Code execution failed: {str(e)}"}]

def print_evaluation_results(results):
    """Print formatted evaluation summary for both MCQ and coding questions"""
    print("\nEvaluation Results:")
    for model, model_result in results.items():
        total = model_result["total"]
        accuracy = (model_result["correct"] / total * 100) if total else 0

        print(f"\n--- {model.upper()} ---")
        print(f"Accuracy: {accuracy:.1f}% ({model_result['correct']}/{total})")
        print("Question Breakdown:")
        
        for q_id, detail in model_result["details"].items():
            if "tests_passed" in detail:  # Coding question
                print(f"{q_id}: {detail['status']} | Tests: {detail['tests_passed']}")
            else:  # MCQ question
                print(f"{q_id}: {detail['status']} | Answered: {detail['given_answer']}")

def evaluate_questions(questions, models):
    results = initialize_results(models)
    category = questions[0].get("category", "unknown") if questions else "unknown"
    
    for question in questions:
        q_id = question["id"]
        is_coding_task = question.get("category") == "coding"
        is_multimodal = question.get("category") == "multimodal"

        prompt = generate_question_prompt(question)
        correct_answer = question.get("answer") if not is_coding_task else None
        image_path = question.get("metadata", {}).get("imagePath") if is_multimodal else None

        for model in models:
            print(f"\nProcessing {q_id} with {model}...")
            model_answer = get_model_answer(model, prompt, q_id, image_path, is_code=is_coding_task)
            if model_answer is not None:
                update_results(results, model, question, model_answer, correct_answer)

    print_evaluation_results(results)
    
    # Save results to files
    save_detailed_breakdown(results, category)
    
    return results

def save_detailed_breakdown(results, category):
    """Save detailed question-by-question breakdown to markdown file with side-by-side model comparison"""
    output_dir = "Results"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    filepath = os.path.join(output_dir, f"{category}_detailed_breakdown.md")

    with open(filepath, 'w') as f:
        f.write(f"# {category.upper()} Benchmark Detailed Results\n\n")

        f.write("### Overall Scores\n\n")
        f.write("| Model | Score | Correct/Total |\n")
        f.write("|-------|--------|---------------|\n")
        for model, model_result in results.items():
            total = model_result["total"]
            accuracy = (model_result["correct"] / total * 100) if total else 0
            f.write(f"| {model.upper()} | {accuracy:.2f}% | {model_result['correct']}/{total} |\n")
        f.write("\n")
        
        f.write("### Question-by-Question Comparison\n\n")

        all_questions = set()
        for model_result in results.values():
            all_questions.update(model_result["details"].keys())
        all_questions = sorted(all_questions)

        if category.lower() == "coding":
            header = "| Question ID |"
            separator = "|------------|"
            for model in results.keys():
                header += f" {model.upper()} Status | {model.upper()} Tests Passed |"
                separator += "------------|-------------------|"
            f.write(header + "\n")
            f.write(separator + "\n")


            for q_id in all_questions:
                row = f"| {q_id} |"
                for model in results.keys():
                    detail = results[model]["details"].get(q_id, {"status": "N/A", "tests_passed": "N/A"})
                    row += f" {detail['status']} | {detail['tests_passed']} |"
                f.write(row + "\n")

        else:
            header = "| Question ID |"
            separator = "|------------|"
            for model in results.keys():
                header += f" {model.upper()} Status |"
                separator += "------------|"
            f.write(header + "\n")
            f.write(separator + "\n")

            for q_id in all_questions:
                row = f"| {q_id} |"
                for model in results.keys():
                    detail = results[model]["details"].get(q_id, {"status": "N/A", "given_answer": "N/A"})
                    row += f" {detail['status']} |"
                f.write(row + "\n")

    json_data = {
        "category": category,
        "models": {}
    }

    for model, model_result in results.items():
        total = model_result["total"]
        correct = model_result["correct"]
        accuracy = (correct / total * 100) if total else 0.0
        model_entry = {
            "total": total,
            "correct": correct,
            "accuracy": round(accuracy, 2),
        }
        json_data["models"][model] = model_entry

    json_path = os.path.join(output_dir, f"{category}_results.json")
    with open(json_path, 'w') as json_f:
        json.dump(json_data, json_f, indent=4, default=str)

    print(f"Detailed breakdown saved to {filepath}")
    print(f"JSON results saved to {json_path}")


