#!/bin/bash

source ../../scripts/defaultvenv/bin/activate
llm_output=$(../../scripts/defaultvenv/bin/python3 ai-autograding-feedback/main.py --prompt image_style --scope image --submission_image ./student_submission.png --submission ./student_submission.ipynb --question "Question 5b" --model openai)
escaped_llm_output=$(printf "$llm_output" | sed 's/"/\\"/g' | awk '{printf "%s\\n", $0}')
escaped_llm_output_truncated=${escaped_llm_output%\\n*}
echo "{\"overall_comment\": \"$(printf "%s" "$escaped_llm_output_truncated")\"} {\"name\": \"AI Grader\", \"output\": \"$(printf "%s" "$escaped_llm_output_truncated")\", \"marks_earned\": 1, \"marks_total\": 1, \"status\": \"pass\", \"time\": 1}"
