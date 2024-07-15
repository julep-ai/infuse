/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Common_uuid } from "./Common_uuid";
/**
 * Payload for creating a session
 */
export type Sessions_CreateSessionRequest = {
  /**
   * User ID of user associated with this session
   */
  user?: Common_uuid;
  users?: Array<Common_uuid>;
  /**
   * Agent ID of agent associated with this session
   */
  agent?: Common_uuid;
  agents?: Array<Common_uuid>;
  /**
   * A specific situation that sets the background for this session
   */
  situation: string;
  /**
   * Render system and assistant message content as jinja templates
   */
  render_templates: boolean;
  /**
   * Threshold value for the adaptive context functionality
   */
  token_budget: number | null;
  /**
   * Action to start on context window overflow
   */
  context_overflow: string | null;
  metadata?: Record<string, any>;
};
