import json


class Book:
    def __init__(self, dewey, author, title, isbn):
        self.__dewey__ = dewey
        self.__author__ = author
        self.__title__ = title
        self.__isbn__ = isbn

    @staticmethod
    def buildFromCLZDatum(d):
        return Book(
            d['Dewey'],
            d['Author'],
            d['Title'],
            d['ISBN'],
        )

    def toDict(self):
        return dict(
            dewey=self.__dewey__,
            author=self.__author__,
            title=self.__dewey__,
            isbn=self.__title__,
        )

    def __str__(self):
        return json.dumps(self.toDict())
