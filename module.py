from nextcord import *

class BotContent:
    """
    The type of bot contents.
    """
    def __init__(
        self,
        data: dict[Locale, Union[list[Union[Box, str]], str, Box]] = {Locale.en_US: '', Locale.ko: ''},
        local: Union[Interaction, Locale] = Locale.en_US
    ) -> None:
        self._data = {local: datum if isinstance(datum, list) else [datum] for local, datum in data.items()}
        self._condition = 0
        self._iter = self.contents
        self.local_list: list = list(self._data.keys())
        self.local = Locale(local.locale) if isinstance(local, Interaction) else Locale(local)
        if self.local not in self.local_list:
            self.local = Locale.en_US

    def __len__(self) -> int: return len(self._data[self.local])

    def __add__(self, __data: dict[Locale, Union[Box, str]]):
        self._data = {k: self._data[k] + v if isinstance(v, list) else self._data[k] + [v] for k, v in __data.items()}
        return self
    
    def __truediv__(self, __index: int):
        self.divide(__index)
        return self

    def __getitem__(self, __index: Union[Locale, int]):
        if isinstance(__index, int): return self._data[self.local][__index]
        return self._data[__index]

    def divide(self, *index: int) -> None:
        """
        Divides the content. It is useful when you want to load content in specific cases.

        Parameter
        -
        _index: `int` or `list`[`int`]
            The index to divide the content.
        """
        if isinstance(self._data[self.local][0], list): raise ValueError("The data has been divided.")
        if not isinstance(index[0], int): raise TypeError("index should be int type.")
        index = sorted(index)
        self._data: dict[Locale, list[list[Union[str, Box]]]] = {local: [
            content[:index[0]],
            *[content[index[i]:index[i+1]] for i in range(len(index) - 1)],
            content[index[-1]:]] for local, content in self._data.items()
        }
        self._iter = self.contents

    def get_all(self) -> list[Union[str, Box]]:
        "Return all contents of the user's language."
        return self._data[self.local]

    @property
    def contents(self):
        if isinstance(self._data[self.local][0], list):
            for i in self._data[self.local][self._condition]: yield i
        else:
            for i in self._data[self.local]: yield i

    @contents.setter
    def contents(self, __index: int) -> None:
        self._condition = __index
        self._iter = self.contents

    def get(self, condition: Optional[int] = None) -> Union[str, Box]:
        """
        Load the content following by order. If the data has been divided by case, you need to give condition number(index).
        """
        if condition is not None:
            self.contents = condition
            self._iter = self.contents
        return next(self._iter)
