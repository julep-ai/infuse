/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Chat_BaseChatResponse } from "./Chat_BaseChatResponse";
import type { Chat_ChatOutputChunk } from "./Chat_ChatOutputChunk";
export type Chat_ChunkChatResponse = Chat_BaseChatResponse & {
  /**
   * The deltas generated by the model
   */
  choices: Array<Chat_ChatOutputChunk>;
};
