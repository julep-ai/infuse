/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type ChatSettings = {
  /**
   * (OpenAI-like) Number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim.
   */
  frequency_penalty?: number | null;
  /**
   * (Huggingface-like) Number between 0 and 2.0. 1.0 is neutral and values larger than that penalize number of tokens generated.
   */
  length_penalty?: number | null;
  /**
   * Modify the likelihood of specified tokens appearing in the completion.
   *
   * Accepts a JSON object that maps tokens (specified by their token ID in the tokenizer) to an associated bias value from -100 to 100. Mathematically, the bias is added to the logits generated by the model prior to sampling. The exact effect will vary per model, but values between -1 and 1 should decrease or increase likelihood of selection; values like -100 or 100 should result in a ban or exclusive selection of the relevant token.
   *
   */
  logit_bias?: Record<string, number> | null;
  /**
   * The maximum number of tokens to generate in the chat completion.
   *
   * The total length of input tokens and generated tokens is limited by the model's context length.
   *
   */
  max_tokens?: number | null;
  /**
   * (OpenAI-like) Number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim.
   */
  presence_penalty?: number | null;
  /**
   * (Huggingface-like) Number between 0 and 2.0. 1.0 is neutral and values larger than that penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim.
   */
  repetition_penalty?: number | null;
  /**
   * An object specifying the format that the model must output.
   *
   * Setting to `{ "type": "json_object" }` enables JSON mode, which guarantees the message the model generates is valid JSON.
   *
   * **Important:** when using JSON mode, you **must** also instruct the model to produce JSON yourself via a system or user message. Without this, the model may generate an unending stream of whitespace until the generation reaches the token limit, resulting in a long-running and seemingly "stuck" request. Also note that the message content may be partially cut off if `finish_reason="length"`, which indicates the generation exceeded `max_tokens` or the conversation exceeded the max context length.
   *
   */
  response_format?: {
    /**
     * Must be one of `"text"`, `"regex"` or `"json_object"`.
     */
    type?: "text" | "json_object" | "regex";
    /**
     * Regular expression pattern to use if `type` is `"regex"`
     */
    pattern?: string;
    /**
     * JSON Schema to use if `type` is `"json_object"`
     */
    schema?: any;
  };
  /**
   * This feature is in Beta.
   * If specified, our system will make a best effort to sample deterministically, such that repeated requests with the same `seed` and parameters should return the same result.
   * Determinism is not guaranteed, and you should refer to the `system_fingerprint` response parameter to monitor changes in the backend.
   *
   */
  seed?: number | null;
  /**
   * Up to 4 sequences where the API will stop generating further tokens.
   *
   */
  stop?: string | null | Array<string>;
  /**
   * If set, partial message deltas will be sent, like in ChatGPT. Tokens will be sent as data-only [server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events#Event_stream_format) as they become available, with the stream terminated by a `data: [DONE]` message. [Example Python code](https://cookbook.openai.com/examples/how_to_stream_completions).
   *
   */
  stream?: boolean | null;
  /**
   * What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.
   */
  temperature?: number | null;
  /**
   * Defaults to 1 An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.  We generally recommend altering this or temperature but not both.
   */
  top_p?: number | null;
  /**
   * Minimum probability compared to leading token to be considered
   */
  min_p?: number;
  /**
   * Generation preset name (problem_solving|conversational|fun|prose|creative|business|deterministic|code|multilingual)
   */
  preset?:
    | "problem_solving"
    | "conversational"
    | "fun"
    | "prose"
    | "creative"
    | "business"
    | "deterministic"
    | "code"
    | "multilingual";
  /**
   * Model name
   */
  model?: string;
};
