from uuid import UUID, uuid4

import pandas as pd

from ...autogen.openapi_model import FunctionDef
from ...clients.cozo import client
from ...common.utils import json


def create_tools_query(
    agent_id: UUID,
    functions: list[FunctionDef],
    embeddings: list[list[float]],
) -> pd.DataFrame:
    assert len(functions) == len(embeddings)

    functions_input = []

    for function, embedding in zip(functions, embeddings):
        function_name = json.dumps(function.name)
        function_description = json.dumps(function.description)
        tool_id = uuid4()
        parameters = function.parameters.model_dump_json()
        functions_input.append(
            f"""[to_uuid("{agent_id}"), to_uuid("{tool_id}"), {function_name}, {function_description}, {parameters}, vec({embedding}), now()]"""
        )

    records = "\n".join(functions_input)

    query = f"""
        ?[agent_id, tool_id, name, description, parameters, embedding, updated_at] <- [
            {records}
        ]

        :insert agent_functions {{
            agent_id,
            tool_id,
            name,
            description,
            parameters,
            embedding,
            updated_at,
        }}
        :returning
    """

    return client.run(query)
