# Function Calling Evaluation Template

This directory contains function definitions that can be used to evaluate the tool calling (function calling) abilities of Large Language Models (LLMs).

## Purpose

The functions defined here serve as a benchmark for measuring how well LLMs can:
- Understand function signatures and documentation
- Call functions with appropriate arguments
- Handle different parameter types and return values
- Follow function calling protocols

## Usage

These functions are used in the evaluation pipeline to test LLM function calling capabilities. The evaluation system will:
1. Present the function definitions to the LLM
2. Provide scenarios where the LLM should call these functions
3. Measure the accuracy and appropriateness of the function calls
4. Generate metrics on function calling performance

## Template Function Example:

```python
def sum(a: int, b: int) -> int:
    """
    Sum two integers.
    
    Args:
        a: An integer.
        b: An integer.

    Returns:
        The sum of the two integers.
    """
    return a + b
```