import os
from appointment import Appointment

def create_weekly_calendar(appointments):
    appointments.clear()
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    for day in days:
        for hour in range(9, 17):
            appointments.append(Appointment(day, hour))


def load_scheduled_appointments(appointments):
    filename = input("Enter appointments filename: ").strip()
    if not os.path.exists(filename):
        print("File does not exist. No appointments loaded.")
        return 0

    count = 0
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Format: name,phone,appt_type,day,hour
            parts = line.split(",")
            if len(parts) == 5:
                name, phone, apptype, day, hour = parts
                apptype = int(apptype)
                hour = int(hour)
                appt = find_appointment_by_time(appointments, day, hour)
                if appt:
                    appt.schedule(name, phone, apptype)
                    count += 1
    print(f"{count} appointments loaded.")
    return count


def print_menu():
    print()
    print("1) Schedule an appointment")
    print("2) Find appointment by name")
    print("3) Print calendar for a specific day")
    print("4) Cancel an appointment")
    print("5) Change an appointment")
    print("6) Calculate total fees for a day")
    print("7) Calculate total weekly fees")
    print("0) Exit the system")
    print()

    valid_options = ["0", "1", "2", "3", "4", "5", "6", "7"]
    choice = input("Enter your selection: ").strip()
    while choice not in valid_options:
        choice = input("Invalid selection. Please re-enter: ").strip()
    return choice


def input_day_of_week(prompt="Enter the day of the week (Monday-Saturday): "):
    valid_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    day = input(prompt).strip()
    while day not in valid_days:
        day = input("Invalid day. Please enter a day (Monday-Saturday): ").strip()
    return day


def find_appointment_by_time(appointments, day, start_hour):
    for appt in appointments:
        if appt.get_day_of_week() == day and appt.get_start_time_hour() == start_hour:
            return appt
    return None


def show_appointments_by_name(appointments, name):
    name_lower = name.lower()
    matches = [appt for appt in appointments 
               if appt.get_client_name().lower().find(name_lower) != -1 and appt.get_client_name() != ""]
    if matches:
        for m in matches:
            print(m)  
    else:
        print("No appointments found for that name.")


def show_appointments_by_day(appointments, day):
    matches = [appt for appt in appointments if appt.get_day_of_week() == day]
    for m in matches:
        print(m)


def change_appointment_by_day_time(appointments):
    print("Original Appointment:")
    original_day = input_day_of_week("Enter original appointment day: ")
    try:
        original_hour = int(input("Enter original start hour (9-16): ").strip())
    except ValueError:
        print("Invalid hour.")
        return
    old_appt = find_appointment_by_time(appointments, original_day, original_hour)
    if not old_appt or old_appt.get_appt_type() == 0:
        print("No scheduled appointment found at that time.")
        return

    print("New Appointment:")
    new_day = input_day_of_week("Enter new day: ")
    try:
        new_hour = int(input("Enter new start hour (9-16): ").strip())
    except ValueError:
        print("Invalid hour.")
        return

    new_appt = find_appointment_by_time(appointments, new_day, new_hour)
    if not new_appt:
        print("Invalid appointment time.")
        return

    if new_appt.get_appt_type() != 0:
        print("New appointment slot is already taken.")
        return

    # Perform the change
    client_name = old_appt.get_client_name()
    client_phone = old_appt.get_client_phone()
    apptype = old_appt.get_appt_type()

    new_appt.schedule(client_name, client_phone, apptype)
    old_appt.cancel()

    print(f"Appointment for {client_name} has been moved to {new_day} {new_hour}:00.")


def calculate_fees_per_day(appointments):
    day = input_day_of_week()
    total = 0
    for appt in appointments:
        if appt.get_day_of_week() == day and appt.get_appt_type() != 0:
            t = appt.get_appt_type()
            total += Appointment.APPT_TYPE_PRICES[t]
    print(f"Total fees for {day} is: ${total}")


def calculate_weekly_fees(appointments):
    total = 0
    for appt in appointments:
        t = appt.get_appt_type()
        if t != 0:
            total += Appointment.APPT_TYPE_PRICES[t]
    print(f"Total fees for the week is: ${total}")


def save_scheduled_appointments(appointments):
    while True:
        filename = input("Enter filename to save appointments: ").strip()
        if os.path.exists(filename):
            overwrite = input("File already exists. Overwrite? (Y/N): ").strip().lower()
            if overwrite == 'y':
                break
            else:
                continue
        else:
            break
    count = 0
    with open(filename, "w") as f:
        for appt in appointments:
            if appt.get_appt_type() != 0:
                f.write(appt.format_record() + "\n")
                count += 1
    print(f"{count} appointments saved to {filename}.")
    return count


def main():
    appointments = []
    create_weekly_calendar(appointments)

    load_choice = input("Load previously booked appointments from file? (Y/N): ").strip().lower()
    if load_choice == 'y':
        load_scheduled_appointments(appointments)

    while True:
        choice = print_menu()
        if choice == '0':
            save_choice = input("Save scheduled appointments to file? (Y/N): ").strip().lower()
            if save_choice == 'y':
                save_scheduled_appointments(appointments)
            print("Exiting system...")
            break
        elif choice == '1':
            day = input_day_of_week()
            try:
                hour = int(input("Enter start hour (9-16): ").strip())
            except ValueError:
                print("Invalid hour.")
                continue

            appt = find_appointment_by_time(appointments, day, hour)
            if not appt:
                print("Invalid appointment time.")
                continue

            if appt.get_appt_type() != 0:
                print("Appointment slot already booked.")
                continue

            name = input("Enter client name: ").strip()
            phone = input("Enter client phone: ").strip()
            print("Select appointment type:")
            for i, desc in enumerate(Appointment.APPT_TYPE_DESCS):
                price = Appointment.APPT_TYPE_PRICES[i]
                print(f"{i}) {desc} ${price}")
            try:
                apptype = int(input("Enter appointment type number: ").strip())
            except ValueError:
                print("Invalid appointment type.")
                continue
            if apptype < 1 or apptype > 4:
                print("Invalid appointment type.")
                continue

            appt.schedule(name, phone, apptype)
            print("Appointment scheduled.")

        elif choice == '2':
            search_name = input("Enter name or partial name: ").strip()
            show_appointments_by_name(appointments, search_name)

        elif choice == '3':
            day = input_day_of_week()
            show_appointments_by_day(appointments, day)

        elif choice == '4':
            day = input_day_of_week()
            try:
                hour = int(input("Enter start hour (9-16): ").strip())
            except ValueError:
                print("Invalid hour.")
                continue

            appt = find_appointment_by_time(appointments, day, hour)
            if not appt:
                print("Invalid appointment time.")
                continue

            if appt.get_appt_type() == 0:
                print("No scheduled appointment at this time.")
                continue

            appt.cancel()
            print("Appointment cancelled.")

        elif choice == '5':
            change_appointment_by_day_time(appointments)

        elif choice == '6':
            calculate_fees_per_day(appointments)

        elif choice == '7':
            calculate_weekly_fees(appointments)


if __name__ == "__main__":
    main()
