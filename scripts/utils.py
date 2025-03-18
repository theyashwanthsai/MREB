from ollama import chat
import json
import re
from pydantic import BaseModel
from typing import Dict, List, Any, Tuple

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
        print(response)
        validated = ModelResponse.model_validate_json(response['message']['content'])
        print(validated)
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

    for question in questions:
        q_id = question["id"]
        is_coding_task = question.get("category") == "coding"
        is_multimodal = question.get("category") == "multimodal"

        prompt = generate_question_prompt(question)
        correct_answer = question.get("answer") if not is_coding_task else None
        image_path = question.get("metadata", {}).get("imagePath") if is_multimodal else None

        for model in models:
            print(f"\nProcessing {q_id} with {model}...")
            model_answer = get_model_answer(model, prompt, q_id, is_code=is_coding_task, image_path=image_path)
            if model_answer is not None:
                update_results(results, model, question, model_answer, correct_answer)

    print_evaluation_results(results)
    
    # For coding tasks, print detailed results
    # if any(question.get("category") == "coding" for question in questions):
    #     print("\n=== DETAILED TEST RESULTS ===")
    #     for model, model_result in results.items():
    #         print(f"\n--- {model.upper()} ---")
    #         for q_id, detail in model_result["details"].items():
    #             if "test_results" in detail:  # Coding question
    #                 print(f"\nQuestion {q_id}: {detail['status']}")
    #                 for result in detail["test_results"]:
    #                     if "error" in result and "test_case" not in result:
    #                         print(f"Error: {result['error']}")
    #                         continue
                            
    #                     test_id = result.get("test_case", "?")
    #                     status = "✅" if result.get("passed", False) else "❌"
                        
    #                     print(f"Test {test_id}: {status}")
    #                     if not result.get("passed", False):
    #                         print(f"  Input: {result.get('input')}")
    #                         print(f"  Expected: {result.get('expected')}")
    #                         if "actual" in result:
    #                             print(f"  Actual: {result.get('actual')}")
    #                         if "error" in result:
    #                             print(f"  Error: {result.get('error')}")
