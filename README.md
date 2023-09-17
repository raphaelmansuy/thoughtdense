# thoughtdense

## Description

Author: Raphaël MANSUY

## Overview

thoughtdense analyzes text and generates a concise summary using Chain Of Density technique as described in the paper [From Sparse to Dense:
GPT-4 Summarization with Chain of Density Prompting](https://arxiv.org/abs/2309.04269).

![thoughtdense](./assets/illustration.png)

## cod-summarizer

This is a Python module for generating multi-step summaries of documents using the Chain Of Density.

## Usage

```python
import cod_summarizer

document = "Article text..."

summaries = cod_summarizer.cod_summarize(document, steps=3)
```

This will generate 3 increasingly concise summaries using the CoD prompt.

The `cod_summarize()` function takes the following arguments:

- `document` - The text of the document to summarize.
- `steps` - The number of summarization steps to perform, between 1 and 5. Default is 3.
- `debug` - Print intermediate summaries if True. Default is False.

It returns a list of summary texts generated at each step.

## Example

```python
import cod_summarizer

text = "Some long text to summarize..."

summaries = cod_summarizer.cod_summarize(text, steps=2)

print(summaries[0]) # Initial verbose summary
print(summaries[1]) # Final concise summary
```

## Prompt Engineering

The module constructs a CoD prompt tailored for summarization, with instructions for an initial verbose summary and iterative improvements asking the model to add missing entities.

The prompt structure and engineering details are encapsulated in the `gen_prompt()` function.

## Usage as a CLI command

```bash
Usage: toughtdense.py summarize [OPTIONS] FILENAME

  Generate a summary of a document using the CoD prompt.

Options:
  --steps INTEGER RANGE  Number of steps.  [default: 5; 1<=x<=5]
  --debug BOOLEAN        [default: False]
  --help                 Show this message and exit.
```

### Example

```bash
python thoughtdense.py summarize --steps 3 --debug True ./demo/demo.txt
```

### Pre-requisites

- Python 3.8 or higher
- OpenAI API key (set as environment variable OPENAI_API_KEY)
