/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Common_uuid } from "./Common_uuid";
import type { Sessions_Session } from "./Sessions_Session";
export type Sessions_SingleAgentMultiUserSession = Sessions_Session & {
  agent: Common_uuid;
  users: Array<Common_uuid>;
};
