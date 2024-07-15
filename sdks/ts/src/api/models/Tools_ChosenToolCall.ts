/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Common_uuid } from "./Common_uuid";
import type { Tools_FunctionCallOption } from "./Tools_FunctionCallOption";
import type { Tools_ToolType } from "./Tools_ToolType";
/**
 * The response tool value generated by the model
 */
export type Tools_ChosenToolCall = {
  /**
   * Whether this tool is a `function`, `api_call`, `system` etc. (Only `function` tool supported right now)
   */
  type: Tools_ToolType;
  function?: Tools_FunctionCallOption;
  integration?: any;
  system?: any;
  api_call?: any;
  readonly id: Common_uuid;
};
