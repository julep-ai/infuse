[@julep/sdk](../README.md) / [Modules](../modules.md) / utils/invariant

# Module: utils/invariant

## Table of contents

### Functions

- [invariant](utils_invariant.md#invariant)

## Functions

### invariant

▸ **invariant**(`condition`, `message?`): `void`

Ensures that a condition is met, throwing a custom error message if not.

#### Parameters

| Name | Type | Default value | Description |
| :------ | :------ | :------ | :------ |
| `condition` | `any` | `undefined` | The condition to test. If falsy, an error is thrown. |
| `message` | `string` | `"Invariant Violation"` | Optional. The error message to throw if the condition is not met. Defaults to "Invariant Violation". |

#### Returns

`void`

#### Defined in

[src/utils/invariant.ts:6](https://github.com/julep-ai/julep/blob/a1394c98327f6a0f4b31baa392d88efb1c6d0233/sdks/ts/src/utils/invariant.ts#L6)
