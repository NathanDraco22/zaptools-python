from typing import Any


class MetaTag:

    def __init__(
        self,
        name: str,
        description: str = "",
        values: dict[str, Any] = {},
    ) -> None:
        self.name = name
        self.description = description
        self.values = values
