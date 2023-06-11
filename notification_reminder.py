from plyer import notification
import datetime
import time
import schedule
import random_word
from PyDictionary import PyDictionary

def fetch_word_of_the_day():
    # Generate a random word
    word_generator = random_word.RandomWords()
    r_word = word_generator.get_random_word()
    
    # Get the meaning of the random word
    dictionary = PyDictionary()
    meaning = dictionary.meaning(r_word)
    
    if meaning is None:
        return r_word,None
    else:
        return r_word, meaning


# Fetch the word of the day
word_of_the_day, meaning = fetch_word_of_the_day()
word = str(word_of_the_day)
mean = str(meaning)
# Print the word and its meaning
print(f"Word of the Day ({datetime.date.today()}): {word_of_the_day}")
print(f"Meaning: {meaning}")


def set_reminder(reminder_text, reminder_time,word,mean):
    current_time = datetime.datetime.now()
    time_difference = reminder_time - current_time

    # Check if the reminder time has already passed
    if time_difference.total_seconds() <= 0:
        print("Invalid reminder time. It should be in the future.")
        return

    # Convert the time difference to seconds
    delay_seconds = time_difference.total_seconds()

    # Schedule the notification after the delay
    schedule.every(delay_seconds).seconds.do(send_notification, reminder_text)
    schedule.every(delay_seconds).seconds.do(send_notification1,word,mean)

    # Wait until the scheduled time is reached
    time.sleep(delay_seconds)
    schedule.run_pending()

def send_notification(reminder_text):
    notification.notify(
        title="Reminder",
        message=reminder_text,
        timeout=60  # Specify the notification timeout in seconds (e.g., 10 seconds)
    )
    print("Reminder set successfully!")

def send_notification1(word,mean):
    notification.notify(
        title=word,
        message=mean,
        timeout=60  # Specify the notification timeout in seconds (e.g., 10 seconds)
    )

# Example usage
today = datetime.datetime.today()
x = today.year
y = today.month
z = today.day
reminder_text = input("Enter the message : ")
reminder_time = datetime.datetime(x , y , z , 20, 41)  # Set the desired reminder time

set_reminder(reminder_text, reminder_time,word,mean)