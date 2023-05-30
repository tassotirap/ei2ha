import mysql.connector as database
from datetime import datetime
from .config import config

class Statistics:

    def getConnection(self):
        return database.connect(
        user = config["HA"]["user"],
        password = config["HA"]["password"],
        host = config["HA"]["host"],
        port = config["HA"]["port"],
        database = config["HA"]["database"])


    def getStasticId(self):
        result = 0
        cnn = self.getConnection()
        cur = cnn.cursor()
        cur.execute("SELECT id FROM statistics_meta WHERE statistic_id = 'sensor.electric_ireland';")
        for (id,) in cur:
            result = id
        cnn.close()
        return result
        

    def cleanOldStatistics(self):
        id = self.getStasticId()
        cnn = self.getConnection()
        cur = cnn.cursor()
        cur.execute("DELETE FROM statistics where metadata_id = %s", (id,))
        cnn.commit()
        cnn.close()

    def importStatistics(self, data):
        id = self.getStasticId()
        cnn = self.getConnection()
        cur = cnn.cursor()
        sum = 0.0
        lastUnixTimestamp = 0.0
        for day in data:
            cmds = []
            for hour in day.hours:
                sum += hour.value
                time = "{day} {hour}:00:00.000000".format(day = day.date.strftime("%Y-%m-%d"), hour=str(hour.hour).zfill(2))
                unixTimestamp = datetime(day.date.year, day.date.month, day.date.day, hour.hour).timestamp()

                if(lastUnixTimestamp == unixTimestamp):                
                    unixTimestamp += 1
                
                lastUnixTimestamp = unixTimestamp
                cmds.append(" (CURRENT_TIMESTAMP,'{time}',{hour},{hour},{hour},'{time}',{hour},{sum},{id},{unixTimestamp},{unixTimestamp})".format(time=time, hour = hour.value, sum=sum, id=id, unixTimestamp=unixTimestamp))

            sql = "INSERT INTO statistics (created,start,mean,min,max,last_reset,state,sum,metadata_id,start_ts,last_reset_ts) VALUES {value}".format(value = ",".join(cmds))
            cur.execute(sql)

        cnn.commit()
        cnn.close()

