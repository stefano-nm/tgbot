class JSONObj(dict):
    def filter(self, *attrs: str):
        return self.__class__({
            attr: getattr(self, attr)
            for attr in attrs
        })

    def __setattr__(self, key: str, value):
        if key.endswith("_"):
            key = key[:-1]
        self[key] = value

    def __getattr__(self, item: str):
        typ = self.__annotations__[item]
        if item.endswith("_"):
            item = item[:-1]
        if item in self:
            return typ(self[item])
        else:
            return None
