/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $Chat_MultipleChatOutput = {
  type: "all-of",
  description: `The output returned by the model. Note that, depending on the model provider, they might return more than one message.`,
  contains: [
    {
      type: "Chat_BaseChatOutput",
    },
    {
      properties: {
        messages: {
          type: "array",
          contains: {
            properties: {
              role: {
                type: "all-of",
                description: `The role of the message`,
                contains: [
                  {
                    type: "Entries_ChatMLRole",
                  },
                ],
                isRequired: true,
              },
              content: {
                type: "any-of",
                description: `The content parts of the message`,
                contains: [
                  {
                    type: "string",
                  },
                  {
                    type: "array",
                    contains: {
                      type: "string",
                    },
                  },
                ],
                isRequired: true,
              },
              name: {
                type: "string",
                description: `Name`,
              },
              tool_calls: {
                type: "array",
                contains: {
                  type: "any-of",
                  contains: [
                    {
                      type: "Tools_ChosenFunctionCall",
                    },
                    {
                      type: "Tools_ChosenIntegrationCall",
                    },
                    {
                      type: "Tools_ChosenSystemCall",
                    },
                    {
                      type: "Tools_ChosenApiCall",
                    },
                  ],
                },
                isReadOnly: true,
                isNullable: true,
              },
              created_at: {
                type: "string",
                description: `When this resource was created as UTC date-time`,
                isReadOnly: true,
                format: "date-time",
              },
              id: {
                type: "all-of",
                contains: [
                  {
                    type: "Common_uuid",
                  },
                ],
                isReadOnly: true,
              },
            },
          },
          isReadOnly: true,
          isRequired: true,
        },
      },
    },
  ],
} as const;
