/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Tools_FunctionDefUpdate } from "./Tools_FunctionDefUpdate";
import type { Tools_ToolType } from "./Tools_ToolType";
/**
 * Payload for patching a tool
 */
export type Tools_PatchToolRequest = {
  /**
   * Whether this tool is a `function`, `api_call`, `system` etc. (Only `function` tool supported right now)
   */
  type?: Tools_ToolType;
  /**
   * The tool should be run in the background (not supported at the moment)
   */
  background?: boolean;
  /**
   * Whether the tool that can be run interactively (response should contain "stop" boolean field)
   */
  interactive?: boolean;
  function?: Tools_FunctionDefUpdate;
  integration?: any;
  system?: any;
  api_call?: any;
};
