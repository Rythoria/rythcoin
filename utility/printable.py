"""Converts any Object into a readable string format for JSON"""
class Printable:
    def __repr__(self):
        return str(self.__dict__)