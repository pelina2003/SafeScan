from typing import List

class Report:
    def __init__(self,activity_id:str,name:str,description:str):
        self._activity_id = activity_id
        self._name = name
        self._description = description