"""dayModel module."""
from datetime import datetime

from .hourModel import HourModel

class DayModel:

    @staticmethod
    def parse(line):        
        data = line.split(",")
        result = DayModel()
        result.date = datetime.strptime(data[0], "%d/%m/%Y")
        result.hours = HourModel.parse(data[1:])
        return result


