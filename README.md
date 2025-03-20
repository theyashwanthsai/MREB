# MREB
Multimodal Reasoning and Ethics Benchmark (MREB) is an open source benchmark designed to assess the cross-domain capabilities of AI models. Currently I am comparing local llms via ollama

### Resources:
- Blog post: [Link](https://saiyashwanth.tech/mreb)
- Youtube Video: tbd 


MREB provides a standardized way to evaluate LLMs by:
- Testing cross-domain capabilities
- Providing consistent scoring metrics
- Enabling fair comparison between different models
- Focusing on practical, real-world applications

The fun part? All of the llms are run locally on my pc. Check more about my pc building experience [here](https://saiyashwanth.tech/pcbuild)

## How does it work?
There are 4 categories - Logical, Coding, Ethics, Multimodal. Each category is to test an llm in that skill/space. Currently there are 25 tasks in each. The goal is to expand them to 120, with different difficulty types. 

Here’s a glimpse of the categories and example tasks:

#### Code Score
- Example Task:
!["Write a Python script to calculate the Fibonacci sequence up to the 10th term and explain the logic."](./images/coding.png)


#### Logic Score
- Example Task:
!["Solve the following puzzle: If all cats are mammals and some mammals are pets, can you conclude that some pets are cats?"](./images/logic.png)


#### Ethics Score
- Example Task:
!["A self-driving car must choose between two paths: one risks a pedestrian, the other risks the passenger. What ethical principles should guide its decision?"](./images/ethics.png)


#### Multimodal Score
- Example Task:
!["Analyze this image of a weather chart and a text summary of climate data. Explain how they contradict each other."](./images/multimodal.png)



The project includes an automated evaluation script (`evaluate.py`) that benchmarks various LLMs on multimodal tasks. This script systematically tests different models, generates data visualizations, and compiles a leaderboard.

Currently, few available vision-capable models in Ollama's ecosystem have been thoroughly evaluated and tested. 


## Todo
- [x] Add code tasks
- [x] Add multimodal tasks
- [x] Add more tasks in logical and ethics
- [x] Evaluation script should account for multiple categories.
- [x] Add readme for each category.
- [ ] Blog must include graphs and charts along with leaderboards.
- [x] Add logic to write the results in a file
- [x] Add logic to automatically create visuals using plotly
- [ ] Add bash file

## 📝 License

MREB is released under the MIT License. See the LICENSE file for more details.

## 📬 Contact

For questions or suggestions, please open an issue or contact me - taddishetty34@gmail.com