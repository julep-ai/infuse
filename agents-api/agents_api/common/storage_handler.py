import asyncio
import sys
from datetime import timedelta
from functools import wraps
from typing import Any, Callable

from pydantic import BaseModel
from temporalio import workflow

from ..activities.sync_items_remote import load_inputs_remote
from ..clients import async_s3
from ..common.protocol.remote import BaseRemoteModel, RemoteObject
from ..common.retry_policies import DEFAULT_RETRY_POLICY
from ..env import (
    blob_store_cutoff_kb,
    debug,
    temporal_heartbeat_timeout,
    temporal_schedule_to_close_timeout,
    testing,
    use_blob_store_for_temporal,
)
from ..worker.codec import deserialize, serialize


async def store_in_blob_store_if_large(x: Any) -> RemoteObject | Any:
    if not use_blob_store_for_temporal:
        return x

    await async_s3.setup()

    serialized = serialize(x)
    data_size = sys.getsizeof(serialized)

    if data_size > blob_store_cutoff_kb * 1024:
        key = await async_s3.add_object_with_hash(serialized)
        return RemoteObject(key=key)

    return x


async def load_from_blob_store_if_remote(x: Any | RemoteObject) -> Any:
    if not use_blob_store_for_temporal:
        return x

    await async_s3.setup()

    if isinstance(x, RemoteObject):
        fetched = await async_s3.get_object(x.key)
        return deserialize(fetched)

    elif isinstance(x, dict) and set(x.keys()) == {"bucket", "key"}:
        fetched = await async_s3.get_object(x["key"])
        return deserialize(fetched)

    return x


# Decorator that automatically does two things:
# 1. store in blob store if the output of a function is large
# 2. load from blob store if the input is a RemoteObject


def auto_blob_store(f: Callable | None = None, *, deep: bool = False) -> Callable:
    def auto_blob_store_decorator(f: Callable) -> Callable:
        async def load_args(
            args: list | tuple, kwargs: dict[str, Any]
        ) -> tuple[list | tuple, dict[str, Any]]:
            new_args = await asyncio.gather(
                *[load_from_blob_store_if_remote(arg) for arg in args]
            )
            kwargs_keys, kwargs_values = list(zip(*kwargs.items())) or ([], [])
            new_kwargs = await asyncio.gather(
                *[load_from_blob_store_if_remote(v) for v in kwargs_values]
            )
            new_kwargs = dict(zip(kwargs_keys, new_kwargs))

            if deep:
                args = new_args
                kwargs = new_kwargs

                new_args = []

                for arg in args:
                    if isinstance(arg, list):
                        new_args.append(
                            await asyncio.gather(
                                *[load_from_blob_store_if_remote(item) for item in arg]
                            )
                        )
                    elif isinstance(arg, dict):
                        keys, values = list(zip(*arg.items())) or ([], [])
                        values = await asyncio.gather(
                            *[load_from_blob_store_if_remote(value) for value in values]
                        )
                        new_args.append(dict(zip(keys, values)))

                    elif isinstance(arg, BaseRemoteModel):
                        new_args.append(await arg.unload_all())

                    elif isinstance(arg, BaseModel):
                        for field in arg.model_fields.keys():
                            if isinstance(getattr(arg, field), RemoteObject):
                                setattr(
                                    arg,
                                    field,
                                    await load_from_blob_store_if_remote(
                                        getattr(arg, field)
                                    ),
                                )
                            elif isinstance(getattr(arg, field), list):
                                setattr(
                                    arg,
                                    field,
                                    await asyncio.gather(
                                        *[
                                            load_from_blob_store_if_remote(item)
                                            for item in getattr(arg, field)
                                        ]
                                    ),
                                )
                            elif isinstance(getattr(arg, field), BaseRemoteModel):
                                setattr(
                                    arg,
                                    field,
                                    await getattr(arg, field).unload_all(),
                                )

                        new_args.append(arg)

                    else:
                        new_args.append(arg)

                new_kwargs = {}

                for k, v in kwargs.items():
                    if isinstance(v, list):
                        new_kwargs[k] = await asyncio.gather(
                            *[load_from_blob_store_if_remote(item) for item in v]
                        )

                    elif isinstance(v, dict):
                        keys, values = list(zip(*v.items())) or ([], [])
                        values = await asyncio.gather(
                            *[load_from_blob_store_if_remote(value) for value in values]
                        )
                        new_kwargs[k] = dict(zip(keys, values))

                    elif isinstance(v, BaseRemoteModel):
                        new_kwargs[k] = await v.unload_all()

                    elif isinstance(v, BaseModel):
                        for field in v.model_fields.keys():
                            if isinstance(getattr(v, field), RemoteObject):
                                setattr(
                                    v,
                                    field,
                                    await load_from_blob_store_if_remote(
                                        getattr(v, field)
                                    ),
                                )
                            elif isinstance(getattr(v, field), list):
                                setattr(
                                    v,
                                    field,
                                    await asyncio.gather(
                                        *[
                                            load_from_blob_store_if_remote(item)
                                            for item in getattr(v, field)
                                        ]
                                    ),
                                )
                            elif isinstance(getattr(v, field), BaseRemoteModel):
                                setattr(
                                    v,
                                    field,
                                    await getattr(v, field).unload_all(),
                                )
                        new_kwargs[k] = v

                    else:
                        new_kwargs[k] = v

            return new_args, new_kwargs

        async def unload_return_value(x: Any | BaseRemoteModel) -> Any:
            if isinstance(x, BaseRemoteModel):
                await x.unload_all()

            return await store_in_blob_store_if_large(x)

        @wraps(f)
        async def async_wrapper(*args, **kwargs) -> Any:
            new_args, new_kwargs = await load_args(args, kwargs)
            output = await f(*new_args, **new_kwargs)

            return await unload_return_value(output)

        return async_wrapper if use_blob_store_for_temporal else f

    return auto_blob_store_decorator(f) if f else auto_blob_store_decorator


def auto_blob_store_workflow(f: Callable) -> Callable:
    @wraps(f)
    async def wrapper(*args, **kwargs) -> Any:
        keys = kwargs.keys()
        values = [kwargs[k] for k in keys]

        loaded = await workflow.execute_activity(
            load_inputs_remote,
            args=[[*args, *values]],
            schedule_to_close_timeout=timedelta(
                seconds=60 if debug or testing else temporal_schedule_to_close_timeout
            ),
            retry_policy=DEFAULT_RETRY_POLICY,
            heartbeat_timeout=timedelta(seconds=temporal_heartbeat_timeout),
        )

        loaded_args = loaded[: len(args)]
        loaded_kwargs = dict(zip(keys, loaded[len(args) :]))

        result = await f(*loaded_args, **loaded_kwargs)

        return result

    return wrapper if use_blob_store_for_temporal else f
