# Final Exam
import random
import string
import csv
import time
import requests
from concurrent.futures import ThreadPoolExecutor

student_id = input("Enter your student ID: ")
last_digit = int(student_id[-1])
last_two_digits = int(student_id[-2:])

virtual_users = (last_two_digits * 2) + 50
ramp_up_time = last_digit * 5

print(f"Virtual Users: {virtual_users}")
print(f"Ramp-up Time: {ramp_up_time} seconds")



def random_string(length=6):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

users = []

for i in range(15):
    username = f"user_{random_string()}"
    password = random_string(8)

    users.append({
        "username": username, 
        "password": password
        })
    
csv_file = "test_users.csv"

with open(csv_file, mode='w', newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["username", "password"])
    writer.writeheader()
    writer.writerows(users)

print(f"Generated {len(users)} test users and saved to {csv_file}")

url = "https://reqres.in/api/login"

def send_request(user):
    payload = {
        "email": "donaljtrump@reqres.in",
        "password": "bombthesh1t"
    }

    try: 
        start = time.time()
        resposne = requests.post(url, json=payload)
        end = time.time()

        print(f"Status: {resposne.status_code}, Response Time: {end - start:.2f} seconds")

    except Exception as e:
        print("Request failed:", e)

delay = ramp_up_time / virtual_users if virtual_users > 0 else 0

with ThreadPoolExecutor(max_workers=virtual_users) as executor:
    for i in range(virtual_users):
        executor.submit(send_request, users)
        time.sleep(delay)

print("\nLoad test finished.")
    
        