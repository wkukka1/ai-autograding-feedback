#!/bin/bash

TEST_NAME="LLM Feedback Test"

# Run main.py to get LLM response 
# Change prompt type and model type here
MAIN_OUTPUT=$(/home/docker/.autotesting/scripts/defaultvenv/bin/python ai-autograding-feedback/main.py \
      --submission_type jupyter \
      --prompt code_template \
      --scope code \
      --model claude-3.7-sonnet \
      --assignment ./ \
      --output stdout 2>&1)

OVERALL_COMMENT=$(echo "$MAIN_OUTPUT" | jq -R -s .)

echo "{\"name\": \"$TEST_NAME\", \"output\": $OVERALL_COMMENT, \"marks_earned\": 1, \"marks_total\": 1, \"status\": \"pass\", \"time\": null}"

echo "{\"overall_comment\": $OVERALL_COMMENT}"
