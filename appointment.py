# appointment.py

class Appointment:
    APPT_TYPE_DESCS = [
        "Available",
        "Mens Cut",
        "Ladies Cut",
        "Mens Colouring",
        "Ladies Colouring"
    ]

    APPT_TYPE_PRICES = [
        0,   # Available
        40,  # Mens Cut
        60,  # Ladies Cut
        40,  # Mens Colouring
        80   # Ladies Colouring
    ]

    @classmethod
    def get_appt_type_desc_and_price(cls, appt_type):
        return f"{appt_type}: {cls.APPT_TYPE_DESCS[appt_type]} ${cls.APPT_TYPE_PRICES[appt_type]}"

    def __init__(self, day_of_week, start_time_hour):
        self.client_name = ""
        self.client_phone = ""
        self.appt_type = 0

        self.day_of_week = day_of_week
        self.start_time_hour = start_time_hour

    # Getters
    def get_client_name(self):
        return self.client_name

    def get_client_phone(self):
        return self.client_phone

    def get_appt_type(self):
        return self.appt_type

    def get_day_of_week(self):
        return self.day_of_week

    def get_start_time_hour(self):
        return self.start_time_hour

    def get_appt_type_desc(self):
        return self.APPT_TYPE_DESCS[self.appt_type]

    def get_end_time_hour(self):
        return self.start_time_hour + 1

    # Setters
    def set_client_name(self, name):
        self.client_name = name

    def set_client_phone(self, phone):
        self.client_phone = phone

    def set_appt_type(self, apptype):
        self.appt_type = apptype

    def schedule(self, client_name, client_phone, apptype):
        self.client_name = client_name
        self.client_phone = client_phone
        self.appt_type = apptype

    def cancel(self):
        self.client_name = ""
        self.client_phone = ""
        self.appt_type = 0

    def format_record(self):
        return f"{self.client_name},{self.client_phone},{self.appt_type},{self.day_of_week},{self.start_time_hour:02d}"

    def __str__(self):

        name_str = self.client_name if self.client_name else "Available"
        phone_str = self.client_phone if self.client_phone else ""
        appt_desc = self.get_appt_type_desc()
        start_str = f"{self.start_time_hour:02d}:00"
        end_str = f"{self.get_end_time_hour():02d}:00"
        if self.appt_type == 0:
            return f"{self.day_of_week} {start_str}-{end_str} {appt_desc}"
        else:
            return f"{self.client_name} {self.client_phone} {self.day_of_week} {start_str}-{end_str} {appt_desc}"
