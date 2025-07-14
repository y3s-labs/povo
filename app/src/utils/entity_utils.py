def extract_entity_map(entities: list[dict]) -> dict:
    """
    Extracts a map of entity names to their values from a list of entities.

    Args:
        entities (list[dict]): A list of entity dictionaries, each containing 'entity_name' and 'value'.

    Returns:
        dict: A dictionary mapping entity names to their corresponding values.
    """
    entity_map = {}
    for item in entities:
        key = item.get("entity_type")
        value = item.get("value")
        if key and value:
            if key in entity_map:
                entity_map[key] += f", {value}"
            else:
                entity_map[key] = value
    return entity_map
