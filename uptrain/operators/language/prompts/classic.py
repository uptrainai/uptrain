# Factual Accuracy
FACT_EVAL_PROMPT_TEMPLATE = """
You are a detail-oriented LLM whose task is to determine if the given facts are supported by the given context. 
Each fact is separated by the following symbol: ", ". Go over each fact sentence one by one, and write down your judgement.

{prompting_instructions}

{scenario_description}

Example Data.
{few_shot_examples}

Return the output only in the corresponding JSON format. Do not output anything other than this JSON object:
{output_format}

Task Data.
[Facts]: {facts}
[Context]: {context}
[Output]:
"""

FACT_GENERATE_PROMPT_TEMPLATE = """
You are given a response along with its question. Please breakdown the following response into independent facts. A fact is a sentence that is true and can only be stated from the response. Facts should not depend on each another and must not convey the same information. Limit to 5 facts in the output. 

{scenario_description}

Example Data.
{few_shot_examples}

Return the output only in the corresponding JSON format. Do not output anything other than this JSON object:
{output_format}

Task Data.
[Question]: {question}
[Response]: {response}
[Output]: 
"""


# Context Relevance
CONTEXT_RELEVANCE_PROMPT_TEMPLATE = """
You are a detail-oriented LLM which pays close attention to the details, checks for consistency, and is adept at identifying logical fallacies, incorrect assumptions, or other errors in reasoning.
Your task is to determine if the given context has enough information to answer the given query.

{prompting_instructions}

{scenario_description}

Example Data.
{few_shot_examples}

Compare the semantic similarity of the extracted context with the query. Ignore any differences in style, grammar, or punctuation.
The context may either contain sufficient information to answer the given query completely, or contains relevant but incomplete information to form the answer or doesn't have any relevant information at all. 
Determine which case applies by selecting one of the following options:
(A) The extracted context can answer the given query completely.
(B) The extracted context can give some relevant answer for the given query but can't answer it completely.
(C) The extracted context doesn't contain any information to answer the given query.

Return the output only in the corresponding JSON format. Do not output anything other than this JSON object:
{output_format}

Task Data.
[Query]: {question}
[Extracted Context]: {context}
[Output]:
"""


# Response Completeness
RESPONSE_COMPLETENESS_PROMPT_TEMPLATE = """
You are a detail-oriented LLM which pays close attention to the details, checks for consistency, and is adept at identifying logical fallacies, incorrect assumptions, or other errors in reasoning.
Your task is to determine if the given response is able to answer the given query completely.

{prompting_instructions}

{scenario_description}

Example Data.
{few_shot_examples}

For the provided question-answer pair, please assess if the machine-generated response is relevant and answers the user query adequately. Don't focus on aspects like style, grammar, or punctuation. 
Please form your response by selecting one of the following options. 
(A) The generated answer doesn't answer the given question at all.
(B) The generated answer only partially answers the given question.
(C) The generated answer adequately answers the given question. 

Return the output only in the corresponding JSON format. Do not output anything other than this JSON object:
{output_format}

Task Data.
[Question]: {question}
[Response]: {response}
[Output]:
"""


# Response Conciseness
RESPONSE_CONCISENESS_PROMPT_TEMPLATE = """
You are a detail-oriented LLM which pays close attention to the details, checks for consistency, and is adept at identifying logical fallacies, incorrect assumptions, or other errors in reasoning.
For the provided question-answer pair, please assess if the machine-generated response has any additional irrelevant information or not. Don't focus on aspects like style, grammar, or punctuation. 

{prompting_instructions}

{scenario_description}

Example Data.
{few_shot_examples}

Please form your response by selecting one of the following options. 
(A) The generated answer has a lot of additional irrelevant information.
(B) The generated answer has a little additional irrelevant information.
(C) The generated answer has no additional irrelevant information.

Return the output only in the corresponding JSON format. Do not output anything other than this JSON object:
{output_format}

Task data.
[Question]: {question}
[Response]: {response}
[Output]:
"""


# Response Completeness wrt Context
RESPONSE_COMPLETENESS_WRT_CONTEXT_PROMPT_TEMPLATE = """
You are an extremely detail-orientated and analytical judge whose job is to thoughtfully evaluate a given user query, a piece of context extracted to provide information to respond to it and the LLM-generated response, and determine if the LLM is able to utilize all the relevant information in th context for generating the response.
For the provided task data, please assess if the machine-generated response is able to extract all the relevant information from the context or not. Don't focus on aspects like style, grammar, or punctuation. 

{prompting_instructions}

{scenario_description}

Example Data.
{few_shot_examples}

Please form your response by selecting one of the following options. 
(A) The generated response incorporates all the relevant information present in the context.
(B) The generated response incorporates some of the information present in the context, but misses some of the information in context which is relevant for answering the given question. 
(C) The generated response doesn't incorporate any information present in the context.

Return the output only in the corresponding JSON format. Do not output anything other than this JSON object:
{output_format}

Task data.
[Question]: {question}
[Context]: {context}
[Response]: {response}
[Output]:
"""

# Response Consistency
RESPONSE_CONSISTENCY_PROMPT_TEMPLATE =  """
You are given a question along with a context and a machine generated response. An intelligent LLM generated the given response to answer the given question by utilizing information present in the context.
For the provided task data, come up with an argument to justify why the given answer is appropriate for the given question. Finally give a score between 0 to 1, how logical the argument looks like along with an explanation for the score.

{prompting_instructions}

{scenario_description}

Example Data.
{few_shot_examples}

Return the output only in the corresponding JSON format. Do not output anything other than this JSON object:
{output_format}

Task data.
[Question]: {question}
[Context]: {context}
[Response]: {response}
[Output]:
"""


# Valid Response
VALID_RESPONSE_PROMPT_TEMPLATE =  """
You are given a question and a response generated from an AI assistant. Please assess if the given response contain any information. 

{prompting_instructions}

{scenario_description}

Example Data.
{few_shot_examples}

Determine which case applies by selecting one of the following options:
(A) The given response does contain some information.
(B) The given response does not contain any information.

Even if the response contains any irrelevant information, the choice should be A. Please DON'T check for any response relevancy with respect to the question. 

Return the output only in the corresponding JSON format. Do not output anything other than this JSON object:
{output_format}

Task data:
[Question]: {question}
[Response]: {response}
"""
