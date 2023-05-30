class HourModel:
    @staticmethod
    def parse(data):
        result = []
        lastHour = 0
        lastValue = 0.0
        for idx, value in enumerate(data[2:]):
            if (value != ""):
                lastValue += float(value)

            if (idx % 2 == 1):
                model = HourModel()
                model.value = lastValue
                model.hour = lastHour
                result.append(model)
                lastValue = 0.0
                lastHour += 1
        return result