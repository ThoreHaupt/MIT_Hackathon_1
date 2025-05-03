import datetime

class TrafficIssue:
    def __init__(self, longitude: float, latitude: float, description: str, isBlocked: bool,
                 estimatedTimeLoss: float, beginTime: datetime.datetime, endTime: datetime.datetime):
        self.longitude = longitude
        self.latitude = latitude
        self.description = description
        self.isBlocked = isBlocked
        self.estimatedTimeLoss = estimatedTimeLoss
        self.beginTime = beginTime
        self.endTime = endTime

    def __str__(self):
        return (f"TrafficIssue(longitude={self.longitude}, latitude={self.latitude}, description={self.description}, "
                f"isBlocked={self.isBlocked}, estimatedTimeLoss={self.estimatedTimeLoss}, "
                f"beginTime={self.beginTime}, endTime={self.endTime})")
    
    def to_dict(self):
        return {
            "longitude": self.longitude,
            "latitude": self.latitude,
            "description": self.description,
            "isBlocked": self.isBlocked,
            "estimatedTimeLoss": self.estimatedTimeLoss,
            "beginTime": self.beginTime.isoformat() if self.beginTime else None,
            "endTime": self.endTime.isoformat() if self.endTime else None
        }