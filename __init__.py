"""Electric Ireland to Home Assistant Integration"""

from .dayModel import DayModel
from .fileReader import FileReader
from .staticstics import Statistics

DOMAIN = "ei2ha"
ATTR_NAME = "Electric Ireland to Home Assistant"
DEFAULT_NAME = "Electric Ireland to Home Assistant"

def setup(hass, config):
    """Set up is called when Home Assistant is loading our component."""

    fileReader = FileReader()
    statistics = Statistics()

    def update(call):
        """Update."""
        content = fileReader.readFile().splitlines()
        days = []
        for line in content[1:]:
            dayModel = DayModel.parse(line)
            days.append(dayModel)

        statistics.cleanOldStatistics()
        statistics.importStatistics(days)

    hass.services.register(DOMAIN, "update", update)

    return True