# ai-autograding-feedback

## Overview
This program is part of an exploratory project to evaluate the quality of LLM-generated feedback in assisting with assignment grading and enhancing student learning. This program processes either the code sections or images of a student's submission to programming assignments, based on the provided arguments. It generates output into a markdown file or standard output. 

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
To test the program and run the models, we assume that the test assignment files follow a specific directory structure. Currently, this program has been tested using *Homework 5* of the *GGR274* class at the *University of Toronto*.  

##### Directory Structure  

Within the `ggr274_homework5` directory, mock submissions are contained in a separate subdirectories `ggr274_homework5/test#`. The following naming convention is used for the files:  

- `Homework_5_Solution.ipynb` – Instructor-provided solution file  
- `student_submission.ipynb` – Student's submission file  
- `test#_error_output.txt` – Error trace file for the corresponding test case  

Each test folder contains variations of `student_submission.ipynb` with different errors.  

##### Preprocessing Jupyter Notebook Files  

Note: Since OpenAI does not support direct uploads of `.ipynb` files, a preprocessing step is required to convert them to `.txt` format. Before running `main.py`, the following command can be executed:  

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

### Image Scope 
#### Test Files
Mock student submissions are stored in `ggr274_homework5/image_test#`. The following naming convention is used for the files:  
- `solution.ipynb` – Instructor-provided solution file  
- `student_submission.ipynb` – Student's submission file

##### Notebook Preprocessing
To grade a specific question using the `--question` argument, add the tag `markus_question_name: <question name>` to the metadata for the code cell that generates an image to be graded. The previous cell's markdown content will be used as the question's context.

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
Run this command to see help messages and available choices: 
```bash
python main.py -h
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
| `--prompt`       | The prompt name (from `arg_options.Prompt`) | ❌ **|
| `--prompt_text`       | Additional customizable prompt text that can be fed to model. | ❌ ** |
| `--scope`        | Processing scope (`image` or `code`)             | ✅ |
| `--assignment`   | Name of the directory which contains test files (any subdirectory of 'ggr274_homework5')| ✅ |
| `--question`     | Specific question to evaluate                      | ❌ |
| `--model`        | Model type (from `arg_options.Models`)           | ✅ |
| `--output`       | Output type (`markdown` or `stdout`)             | ✅ |

** One of either prompt or prompt_text must be selected. 

## Scope 
The program supports two distinct scopes: code or image. Depending on whether "code" or "image" is selected, the program supports different models and prompts tailored for each option.

If the "code" scope is selected, the program will identify student errors in the code sections of the assignment, comparing them to the solution code. Additionally, if the `--scope code` option is chosen, the `--question` option can also be specified to analyze the code for a particular question rather than the entire file. In order to use the `--question` option, the question code in both the solution and submission file must be delimited by '## Task {#}'. See the [Assumptions](#Assumptions) section above. 

## Submission Type 
Currently, jupyter notebook and python assignments are supported. 

## Prompts 
To view the predefined prompts, navigate to the /prompts folder. Each prompt is stored as a JSON object with the following structure:

```json
{
  "prompt_content": "The text prompt that will be sent to the model",
  "include_question_context": true/false,
  "include_submission_image": true/false,
  "include_solution_image": true/false 
}
```

Prompt Naming Conventions: 
- Prompts to be used when --scope code is selected are prefixed with code_{}.json
- Prompts to be used when --scope image is selected are prefixed with image_{}.json

If the --scope argument is provided and its value does not match the prefix of the selected --prompt, an error message will be displayed.

Prompt Extra Options (for image scope only):
- `include_question_context` (true/false): If set to true, a `{context}` field can be added to the prompt, which will be replaced with the markdown content of the cell before the code cell with the `markus_question_name` tag.
- `include_submission_image` (true/false): Whether the student submission image should be attached in the prompt.
- `include_solution_image` (true/false): Whether the solution image should be attached in the prompt.

### Code Scope Prompts 
| Prompt Name          | Description                                  | 
|------------------|--------------------------------------------------|
| `code_explanation.json` | Outputs paragraph explanation of errors. |
| `code_hint.json`       | Outputs short hints on what errors are. |
| `code_lines.json`        | Outputs only code lines where errors are caused.       | 
| `code_table.json`   | Outputs a table which shows the question requirement, the student’s attempt, and potential issue.  |
| `code_template.json`     | Outputs a template format specified to include error type, description, solution. |
| `code_annotation.json`     | Outputs a json object of a list of annotation objects to display student errors on MarkUs. |

### Image Scope Prompts 
| Prompt Name          | Description                                  | 
|------------------|--------------------------------------------------|
| `image_analyze.json` | Outputs whether the submission image answers the question provided by the context. |
| `image_compare.json` | Outputs table comparing style elements between submission and solution graphs. |
| `image_style.json` | Outputs table checking the style elements in a submission graph. |

## Models 
The models used can be seen under the /models folder. 
### OpenAI Vector Store 
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
### OpenAI 
- Uses the same model as above but doesn't use the vector store functionality. Uploads files as part of the prompt. 

### Claude
#### Code Scope 
- Model Name: claude-3.7-sonnet
- System Prompt: Behaviour of model is set with INSTRUCTIONS prompt from helpers/constants.py.
- [Claude Documentation](https://www.anthropic.com/claude/sonnet)

Note: If you wish to use the Claude model, you must specify your API key in an .env file. Create a .env file in your project directory and add your API key:
```
CLAUDE_API_KEY=your_api_key_here
```

### Ollama 
Various models were also tested and run locally on the Teach CS Bigmouth server by using Ollama. Listed below are the models that were used to test out the project:  

#### Code Scope 

Models: 
- deepSeek-R1:70B [Documentation](https://ollama.com/library/deepseek-r1)
- codellama:latest [Documentation](https://ollama.com/library/codellama)

#### Image Scope
- llama3.2-vision:90b [Documentation](https://ollama.com/library/llama3.2-vision)
- - This model only supports at most one image attachment.
- llava:34b [Documentation](https://ollama.com/library/llava)

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
- When `--output markdown` is selected, the script will:
1. Load `helpers/output_template.md`
2. Format it with the provided arguments and processing results.
3. Save it under `test_responses_md/<assignment>/<model>/<prompt>_<timestamp>.md`

Example Markdown file name:
```
test_responses_md/test1/openai/code_table_20250310_143500.md
```

- When `--output stdout` is selected, the prompt used and generated response will be sent to stdout.
- When `--output direct` is selected, only the generated response will be sent to stdout.


## Markus Integration 
- Code was slightly modified to integrate with MarkUs and no longer depends on GGR274 Assignment Folder 
- To integrate this code base with MarkUs: 
  - Upload this entire repository to autotester settings as a folder (File Upload section)
  - Upload the instructor's solution code (file must be suffixed with _solution) and assignment test files to autotester. Student's submission file must also be suffixed with _submission when uploaded.
  - Upload one of the scripts from the /markus_test_scripts folder and set up a test group to run the script. The LLM script and test files must be separate test groups. The script contains commands to run this repository and generate LLM feedback for the student's submission file, which will be displayed in overall comments and annotations on MarkUs. 
- Ensure markus autotester docker container has the API Keys in an .env file and specified in the docker compose file
- Ensure markus autotester virtual environment has all libraries downloaded specified in requirements.txt file
- Ensure test timeouts are set to 60 seconds or longer due to API request latency

### Markus Test Scripts 
- /markus_test_scripts contains scripts which can be uploaded to the autotester in order to generate LLM Feedback 
- Currently, only openAI and Claude models are supported. 

#### Python Tester 
- run_llm_combined.py: Runs LLM on any assignment (solution file, submission file) uploaded to the autotester. First, creates general feedback and displays as overall comments and test output (can use any prompt and model). Second, feeds in the output of the first LLM response into the model again, asking it to create annotations for the student's mistakes. Prompt can be seen in the script. 
- run_llm_feedback.py: Runs LLM on any assignment (solution file, submission file) uploaded to the autotester. Can specify prompt and model used in the script. Displays in overall comments and in test outputs. 
- run_llm_annotation.py: Runs LLM on any assignment (solution file, submission file) uploaded to the autotester. Uses the code_annotation.json prompt and model can be specified in the script. Displays in test outputs and as annotations. 

#### Custom Tester 
- run_hw5_test.sh: Runs test for GGR274 HW5 assignment
- run_llm_jupyter.sh: Runs LLM on any assignment (solution file, submission file, test output file) uploaded to the autotester. Can specify prompt and model used in the script. Displays in overall comments and in test outputs. 
