#!/bin/bash

ANNOTATION_PROMPT="These are the student mistakes you previously identified in the
last message. For each of the mistakes you identified, return a JSON object containing
an array of annotations, referencing the student's submission file for line and column #s.
Each annotation should include: filename: The name of the student's file. content:
A short description of the mistake. line_start and line_end: The line number(s) where the
mistake occurs. column_start and column_end: The column number(s) where the
mistake occurs. Ensure the JSON is valid and properly formatted. Here is a sample format
of the json array to return: { \"annotations\": [{\"filename\": \"student_code.py\",
\"content\": \"Variable 'x' is unused.\", \"line_start\": 5, \"line_end\": 5, \"column_start\": 0,
\"line_end\": 2},]}. ONLY return the json object and nothing else, with no markdown wrapped
around the json object. Make sure the line #s don't exceed the number of lines in the file and
the column lines don't exceed the number of columns for each line. You can use markdown
syntax in the annotation's content, especially when denoting code. column_start should be 0."

TEST_NAME="LLM Feedback Test"

PYTHON_BIN="/home/docker/.autotesting/scripts/defaultvenv/bin/python"

submission=""
solution=""

while IFS= read -r -d '' file; do
  filename=$(basename "$file")
  lowercase_name=$(echo "$filename" | tr '[:upper:]' '[:lower:]')
  if [[ -z "$submission" && "$lowercase_name" == *student_submission* && "$lowercase_name" != *.png ]]; then
    submission="$file"
  elif [[ -z "$solution" && "$lowercase_name" == *instructor_solution* ]]; then
    solution="$file"
  fi
done < <(find ./ -type f -print0)

CMD=("$PYTHON_BIN" -m ai_feedback \
  --submission_type jupyter \
  --prompt code_template \
  --scope code \
  --model openai)

if [[ -n "$submission" ]]; then
  CMD+=(--submission "$submission")
fi

if [[ -n "$solution" ]]; then
  CMD+=(--solution "$solution")
fi

MAIN_OUTPUT=$("${CMD[@]}" 2>&1)

OVERALL_COMMENT=$(echo "$MAIN_OUTPUT" | jq -R -s .)

echo "{\"name\": \"$TEST_NAME\", \"output\": $OVERALL_COMMENT, \"marks_earned\": 1, \"marks_total\": 1, \"status\": \"pass\", \"time\": null}"

echo "{\"overall_comment\": $OVERALL_COMMENT}"


# UNCOMMENT TO CREATE ANNOTATIONS ON THE test1_output.txt file

# ANNOTATIONS_OUTPUT=$($PYTHON_BIN -m ai_feedback \
#       --submission_type jupyter \
#       --prompt_text "Previous message: $OVERALL_COMMENT. $ANNOTATION_PROMPT" \
#       --scope code \
#       --model openai \
#       --assignment ./ \
#       --output direct 2>&1)
# ANNOTATIONS_OUTPUT_STR=$(echo "$ANNOTATIONS_OUTPUT" | jq -R -s .)
# echo "$ANNOTATIONS_OUTPUT"
