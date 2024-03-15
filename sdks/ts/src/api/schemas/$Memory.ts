/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $Memory = {
  properties: {
    type: {
      type: "Enum",
      isRequired: true,
    },
    agent_id: {
      type: "string",
      description: `ID of the agent`,
      isRequired: true,
      format: "uuid",
    },
    user_id: {
      type: "string",
      description: `ID of the user`,
      isRequired: true,
      format: "uuid",
    },
    content: {
      type: "string",
      description: `Content of the memory`,
      isRequired: true,
    },
    weight: {
      type: "number",
      description: `Weight (importance) of the memory on a scale of 0-100`,
      maximum: 100,
    },
    created_at: {
      type: "string",
      description: `Memory created at (RFC-3339 format)`,
      isRequired: true,
      format: "date-time",
    },
    last_accessed_at: {
      type: "string",
      description: `Memory last accessed at (RFC-3339 format)`,
      format: "date-time",
    },
    timestamp: {
      type: "string",
      description: `Memory happened at (RFC-3339 format)`,
      format: "date-time",
    },
    sentiment: {
      type: "number",
      description: `Sentiment (valence) of the memory on a scale of -1 to 1`,
      maximum: 1,
      minimum: -1,
    },
    duration: {
      type: "number",
      description: `Duration of the Memory (in seconds)`,
    },
    id: {
      type: "string",
      description: `Memory id (UUID)`,
      isRequired: true,
      format: "uuid",
    },
    emotions: {
      type: "array",
      contains: {
        type: "Enum",
      },
    },
  },
} as const;
