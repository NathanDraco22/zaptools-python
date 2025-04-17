import uuid


class IDController:
    _ID_HEADING = "zpt"

    def eval(self, id: str | None = None) -> str:
        if id:
            return id
        return str(f"{self._ID_HEADING}-{uuid.uuid4()}")
