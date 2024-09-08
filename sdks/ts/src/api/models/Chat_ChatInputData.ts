/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Entries_ChatMLRole } from "./Entries_ChatMLRole";
import type { Tools_NamedApiCallChoice } from "./Tools_NamedApiCallChoice";
import type { Tools_NamedFunctionChoice } from "./Tools_NamedFunctionChoice";
import type { Tools_NamedIntegrationChoice } from "./Tools_NamedIntegrationChoice";
import type { Tools_NamedSystemChoice } from "./Tools_NamedSystemChoice";
import type { Tools_Tool } from "./Tools_Tool";
export type Chat_ChatInputData = {
  /**
   * A list of new input messages comprising the conversation so far.
   */
  messages: Array<{
    /**
     * The role of the message
     */
    role: Entries_ChatMLRole;
    /**
     * The content parts of the message
     */
    content: string | Array<string>;
    /**
     * Name
     */
    name?: string;
    /**
     * Whether to continue this message or return a new one
     */
    continue?: boolean;
  }>;
  /**
   * (Advanced) List of tools that are provided in addition to agent's default set of tools.
   */
  tools: Array<Tools_Tool>;
  /**
   * Can be one of existing tools given to the agent earlier or the ones provided in this request.
   */
  tool_choice?:
    | "auto"
    | "none"
    | Tools_NamedFunctionChoice
    | Tools_NamedIntegrationChoice
    | Tools_NamedSystemChoice
    | Tools_NamedApiCallChoice;
};
