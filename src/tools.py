TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "browser_goto",
            "description": "Navigate browser to a URL",
            "parameters": {
                "type": "object",
                "properties": {"url": {"type": "string"}},
                "required": ["url"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "browser_snapshot",
            "description": "Get current page url/title and a list of clickable candidates",
            "parameters": {
                "type": "object",
                "properties": {
                    "max_candidates": {"type": "integer", "minimum": 1, "maximum": 200}
                },
                "required": ["max_candidates"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "browser_click",
            "description": "Click a candidate element by candidate_id returned from browser_snapshot",
            "parameters": {
                "type": "object",
                "properties": {"candidate_id": {"type": "string"}},
                "required": ["candidate_id"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "browser_press",
            "description": "Press a keyboard key, e.g. Enter, Escape, ArrowDown, Control+K",
            "parameters": {
                "type": "object",
                "properties": {"key": {"type": "string"}},
                "required": ["key"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "browser_type",
            "description": "Type text into a CSS selector. Can clear before typing.",
            "parameters": {
                "type": "object",
                "properties": {
                    "selector": {"type": "string"},
                    "text": {"type": "string"},
                    "clear": {"type": "boolean"},
                },
                "required": ["selector", "text"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "browser_wait",
            "description": "Wait for N milliseconds",
            "parameters": {
                "type": "object",
                "properties": {"ms": {"type": "integer", "minimum": 0, "maximum": 600000}},
                "required": ["ms"],
                "additionalProperties": False,
            },
        },
    },
]
