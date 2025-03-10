# ai-autograding-feedback

## Overview
This program is part of an exploratory project to evaluate the quality of LLM-generated feedback in assisting with assignment grading and enhancing student learning. This program processes either the code sections or images of a student's submission to programming assignments, based on the provided arguments. It generates output in either markdown format or standard output. 

The large language models used and implementation logic vary depending on whether the selected scope is 'image' or 'code'.

For the code scope, the program takes three files:
- An assignment's solution file
- A student's submission file
- A text file containing the error trace


## Features
- Handles both **image** and **code** scopes.
- Reads pre-defined prompts specified in JSON files.
- Uses an argument parser for structured command-line input.
- Supports various Large Language Models to evaluate student assignment submissions.
- Saves response output in Markdown format with a predefined template or prints to stdout.

## Assumptions 
### Code Scope 
#### Test Files 
To test the program and run the models, we assume that the test assignment files follow a specific directory structure. Currently, this program has been tested using from *Homework 5* of the *GGR274* class at the *University of Toronto*.  

##### Directory Structure  

Mock student submissions are stored in a directory named `ggr274_homework5`. Within this directory, mock submissions are contained in a separate subdirectory `ggr274_homework5/test#`. The following naming convention is used for the files:  

- `Homework_5_Solution.ipynb` – Instructor-provided solution file  
- `student_submission.ipynb` – Student's submission file  
- `test#_error_output.txt` – Error trace file for the corresponding test case  

Each different test folder contains variations of `student_submission.ipynb` with different errors to simulate common student mistakes.  

##### Preprocessing Jupyter Notebook Files  

Since OpenAI does not support direct uploads of `.ipynb` files, a preprocessing step is required to convert them to `.txt` format. Before running `main.py`, the following command can be executed:  

```bash
python helpers/file_converter.py
```  

This script will convert all Jupyter notebook files in the `ggr274_homework5` directory into `.txt` files for processing.  

##### File Formatting Assumptions  

To ensure proper extraction and evaluation of student responses, the following format is assumed for `Homework_5_Solution.txt` and `student_submission.txt`:  

- Each task must be clearly delimited using markdown headers in the format:  
  ```markdown
  ## Task {#}
  ```  
  This allows the program to isolate specific questions when using the `--question` argument, ensuring the model only evaluates errors related to the specified question.  

- Each file must start with:  
  ```markdown
  ## Introduction
  ```  
  This section serves as the general assignment instructions and is not included in error evaluation.  


## Usage

Run the script with the required arguments:

```bash
python main.py \
  --submission_type <file_type> \
  --prompt <prompt_name> \
  --scope <image|code> \
  --assignment <assignment_name> \
  --question <question_number> \
  --model <model_name> \
  --output <markdown|stdout>
```

### Example Commands
#### Generate Markdown Output for Table Evalutation of Student Submission
```bash
python main.py --submission_type jupyter --prompt code_table \
  --scope code --assignment test1 --model deepSeek-R1:70B --output markdown
```

#### Generate Markdown Output for Table Evalutation of Question 1 of Student Submission
```bash
python main.py --submission_type jupyter --prompt code_table \
  --scope code --assignment test1 --question 1 --model deepSeek-R1:70B --output markdown
```


## Argument Details
| Argument          | Description                                      | Required |
|------------------|--------------------------------------------------|----------|
| `--submission_type` | Type of submission (from `arg_options.FileType`) | ✅ |
| `--prompt`       | The prompt name (from `arg_options.Prompt`) | ✅ |
| `--scope`        | Processing scope (`image` or `code`)             | ✅ |
| `--assignment`   | Name of the directory which contains test files (any subdirectory of 'ggr274_homework5')| ✅ |
| `--question`     | Question number (optional)                        | ❌ |
| `--model`        | Model type (from `arg_options.Models`)           | ✅ |
| `--output`       | Output type (`markdown` or `stdout`)             | ✅ |

## Scope 
The program supports two distinct scopes: code or image. Depending on whether "code" or "image" is selected, the program supports different models and prompts tailored for each option.

If the "code" scope is selected, the program will identify student errors in the code sections of the assignment, comparing them to the solution code. Additionally, if the `--scope code` option is chosen, the `--question` option can also be specified to analyze the code for a particular question rather than the entire file. In order to use the `--question` option, the question code in both the solution and submission file must be delimited by '## Task {#}'. See the [Assumptions](#Assumptions) section above. 

## Submission Type 
Currently, jupyter notebook assignments are supported. 

## Prompts 
To view the predefined prompts, navigate to the /prompts folder. Each prompt is stored as a JSON object with the following structure:

```json
{
  "prompt_content": "The text prompt that will be sent to the model",
  "include_question_context": ,
  "include_submission_image": ,
  "include_solution_image": 
}
```

Prompt Naming Conventions: 
- Prompts to be used when --scope code is selected are prefixed with code_
- Prompts to be used when --scope image is selected are prefixed with image_

If the --scope argument is provided and its value does not match the prefix of the selected --prompt, an error message will be displayed.

### Code Scope Prompts 
| Prompt Name          | Description                                  | 
|------------------|--------------------------------------------------|
| `code_explanation.json` | Outputs paragraph explanation of errors. |
| `code_hint.json`       | Outputs short hints on what errors are. |
| `code_lines.json`        | Outputs only code lines where errors are caused.       | 
| `code_table.json`   | Outputs a table which shows the question requirement, the student’s attempt, and potential issue.  |
| `code_template.json`     | Outputs a template format specified to include error type, description, solution. |


## Models 
The models used can be seen under the /models folder. 
### OpenAI 
#### Code Scope 
- Model Name: gpt-4-turbo
- System Prompt: Behaviour of model is set with INSTRUCTIONS prompt from helpers/constants.py.
- Features: 
    - Assistant: Uses the OpenAI Assistant Beta Feature, allowing customized model for specific tasks. 
    - Vector Store: The model creates and manages a vector store for data retrieval.
    - Tools Used: Supports file_search for retrieving information from uploaded files.
    - Cleanup: Uploaded files and models are deleted after processing, in order to manage API resources.
- [OpenAI Assistants Documentation](https://platform.openai.com/docs/assistants/overview)

Note: If you wish to use the OpenAI model, you must specify your API key in an .env file. Create a .env file in your project directory and add your API key:
```
OPENAI_API_KEY=your_api_key_here
```
### Ollama 
Various models were also tested and ran locally on the Teach CS Bigmouth server by using Ollama. Listed below are the models that were used to test out the project:  

#### Code Scope 

Models: 
- deepSeek-R1:70B [Documentation](https://ollama.com/library/deepseek-r1)
- codellama:latest [Documentation](https://ollama.com/library/codellama)

#### Using Ollama  
In order to run this project on Bigmouth: 
1. SSH into teach.cs
```bash
ssh username@teach.cs.utoronto.ca
```
2. SSH into bigmouth (access permission required)
```bash
ssh bigmouth
```
3. Go into the project directory
4. Start Ollama 
```bash
ollama start 
```
5. Run the main.py script

Ollama can also be installed on your personal computer in order to run models locally (https://ollama.com/).

## Output Structure
When `--output markdown` is selected, the script will:
1. Load `helpers/output_template.md`
2. Format it with the provided arguments and processing results.
3. Save it under `test_responses_md/<assignment>/<model>/<prompt>_<timestamp>.md`

Example Markdown file name:
```
test_responses_md/test1/openai/code_table_20250310_143500.md
```

When `--output stdout` is selected, the prompt used and generated response will be sent to stdout.


