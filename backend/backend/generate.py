import spacy
from spacy.lang.en import English
from collections import deque
import itertools as it
import random
from threading import Thread
from typing import Literal, Optional, TypedDict

import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    StoppingCriteria,
    StoppingCriteriaList,
    TextIteratorStreamer,
)


spacy.prefer_gpu()
nlp = English()


###########
## Types ##
###########

class ChatMLMessage(TypedDict):
    name: Optional[str] = None
    role: Literal["assistant", "system", "user"]
    content: str

ChatML = list[ChatMLMessage]

# Example:
# [
#     {"role": "system", "name": "situation", "content": "I am talking to Diwank"},
#     {"role": "assistant", "name": "Samantha", "content": "Hey Diwank"},
#     {"role": "user", "name": "Diwank", "content": "Hey!"},
# ]

############
## Consts ##
############

AGENT_NAME: str = "Samantha"


###########
## Model ##
###########

# assistant_model_id = "julep-ai/samantha-7b-ds-03"
# assistant_model = AutoModelForCausalLM.from_pretrained(assistant_model_id, torch_dtype=torch.bfloat16, device_map="auto")

# Load model and tokenizer
model_id = "julep-ai/samantha-33b"
tokenizer_id = "julep-ai/samantha-33b"

print("Loading model...")
model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.bfloat16, device_map="auto")
tokenizer = AutoTokenizer.from_pretrained(tokenizer_id, use_fast=False, clean_up_tokenization_spaces=True)

# warmup
model.generate(**tokenizer("Hello", return_tensors="pt").to(0), max_new_tokens=2)

print("Model loaded")


##############
## Generate ##
##############

class StopSequenceCriteria(StoppingCriteria):
    def __init__(
        self,
        tokenizer,
        stop: list[str],
        input_length,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        
        self.stop = stop
        self.tokenizer = tokenizer
        self.input_length = input_length

    def __call__(
        self,
        input_ids: torch.LongTensor,
        scores: torch.FloatTensor,
        **kwargs,
    ) -> bool:

        input_ids = input_ids.long().tolist()
        new_input_ids = [i[self.input_length:] for i in input_ids]
        
        for text in self.stop:
            generated_so_far = ""
            
            for input_id in new_input_ids:
                decoded = self.tokenizer.decode(input_id, skip_special_tokens=False)
                generated_so_far += decoded

                if text in generated_so_far:
                    return True

        return False


def message_role_to_prefix(message: ChatMLMessage) -> str:
    match message:
        case {"role": "system", "name": name, **rest}:
            return name
        case {"role": "user", "name": name, **rest}:
            return f"person ({name})" if name else "person"
        case {"role": "assistant", "name": name, **rest}:
            return f"me ({name})" if name else "me"


def to_prompt(
    messages: ChatML,
    bos: str = "<|section|>",
    eos: str = "<|endsection|>",
    suffix: str = f"\n<|section|>me ({AGENT_NAME})\n",
) -> str:
    # Input format:
    # [
    #     {"role": "system", "name": "situation", "content": "I am talking to Diwank"},
    #     {"role": "assistant", "name": "Samantha", "content": "Hey Diwank"},
    #     {"role": "user", "name": "Diwank", "content": "Hey!"},
    # ]
    
    # Output format:
    #
    # <|section|>situation
    # I am talking to Diwank<|endsection|>
    # <|section|>me (Samantha)
    # Hey Diwank<|endsection|>
    # <|section|>person (Diwank)
    # Hey<|endsection|>
    # <|section|>me (Samantha)\n
    

    prompt = "\n".join([
        f"{bos}{message_role_to_prefix(message)}\n{message['content']}{eos}"
        for message in messages
    ])

    return prompt + suffix


def groupwise(iterable, n):
    """Like itertools.pairwise but for n elements"""

    accum = deque((), n)
    count = 0
    
    for element in iterable:
        accum.append(element)
        count += 1
        
        if len(accum) == n:
            yield tuple(accum)

    if count < n:
        yield tuple(accum)


def wrap_iterator(iterator):
    for item in iterator:
        yield item

# TODO: Turn this into accepting regular expressions instead
def remove_stops(iterator, tokenizer, stop: list[str] = []):

    # If there's nothing to check yield everything as is
    if not stop:
        yield from iterator
        return

    # We need to look ahead n number of tokens so that,
    #   we can check if a stop sequence is coming up
    #   and not yield starting part of the stop sequence.

    # Look ahead by len of largest stop sequence
    look_ahead = max([
        len(tokenizer.encode(s, add_special_tokens=False))
        for s in stop
    ])

    # Group tokens into look_ahead groups
    for items in groupwise(iterator, look_ahead):

        # Check if group has a stop sequence
        joined = "".join(items).strip()
        has_stop_sequence = {s: joined.endswith(s) for s in stop}

        # If so, yield tokens minus stop sequence and return
        if any(has_stop_sequence.values()):
            # which stop sequence was found?
            offending_sequence = next(s for s, is_bad in has_stop_sequence.items() if is_bad)

            # remove that bit, yield and exit
            yield joined.split(offending_sequence)[0]
            return

        # Otherwise, keep yielding the first item in the group
        first, *_ = items
        
        if first.strip():
            yield first

def sentence_stream(token_stream):
    # value containers
    collected = ""

    for token in token_stream:
        # Updated containers
        collected += token
        doc = nlp(collected)

        # Find starting points of sentences
        sent_starts = [token.is_sent_start for token in doc]
        sent_start_idx = [i for i, is_start in enumerate(sent_starts) if is_start]

        # If more than one starting points, then that means there's a sentence in there
        if len(sent_start_idx) > 1:
            # Sentence := everything up to second starting point
            start1, start2, *_ = sent_start_idx

            # Extract and yield that sentence
            sentence = doc[:start2].text_with_ws
            yield sentence

            # and remove it from doc and collected
            collected = collected.replace(sentence, "", 1)
            doc = nlp(doc[start2:].text_with_ws)

    # If token stream has ended and there's still something left, then yield that
    if collected.strip():
        yield collected  # We dont want to strip it just in case there's important whitespace left?


def generate(
    messages: ChatML,
    stop: list[str] = [],
    timeout: int = 15,
    stream: bool = False,
    prompt_settings: dict = {},
    **kwargs
) -> TextIteratorStreamer | str:
    
    # Prepare input
    prompt = to_prompt(messages, **prompt_settings)
    inputs = tokenizer(prompt, return_tensors="pt").to(0)
    input_length = len(inputs["input_ids"].squeeze().tolist())

    # Stopping criteria
    stopping_criteria = (
        StoppingCriteriaList([StopSequenceCriteria(
            tokenizer=tokenizer,
            stop=stop,
            input_length=input_length,
        )])
        if stop else None
    )

    # Generation parameters
    generation_kwargs = {
        # defaults
        "max_new_tokens": 40, 
        "repetition_penalty": 1.02,
        "no_repeat_ngram_size": 4,
        "renormalize_logits": True,
        "temperature": 1.1,
        #
        # overrides
        **kwargs,
        #
        # required params
        "stopping_criteria": stopping_criteria,
        # "assistant_model": assistant_model,
        #
        # add inputs
        **inputs,
    }

    # If not streaming, run directly and return result
    if not stream:
        [output] = model.generate(**generation_kwargs)
        result = tokenizer.decode(output[input_length:], skip_special_tokens=False)

        # Remove the stop sequence at the end (needed)
        for s in stop:
            result = result.split(s)[0].strip()
        
        return result
    
    # If streaming, prepare streamer
    streamer = TextIteratorStreamer(tokenizer, skip_prompt=True, timeout=timeout, skip_special_tokens=False)
    generation_kwargs["streamer"] = streamer

    # and start generating in new thread
    thread = Thread(target=model.generate, kwargs=generation_kwargs)
    thread.start()
    
    # stop sequence filter
    return remove_stops(streamer, tokenizer, stop)


# LLM settings
llm_settings = dict(
    max_new_tokens=120, 
    stop=["<|", "\n\n", "< |", "<end", "<section"],
    temperature=1.2,
)

async def reply(message: str):

    chatml = [
        ChatMLMessage(name="situation", role="system", content="Samantha is talking to a person."),
        ChatMLMessage(name="", role="user", content=message),
    ]

    # Generate streaming response
    response_stream = generate(
        chatml,
        stream=True,
        **llm_settings,
    )
    
    # Print tokens and collect tokens to add to agent history
    response = ""
    for token in response_stream:
        response += token
        print(token, end=" ")
    
    print()
