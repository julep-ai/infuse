from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper


async def dalle_image_generator(parameters: dict) -> str:
    # FIXME: Fix OpenAI API Key error

    dalle = DallEAPIWrapper()
    prompt = parameters.get("prompt")
    if not prompt:
        raise ValueError("Prompt parameter is required for DALL-E image generation")
    return dalle.run(prompt)
