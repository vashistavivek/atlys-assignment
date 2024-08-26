class DictToObject:
    def __init__(self, in_dict: dict):
        assert isinstance(in_dict, dict)
        for key, val in in_dict.items():
            if isinstance(val, (list, tuple)):
                setattr(
                    self,
                    key,
                    [DictToObject(x) if isinstance(x, dict) else x for x in val],
                )
            else:
                setattr(self, key, DictToObject(val) if isinstance(val, dict) else val)