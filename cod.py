""" A Python module for generating summaries of documents using the CoD prompt. """
import openai


VERBOSITY_GUIDELINES = """
The first summary should be long (4-5 sentences, ~80 words)
yet highly non-specific, containing little information beyond
the entities marked as missing.
Use overly verbose language and fillers (e.g., "this article discusses")
to reach ~80 words.
"""

FUSION_INSTRUCTIONS = """
- Make every word count: re-write the previous summary to improve flow
 and make space for additional entities.
- Make space with fusion, compression, and removal of uninformative phrases
like "the article discusses".
"""

ENTITY_CONSTRAINTS = """
A Missing Entity is:
- Relevant: to the main story
- Specific: descriptive yet concise (5 words or fewer)
- Novel: not in the previous summary
- Faithful: present in the Article
- Anywhere: located anywhere in the Article
"""

RESULT_FORMAT = """
  The result format is a JSON object with the following fields:
  {
    previous_summary: "The previous summary text",
    missing_entities: ["entity1", "entity2", "entity3"]
   "summary": "The summary text",
  }
"""


def gen_prompt(document: str) -> str:
    """
    Generate the CoD prompt for a document.
    """
    prompt = (
        f"Article: {{{document}}}\n"
        "You will generate increasingly concise, entity-dense summaries of "
        "the above Article.\n"
        f"{VERBOSITY_GUIDELINES}\n"
        f"{FUSION_INSTRUCTIONS}\n"
        'Step 1. Identify 1-3 informative Entities (";" delimited) from the '
        "Article which are missing from the previously generated summary.\n"
        "Step 2. Write a new, denser summary of identical length which covers "
        "every entity and detail from the previous summary plus the Missing "
        "Entities.\n"
        f"{VERBOSITY_GUIDELINES}\n"
        f"{RESULT_FORMAT}\n"

    )
    return prompt


def cod_summarize(document: str, steps: int, debug: bool = False) -> list:
    """
    Generate a summary of a document using the CoD prompt.
    :param document: The document to summarize.
    :type document: str
    :param steps: The number of steps to perform for summarization.
    :type steps: int
    :return: A list of summaries generated using the CoD prompt.
    :rtype: list of str
    """

    # Check if the inputs are valid
    if not isinstance(document, str) or not document:
        raise ValueError("Document must be a non-empty string")
    if not isinstance(steps, int) or steps < 1 or steps > 5:
        raise ValueError("Steps must be an integer between 1 and 5")

    # Initialize an empty list to store the summaries
    summaries = []

    # Loop through the number of steps
    for i in range(steps):
        # Construct the CoD prompt with the document and the previous summary

        prompt = gen_prompt(document)

        if i > 0:
            # Add the previous summary to the prompt
            prev_summary = summaries[-1]
            prompt += prev_summary

        # Call the OpenAI API with the prompt and other parameters
        try:
            print(f"Generating summary... number {i+1}")
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-16k",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an AI assistant expert summary.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=1024,
            )
            summary = response.choices[0].message.content

            if debug:
                print(summary)

            # Append the summary to the list
            summaries.append(summary)
        except openai.error.OpenAIError as error:
            # Handle any errors from the API
            print(f"OpenAI error: {error}")
            break

    # Return the list of summaries
    return summaries
