/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Tasks_BaseWorkflowStep } from "./Tasks_BaseWorkflowStep";
export type Tasks_ErrorWorkflowStep = Tasks_BaseWorkflowStep & {
  kind_: "error";
  /**
   * The error message
   */
  error: string;
};
