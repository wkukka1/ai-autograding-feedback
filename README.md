# ai-autograding-feedback

## Overview
This program is part of an exploratory project to evaluate the quality of LLM-generated feedback in assisting with assignment grading and enhancing student learning. This program processes either the code sections, text sections, or images of a student's submission to programming assignments, based on the provided arguments. It generates output into a markdown file or standard output.

The large language models used and implementation logic vary depending on whether the selected scope is 'image', 'code' or 'text'.

For the code scope, the program takes three files:
- An assignment's solution file
- A student's submission file
- A test file

For the text scope, the program takes two files:
- An assignment's solution file
- A student's submission file

For the image scope, the program takes up to two files, depending on the prompt used:
- A student's submission file
- (Optional) An assignment's solution file

## Features
- Handles **image**, **text** and **code** scopes.
- Reads pre-defined prompts specified in JSON files.
- Uses an argument parser for structured command-line input.
- Supports various Large Language Models to evaluate student assignment submissions.
- Saves response output in Markdown format with a predefined template or prints to stdout.

## Argument Details
| Argument             | Description                                                         | Required |
|----------------------|---------------------------------------------------------------------|----------|
| `--submission_type`  | Type of submission (from `arg_options.FileType`)                    | ❌ |
| `--prompt`           | Pre-defined prompt name or file path to custom prompt file          | ❌ **|
| `--prompt_text`      | String prompt                                                       | ❌ ** |
| `--scope`            | Processing scope (`image` or `code` or `text`)                      | ✅ |
| `--submission`       | Submission file path                                                | ✅ |
| `--question`         | Specific question to evaluate                                       | ❌ |
| `--model`            | Model type (from `arg_options.Models`)                              | ✅ |
| `--output`           | File path for where to record the output                            | ❌ |
| `--solution`         | File path for the solution file                                     | ❌ |
| `--test_output`      | File path for the file containing the results from tests            | ❌ |
| `--submission_image` | File path for the submission image file                             | ❌ |
| `--solution_image`   | File path for the solution image file                               | ❌ |
| `--system_prompt`    | Pre-defined system prompt name or file path to custom system prompt | ❌ |
| `--llama_mode`       | How to invoke deepSeek-v3 (choices in `arg_options.LlamaMode`)      | ❌ |
| `--output_template`  | Output template file (from `arg_options.OutputTemplate)             | ❌ |
| `--json_schema`      | File path to json file for schema for structured output             | ❌ |
** One of either `--prompt` or `--prompt_text` must be selected. If both are provided, `--prompt_text` will be appended to the contents of the file specified by `--prompt`.

## Scope
The program supports three scopes: code or text or image. Depending on which is selected, the program supports different models and prompts tailored for each option.

If the "code" scope is selected, the program will identify student errors in the code sections of the assignment, comparing them to the solution code. Additionally, if the `--scope code` option is chosen, the `--question` option can also be specified to analyze the code for a particular question rather than the entire file. Currently, you can specify a question number if the file type is jupyter notebook.  In order to use the `--question` option, the question code in both the solution and submission file must be delimited by '## Task {#}'. See the File Formatting Assumptions section.

If the "text" scope is selected, the program will identify student errors in the written responses of the assignment, comparing them to the solution's rubric for written responses. If the 'text' scope is chosen, then 'pdf' must be chosen for the submission type.

If the "image" scope is selected, the program will identify issues in submission images, optionally comparing them to reference solutions. Question numbers can be specified by adding the tag `markus_question_name: <question name>` to the metadata for the code cell that generates the submission image. The previous cell's markdown content will be used as the question's context.

## Submission Type
The program automatically detects submission type based on file extensions in the assignment directory:
- Files ending with `_submission.ipynb` → jupyter notebook
- Files ending with `_submission.py` → python file
- Files ending with `_submission.pdf` → PDF document

The user can also explicitly specify the submission type using the `--submission_type` argument if auto-detection is not suitable.

Currently, jupyter notebook, pdf, and python assignments are supported.

## Prompts
The `--prompt` argument accepts either pre-defined prompt names or custom file paths:

### Pre-defined Prompts
To use pre-defined prompts, specify the prompt name (without extension). Pre-defined prompts are stored as markdown (.md) files in the `ai_feedback/data/prompts/user/` directory.

### Custom Prompt Files
To use custom prompt files, specify the file path to your custom prompt. The file should be a markdown (.md) file.

Prompt files can contain template placeholders with the following structure:

```markdown
Consider this question:
{context}

{submission_image}

Do the graphs in the attached image solve the problem? Do not include an example solution.
```

Prompt files are now stored as markdown (.md) files in the `ai_feedback/data/prompts/user/` directory. Each prompt can contain template placeholders that will be automatically replaced with relevant content.

Prompt Naming Conventions:
- Prompts to be used when --scope code is selected are prefixed with code_{}.md
- Prompts to be used when --scope image is selected are prefixed with image_{}.md
- Prompts to be used when --scope text is selected are prefixed with text_{}.md

Scope validation (prefix matching) only applies to pre-defined prompts. Custom prompt files can be used with any scope.

All prompts are treated as templates that can contain special placeholder blocks, the following template placeholders are automatically replaced:
- `{context}` - Question context
- `{file_references}` - List of files being analyzed with descriptions
- `{file_contents}` - Full contents of files with line numbers
- `{submission_image}` - Student submission image
- `{solution_image}` - Reference solution image

### Code Scope Prompts
| Prompt Name          | Description                                  |
|------------------|--------------------------------------------------|
| `code_explanation.md` | Outputs paragraph explanation of errors. |
| `code_hint.md`       | Outputs short hints on what errors are. |
| `code_lines.md`        | Outputs only code lines where errors are caused.       |
| `code_table.md`   | Outputs a table which shows the question requirement, the student’s attempt, and potential issue.  |
| `code_template.md`     | Outputs a template format specified to include error type, description, solution. |
| `code_annotation.md`     | Outputs a json object of a list of annotation objects to display student errors on MarkUs. This is intended for markus integration usage. |

### Image Scope Prompts
| Prompt Name          | Description                                  |
|------------------|--------------------------------------------------|
| `image_analyze.md` | Outputs whether the submission image answers the question provided by the context. |
| `image_analyze_annotations.md` | Outputs whether the submission image answers the question provided by the context as a list of JSON objects, each with a description of the issue and a location on the image. Intended for MarkUs integration usage. |
| `image_compare.md` | Outputs table comparing style elements between submission and solution graphs. |
| `image_style.md` | Outputs table checking the style elements in a submission graph. |
| `image_style_annotations.md` | Outputs evaluations of style elements in a submission graph as a list of JSON objects, each with a description of the issue and a location on the image. Intended for MarkUs integration usage. |

### Text Scope Prompts
| Prompt Name          | Description                                  |
|------------------|--------------------------------------------------|
| `text_pdf_analyze.md` | Outputs whether the submission written response matches all the criteria specified in the solution. |


## Prompt_text
Additonally, the user can pass in a string through the --prompt_text argument. This will either be concatenated to the prompt if --prompt is used or fed in as the only prompt if --prompt is not used.

## System Prompts
The `--system_prompt` argument accepts either pre-defined system prompt names or custom file paths:

### Pre-defined System Prompts
To use pre-defined system prompts, specify the system prompt name (without extension). Pre-defined system prompts are stored as markdown (.md) files in the `ai_feedback/data/prompts/system/` directory.

### Custom System Prompt Files
To use custom system prompt files, specify the file path to your custom system prompt. The file should be a markdown (.md) file.

System prompts define the AI model's behavior, tone, and approach to providing feedback. They are used to set the context and personality of the AI assistant.

## Models
The models used can be seen under the ai_feedback/models folder.
### OpenAI Vector Store
- Model Name: gpt-4-turbo
- System Prompt: Behaviour of model is set with INSTRUCTIONS prompt from helpers/constants.py.
- Features:
    - Assistant: Uses the OpenAI Assistant Beta Feature, allowing customized model for specific tasks.
    - Vector Store: The model creates and manages a vector store for data retrieval.
    - Tools Used: Supports file_search for retrieving information from uploaded files.
    - Cleanup: Uploaded files and models are deleted after processing, in order to manage API resources.
- [OpenAI Assistants Documentation](https://platform.openai.com/docs/assistants/overview)

### OpenAI
- Uses the same model as above but doesn't use the vector store functionality. Uploads files as part of the prompt.

Note: If you wish to use OpenAI models, you must specify your API key in an .env file. Create a .env file in your project directory and add your API key:
```
OPENAI_API_KEY=your_api_key_here
```

### Claude
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

## Output Structure
- When `--output filepath` is given, the script will:
1. Load the template for the output based on the `--output_template` (Options defined in ai_feedback/helpers/arg_options.OutputTemplate)
2. Format it with the provided arguments and processing results.
3. Save it under `filepath`

- When the `--output` argument is not given, the prompt used and generated response will be sent to stdout in the format selected by `--output_template`.
- When the `--output_template` argument is not given it will default to `response_only` which is only the response from the model
## Test Files
- Any subdirectory of /test_submissions can be run locally. More examples can be added to this directory using a similar fashion.

## GGR274 Test File Assumptions
### Code Scope
To test the program using the GGR274 files, we assume that the test assignment files follow a specific directory structure. Currently, this program has been tested using *Homework 5* of the *GGR274* class at the *University of Toronto*.

##### Directory Structure

Within the `test_submissions/ggr274_homework5` directory, mock submissions are contained in a separate subdirectories `test_submissions/ggr274_homework5/test#`. The following naming convention is used for the files:

- `Homework_5_solution.ipynb` – Instructor-provided solution file
- `student_submission.ipynb` – Student's submission file
- `test#_error_output.txt` – Error trace file for the corresponding test case

Each test folder contains variations of `student_submission.ipynb` with different errors.

##### File Formatting Assumptions

To ensure proper extraction and evaluation of student responses, the following format is assumed for `Homework_5_solution.ipynb` and `student_submission.ipynb`:

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

## Package Usage

In order to run this package locally:

Ensure you have the environment variables set up (see Models section above).

When you are in a terminal in the repo, run:
```bash
pip install -e .
```

Run the program:
```bash
python -m ai_feedback \
  --submission_type <file_type> \
  --prompt <prompt_name> \
  --scope <image|code|text> \
  --submission <submission_file_path> \
  --solution <solution_file_path> \
  --test_output <test_ouput_path> \
  --submission_image <image_file_path> \
  --solution_image <image_file_path> \
  --question <question_number> \
  --model <model_name> \
  --output <file_path_to> \
  --output_template <file_name> \
  --system_prompt <prompt_file_path> \
  --llama_mode <server|cli>
```

- See the Arguments section for the different command line argument options, or run this command to see help messages and available choices:
```bash
python -m ai_feedback -h
```

### Example Commands

#### Evaluate cnn_example test using openAI model
```bash
python -m ai_feedback --prompt code_lines --scope code --submission test_submissions/cnn_example/cnn_submission --solution test_submissions/cnn_example/cnn_solution.py --model openai
```

#### Evaluate cnn_example test using openAI model and custom prompt
```bash
python -m ai_feedback --prompt_text "Evaluate the student's code readability." --scope code --submission test_submissions/cnn_example/cnn_submission.py --model openai
```

#### Evaluate pdf_example test using openAI model
```bash
python -m ai_feedback --prompt text_pdf_analyze --scope text --submission test_submissions/pdf_example/student_pdf_submission.pdf --model openai
```

#### Evaluate question1 of test1 of ggr274 homework using DeepSeek model
```bash
python -m ai_feedback --prompt code_table \
  --scope code --submission test_submissions/ggr274_homework5/test1/student_submission.ipynb --question 1 --model deepSeek-R1:70B
```

#### Evaluate the image for question 5b of ggr274 homework with Llama3.2-vision
```sh
python -m ai_feedback --prompt image_analyze --scope image --solution ./test_submissions/ggr274_homework5/image_test2/student_submission.ipynb --submission_image test_submissions/ggr274_homework5/image_test2/student_submission.png --question "Question 5b" --model llama3.2-vision:90b
```

### Evaluate the bfs example with remote model to test_file using the verbose template
```sh
python -m ai_feedback --prompt code_lines --scope code --solution ./test_submissions/bfs_example/bfs_solution.py --submission test_submissions/bfs_example/bfs_submission.py --model remote --output --output test_file --output_template verbose
```

#### Evalute the Jupyter notebook of test1 of ggr274 using DeepSeek-v3 via llama.cpp server
```sh
python3 -m ai_feedback --prompt code_table --scope code \
        --submission test_submissions/ggr274_homework5/test1/student_submission.ipynb \
        --solution test_submissions/ggr274_homework5/test1/Homework_5_solution.ipynb \
        --model deepSeek-v3 --llama_mode server
```

#### Evalute the Jupyter notebook of test1 of ggr274 using DeepSeek-v3 via llama.cpp cli
```sh
python3 -m ai_feedback --prompt code_table --scope code \
        --submission test_submissions/ggr274_homework5/test1/student_submission.ipynb \
        --solution test_submissions/ggr274_homework5/test1/Homework_5_solution.ipynb \
        --model deepSeek-v3 --llama_mode cli
```


#### Get annotations for cnn_example test using openAI model
```bash
python -m ai_feedback --prompt code_annotations --scope code --submission test_submissions/cnn_example/cnn_submission --solution test_submissions/cnn_example/cnn_solution.py --model openai --json_schema ai_feedback/data/schema/code_annotation_schema.json
```

#### Evaluate using custom prompt file path
```bash
python -m ai_feedback --prompt ai_feedback/data/prompts/user/code_overall.md --scope code --submission test_submissions/csc108/correct_submission/correct_submission.py --solution test_submissions/csc108/solution.py --model codellama:latest
```

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
3. Ensure you're in the project directory
4. Start Ollama
```bash
ollama start
```
5. Ensure models specified in repo are downloaded
```bash
ollama list
```
6. Run the script according to the Package Usage section above.


## Markus Integration
This python package can be used as a dependency in the Markus Autotester, in order to display LLM generated feedback as overall comments and test outputs, and as annotations on the submission file. Following the instructions below to set up the Autotester, once 'Run Tests' is pressed, these comments and annotations should appear automatically on the Markus UI.

### Markus Test Scripts
- /markus_test_scripts contains scripts which can be uploaded to the autotester in order to generate LLM Feedback
- Currently, only openAI and Claude models are supported.
- The /test_submissions directory has mock assignment submissions, solutions, and test files, used for testing the markus integration. These files can be submitted on the markus autotester along with the llm script files.
- Within these llm script files, the models and prompts used can be changed by editing the command line arguments, through the run_llm() function.

Files:
- python_tester_llm_code.py: Runs LLM on any code assignment (solution file, submission file) uploaded to the autotester. First, creates general feedback and displays as overall comments and test output (can use any prompt and model). Second, feeds in the output of the first LLM response into the model again, asking it to create annotations for the student's mistakes. (Ensure to change submission file import name.)
- llm_helpers.py: contains helper functions needed to run llm scripts.
- python_tester_llm_pdf.py: Runs LLM on any pdf assignment (solution file and submission file) uploaded to the autotester. Creates general feedback about whether the student's written responses matches the instructors feedback. Dislayed in test outputs and overall comments.
- custom_tester_llm_code.sh: Runs LLM on assignments (solution file, submission file, test output file) uploaded to the custom autotester. Currently, supports jupyter notebook files uploaded. Can specify prompt and model used in the script. Displays in overall comments and in test outputs. Can optionally uncomment the annotations section to display annotations, however the annotations will display on the .txt version of the file uploaded by the student, not the .ipynb file.

#### Python AutoTester Usage
##### Code Scope
1. Ensure the student has submitted a submission file (_submission suffixed).
2. Ensure the instructor has submitted a solution file (_solution suffixed), llm_helpers.py (located in /markus_test_scripts), and python_tester_llm_code.py (located in /markus_test_scripts). Instructor can also upload another pytest file which can be run as its own test group.
3. Ensure the submission import statement in python_tester_llm_code.py matches the name of the student's submission file name.
4. Create a Python Autotester Test Group to run the LLM File.
5. In the Package Requirements section of the Test Group Settings for the LLM file, put:
``` bash
git+https://github.com/MarkUsProject/ai-autograding-feedback.git#egg=ai_feedback
```
Along with any other packages that the submission or solution file uses.

6. Ensure the Timeout is set to 120 seconds or longer.
7. Ensure Markus Autotester docker container has the API Keys in an .env file and specified in the docker compose file.

##### Text Scope
- Do the same as the code scope, but ensure that the student submission and instructor solution are .pdf files with the same naming assumption. Also, ensure that python_tester_llm_pdf.py is uploaded as the test script.

#### Running Python Autotester Examples
##### CNN Example
- Look at the /test_submissions/cnn_example directory for the following files
- Instructor uploads: cnn_solution.py, cnn_test.py, llm_helpers.py, python_tester_llm_code.py files
- Separate test groups for cnn_test.py and python_tester_llm_code.py
- cnn_test.py Autotester package requirements: torch numpy
- python_tester_llm_code.py Autotester package requirements: git+https://github.com/MarkUsProject/ai-autograding-feedback.git#egg=ai_feedback numpy torch
- Student uploads: cnn_submission.pdf

##### BFS Example
- Look at the /test_submissions/bfs_example directory for the following files
- Instructor uploads: bfs_solution.py, test_bfs.py, llm_helpers.py, python_tester_llm_code.py files
- Separate test groups for test_bfs.py and python_tester_llm_code.py
- python_tester_llm_code.py Autotester package requirements: git+https://github.com/MarkUsProject/ai-autograding-feedback.git#egg=ai_feedback
- Student uploads: bfs_submission.pdf

##### PDF Example
- Look at the /test_submissions/pdf_example directory for the following files
- Instructor uploads: instructor_pdf_solution.pdf, llm_helpers.py, python_tester_llm_pdf.py files
- Autotester package requirements: git+https://github.com/MarkUsProject/ai-autograding-feedback.git#egg=ai_feedback
- Student uploads: student_pdf_submission.pdf

#### Custom Tester Usage
1. Ensure the student has submitted a submission file (_submission suffixed).
2. Ensure the instructor has submitted a solution file (_solution suffixed) and custom_tester_llm_code.sh (located in /markus_test_scripts). Instructor can also upload another script used to run its own test group. (See below for GGR274 Example.)
3. In the Markus Autotesting terminal:
``` bash
 docker exec -it -u 0 markus-autotesting-server-1 /bin/bash
```
Then as the root user, install the package:
``` bash
/home/docker/.autotesting/scripts/defaultvenv/bin/pip install git+https://github.com/MarkUsProject/ai-autograding-feedback.git#egg=ai_feedback
```
Also pip install other packages that the submission or solution file uses.

4. Create a Custom Autotester Test Group to run the LLM script file.
5. Ensure the Timeout is set to 120 seconds or longer.
6. Ensure Markus Autotester docker container has the API Keys in an .env file and specified in the docker compose file.

##### GGR274 Test1 Example
- Look at the /test_submissions/ggr274_hw5_custom_tester directory for the following files
- Instructor uploads: Homework_5_solution.ipynb, test_hw5.py, test_output.txt, custom_tester_llm_code.sh, run_hw5_test.sh
- Two separate test groups: one for run_hw5_test.sh, and one for custom_tester_llm_code.sh
- Student uploads: test1_submission.ipynb,  test1_submission.txt

NOTE: if the LLM Test Group appears to be blank/does not turn green, try increasing the timeout.

#### Custom Tester
- custom_tester_llm_code.sh: Runs LLM on any assignment (solution file, submission file, test output file) uploaded to the autotester. Can specify prompt and model used in the script. Displays in overall comments and in test outputs.

## Developers

To install project dependencies, including development dependencies:

```console
$ pip install -e .[dev]
```

To install pre-commit hooks:

```console
$ pre-commit install
```

To run the test suite:

```console
$ pytest
```
