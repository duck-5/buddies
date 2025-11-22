import re
import json
import logging

logger = logging.getLogger(__name__)

JSON_REGEX = re.compile("\{.*\}", flags=re.DOTALL)

def parse_llm_response(message):
    # Find json data in response
    logger.debug("Finding json regex in llm response")
    match = re.search(JSON_REGEX, message)
    if not match:
        raise ValueError("Could not find json data in LLM response")
    json_data = match.group()

    logger.debug(f"Found match of length {len(json_data)}")

    # Parse json data
    logger.debug("Parsing json data")
    try:
        result = json.loads(json_data)
        logger.debug("Response parsed successfully!")
        return result
    except json.JSONDecodeError as e:
        raise ValueError("JSON parsing failed! invalid LLM response")
