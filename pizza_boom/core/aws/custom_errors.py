class AwsError(Exception):
    pass


class TaskTimedOut(AwsError):
    pass
