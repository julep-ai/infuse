/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $Docs_HybridDocSearchRequest = {
  properties: {
    limit: {
      type: "number",
      isRequired: true,
      format: "uint16",
      maximum: 100,
      minimum: 1,
    },
    lang: {
      type: "Enum",
      isRequired: true,
    },
    confidence: {
      type: "number",
      description: `The confidence cutoff level`,
      isRequired: true,
      maximum: 1,
    },
    alpha: {
      type: "number",
      description: `The weight to apply to BM25 vs Vector search results. 0 => pure BM25; 1 => pure vector;`,
      isRequired: true,
      maximum: 1,
    },
    text: {
      type: "string",
      description: `Text to use in the search. In \`hybrid\` search mode, either \`text\` or both \`text\` and \`vector\` fields are required.`,
      isRequired: true,
    },
    vector: {
      type: "array",
      contains: {
        type: "number",
      },
      isRequired: true,
    },
  },
} as const;
