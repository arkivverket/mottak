from uuid import UUID

class SASTokenRequest:
    def __init__(self, container: UUID, duration: int):
        self.container = container
        self.duration = duration

    def as_data(self) -> dict:
        """
        Creates a dict adhering to SAS generator expected data structure
        :return: a dict following SAS generator expected data structure
        """
        return {'container': self.container, 'duration': self.duration}
