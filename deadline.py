class Deadline:

    def __init__(self, type, subject, name, estimate_time,
                 dead_time, status):

        self.type = type
        self.subject = subject
        self.name = name
        self.estimate_time = estimate_time
        self.dead_time = dead_time
        self.status = status
