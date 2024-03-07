/**
 * This file was auto-generated by Fern from our API Definition.
 */
/**
 * @example
 *     {
 *         userId: "user_id",
 *         agentId: "agent_id"
 *     }
 */
export interface CreateSessionRequest {
  /** User ID of user to associate with this session */
  userId: string;
  /** Agent ID of agent to associate with this session */
  agentId: string;
  /** A specific situation that sets the background for this session */
  situation?: string;
}
