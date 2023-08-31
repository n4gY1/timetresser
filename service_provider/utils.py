from service_provider.models import ServiceProvider


class FreeBookingTimes:

    def __init__(self, day):
        self.day = day
        self.opening = ""
        self.closing = ""
        self.free_times = []

    def set_opening_hours(self, opening, closing):
        self.opening = opening
        self.closing = closing

    def add_free_time(self, free_time):
        self.free_times.append(free_time)
