from datetime import datetime


def get_current_time() -> str:
    """
    Retrieves the current time in 24-hour format.

    Returns:
        str: The current time as a string in the format "HH:MM" (e.g., "14:30").
    """
    now = datetime.now()
    return now.strftime("%H:%M")

def get_day_of_week(date_str: str, date_format:str="%Y-%m-%d") -> str:
    """
    Get the day of the week for a given date.

    Args:
        date_str (str): The date as a string (e.g., '2024-12-16').
        date_format (str): The format of the input date string.

    Returns:
        str: The day of the week (e.g., 'Monday').
    """
    date_obj = datetime.strptime(date_str, date_format)  # Convert string to datetime object
    return date_obj.strftime("%A")

def get_current_date() -> datetime:
    """
     Retrieves the current date and time as a `datetime` object.

    Returns:
        datetime: The current date and time.
    """
    return datetime.now()


def month_number_to_name(month_number:int) -> str:
    """
     Converts a numeric month (1-12) to its corresponding month name.

    Args:
        month_number (int): The numeric representation of a month (1 for January, 2 for February, etc.).

    Returns:
        str: The name of the month if the input is valid, or "Invalid month number" if the input is out of range.

    """
    months = [
        "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November",
        "December"
    ]
    if 1 <= month_number <= 12:
        return months[month_number - 1]
    else:
        return "Invalid month number"

def day_number_to_name(day_number:int) -> str:
    """
        Converts a day number (e.g., 1, 2, 3) into its ordinal representation (e.g., 1st, 2nd, 3rd).

        Args:
            day_number (int): The day number to be converted.

        Returns:
            str: The day number with its ordinal suffix.
    """
    if 10 <= day_number % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(day_number % 10, "th")

    return f"{day_number}{suffix}"
