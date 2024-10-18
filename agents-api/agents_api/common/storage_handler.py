import inspect
import sys
from datetime import timedelta
from functools import wraps
from typing import Any, Callable

from temporalio import workflow

from ..activities.sync_items_remote import load_inputs_remote
from ..clients import s3
from ..common.protocol.remote import BaseRemoteModel, RemoteList, RemoteObject
from ..common.retry_policies import DEFAULT_RETRY_POLICY
from ..env import blob_store_cutoff_kb, debug, testing, use_blob_store_for_temporal
from ..worker.codec import deserialize, serialize


def store_in_blob_store_if_large(x: Any) -> RemoteObject | Any:
    s3.setup()

    serialized = serialize(x)
    data_size = sys.getsizeof(serialized)

    if data_size > blob_store_cutoff_kb * 1024:
        key = s3.add_object_with_hash(serialized)
        return RemoteObject(key=key)

    return x


def load_from_blob_store_if_remote(x: Any | RemoteObject) -> Any:
    s3.setup()

    if isinstance(x, RemoteObject):
        fetched = s3.get_object(x.key)
        return deserialize(fetched)

    return x


# Decorator that automatically does two things:
# 1. store in blob store if the output of a function is large
# 2. load from blob store if the input is a RemoteObject


def auto_blob_store(f: Callable) -> Callable:
    def load_args(
        args: list[Any], kwargs: dict[str, Any]
    ) -> tuple[list[Any], dict[str, Any]]:
        new_args = [load_from_blob_store_if_remote(arg) for arg in args]
        new_kwargs = {k: load_from_blob_store_if_remote(v) for k, v in kwargs.items()}

        return new_args, new_kwargs

    def unload_return_value(x: Any | BaseRemoteModel | RemoteList) -> Any:
        if isinstance(x, (BaseRemoteModel, RemoteList)):
            x.unload_all()

        return store_in_blob_store_if_large(x)

    if inspect.iscoroutinefunction(f):

        @wraps(f)
        async def async_wrapper(*args, **kwargs) -> Any:
            new_args, new_kwargs = load_args(args, kwargs)
            output = await f(*new_args, **new_kwargs)

            return unload_return_value(output)

        return async_wrapper if use_blob_store_for_temporal else f

    else:

        @wraps(f)
        def wrapper(*args, **kwargs) -> Any:
            new_args, new_kwargs = load_args(args, kwargs)
            output = f(*new_args, **new_kwargs)

            return unload_return_value(output)

        return wrapper if use_blob_store_for_temporal else f


def auto_blob_store_workflow(f: Callable) -> Callable:
    @wraps(f)
    async def wrapper(*args, **kwargs) -> Any:
        keys = kwargs.keys()
        values = [kwargs[k] for k in keys]

        loaded = await workflow.execute_local_activity(
            load_inputs_remote,
            args=[[*args, *values]],
            schedule_to_close_timeout=timedelta(seconds=10 if debug or testing else 60),
            retry_policy=DEFAULT_RETRY_POLICY,
        )

        loaded_args = loaded[: len(args)]
        loaded_kwargs = dict(zip(keys, loaded[len(args) :]))

        result = await f(*loaded_args, **loaded_kwargs)

        return result

    return wrapper
