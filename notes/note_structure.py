class Note:
    # Constructor:
    def __init__(self, username: str, title: str, description: str) -> None:
        # Instance Attributes:
        self.__title: str = title
        self.__description: str = description
        self.__username: str = username

    # Properties:
    @property
    def title(self) -> str: return self.__title

    @property
    def description(self) -> str: return self.__description

    @property
    def username(self) -> str: return self.__username
