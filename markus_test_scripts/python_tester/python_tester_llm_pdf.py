import pytest
import os
import os.path 
from llm_helpers import *

PROMPT_PDF = "Does the student correctly respond to the question, and meet all the criteria that's stated in the rubric? Respond with a JSON array of objects, where each object contains `description`, a description of the problem, `location`, the location of the issue in the pdf text as a coordinate pair, and `page` the page of the pdf where the problem is."
def test_with_markers(request):
    """ Generates LLM response """
    # Run LLM feedback
    llm_feedback = run_llm(submission="python", scope="text", output="stdout",
                           model="openai", prompt="text_pdf_analyze")
  
    request.node.add_marker(pytest.mark.markus_message(llm_feedback))
    # Display LLM output in the overall comment
    request.node.add_marker(pytest.mark.markus_overall_comments(llm_feedback))

    # outputs = extract_json(llm_feedback)

    # for output in outputs:
    #     x1, y1, x2, y2 = convert_coordinates(output["location"])
    #     page = output["page"]
    #     request.node.add_marker(pytest.mark.markus_annotation(
    #         type="PdfAnnotation",
    #         filename=os.path.relpath("student_pdf_submission.pdf", os.getcwd()),
    #         content=output["description"],
    #         x1=x1,
    #         y1=y1,
    #         x2=x2,
    #         y2=y2,
    #         page=page
    #     ))
