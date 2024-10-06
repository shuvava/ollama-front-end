from __future__ import annotations

from typing import Any, Mapping, Iterator, Literal, List, Dict

from ollama import Client, Options

from .config import settings

OLLAMA_URL = settings.ollama_url

OLLAMA_OPTIONS = Options(
    temperature=0.0,  # Controls randomness: 0.0 is deterministic, higher values increase randomness
#    num_predict=100,  # Maximum number of tokens to predict
#    top_k=40,  # Limits the next token selection to the K most probable tokens
#    top_p=0.9,  # Selects from the smallest possible set of tokens whose cumulative probability exceeds P
#    repeat_penalty=1.1,  # Penalizes repeated tokens: 1.0 means no penalty, higher values increase the penalty
)

client = Client(OLLAMA_URL)

def chat(messages: List[Dict[str, str]], model: str, json_response: bool) -> Mapping[str, Any] | \
                                                                                             Iterator[
                                                                                                 Mapping[str, Any]]:
    response_format: Literal['', 'json'] = ''
    if json_response:
        response_format = 'json'
    return client.chat(
        model=model,
        messages=messages,
        format=response_format,
        options=OLLAMA_OPTIONS,
    )
