from venv import logger

from ai_content.service.utils import validate_title, generate_ai_content


def _build_generate_prompt(title: str, tone: str = None) -> str:
    prompt = f"Write a short blog post about {title}"

    if tone:
        prompt += f"Write it in a \n{tone}"

    prompt += f"keep the total output under 500 characters"
    return prompt


def _generate_post(title: str, tone: str = None) -> dict:
    cleand_title = validate_title(title, min_length=5)

    prompt = _build_generate_prompt(cleand_title, tone)
    try:
        cleand_content = _generate_ai_content(prompt)
    except Exception:
        logger.error(f"Failed to generate {cleand_title}")
        raise

    if len(cleand_content) > 500:
        cleand_content = cleand_content[:500]
    return {
        "title": cleand_title,
        "content": cleand_content,
        "length": len(cleand_content)
    }
