from dataclasses import dataclass
from typing import Generic, Self, TypeVar, cast

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from ...clients import async_s3
    from ...env import blob_store_bucket
    from ...worker.codec import deserialize, serialize


T = TypeVar("T")


@dataclass
class RemoteObject(Generic[T]):
    _type: type[T]
    key: str
    bucket: str

    @classmethod
    async def from_value(cls, x: T) -> Self:
        await async_s3.setup()

        serialized = serialize(x)

        key = await async_s3.add_object_with_hash(serialized)
        return RemoteObject[T](key=key, bucket=blob_store_bucket, _type=type(x))

    async def load(self) -> T:
        await async_s3.setup()

        fetched = await async_s3.get_object(self.key)
        return cast(self._type, deserialize(fetched))
