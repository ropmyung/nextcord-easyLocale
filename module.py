from typing import Union
from nextcord import Locale, Embed, Interaction

class BotContent:
    """
    The type of bot contents.
    """
    def __init__(
        self,
        _data: dict[Locale, list[Union[Embed, str]]],
        _inte: Interaction = None
    ) -> None:
        self.main: dict = _data
        self.data: dict = {}
        self.order: int = 0
        self.local_list: list = list(self.main.keys())
        for i in _data.keys():
            self.data[i]: list[list[Union[Embed, str]]] = tuple(_data[i])
        if _inte is not None:
            self.local: Locale = Locale(_inte.locale) if Locale(_inte.locale) in self.local_list else Locale.en_US

    def add(self, _value: Union[Embed, str], *, _lang: Locale = Locale.en_US) -> None:
        "Add content on the data of the language. If the language is not given, English will be applied by default."
        self.main[_lang].append(_value)

    def divide(self, _index: Union[int, list[int]]) -> None:
        """
        Divides the content. It is useful when you want to load content in specific cases.

        Parameter
        -
        _index: `int` or `list`[`int`]
            The index to divide the content.
        """
        if isinstance(self.main[self.local][0], list):
            raise TypeError("The data has been divided.")
        if isinstance(_index, list):
            _index.append(0)
            _index.sort()
            _data: dict[Locale, list] = {}
            for _local in self.main.keys():
                _data[_local] = []
                for i in range(len(_index)-1):
                    _data[_local].append(self.main[_local][_index[i]:_index[i+1]])
                _data[_local].append(self.main[_local][_index[-1]:])
            self.main = _data
            self.order = [0] * len(_data[self.local])
        elif isinstance(_index, int):
            _data: dict[Locale, list] = {}
            for _local in self.main.keys():
                _data[_local] = []
                _data[_local].append(self.main[_local][:_index])
                _data[_local].append(self.main[_local][_index:])
            self.main = _data
            self.order = [0] * len(_data[self.local])
        else:
            raise TypeError("_index should be int or list")

    def set_inte(self, _inte: Interaction) -> None:
        "Set interaction of the BotContent."
        self.local = Locale.ko if _inte.locale == "ko" else Locale.en_US

    def get_all(self) -> list:
        "Return all contents of the user's language."
        return self.main[self.local]

    def get(self, _condition: int = 0) -> str:
        """
        Load the content following by order. If the data has been divided by case, you need to give condition number(index).
        
        Parameter
        -
        _condition: `int`
            The case index you want to load.
        """
        if isinstance(self.main[self.local][0], list):
            self.order[_condition] += 1
            return self.main[self.local][_condition][self.order[_condition] - 1]
        else:
            self.order += 1
            return self.main[self.local][self.order - 1]