import json
import requests


# url = 'http://127.0.0.1:9997/user/login'
# url = 'http://127.0.0.1:9998/doctors/'
def create_doctor():
    url = 'http://127.0.0.1:9998/doctors/'
    # create doctor
    data = {
        "name"         : {
            "fname": "John",
            "lname": "Doe",
        },
        "email"        : "johndoe@example.com",
        "image"        : "https://cdn-icons-png.flaticon.com/512/3774/3774299.png",
        "year_of_birth": 1980,
        "address"      : {
            "street"  : "123 Main St",
            "district": "District 1",
            "city"    : "City",
        },
        "phone"        : "123456789",
        "specialties"  : [
            {
                "name": "Khoa Da Liễu",
            }
        ],
        "level"        : {
            "name": "Senior",
        },
        "salary"       : 10000,
        "place_of_work": {
            "name": "Hospital A",
        },
        "year_of_work" : 10,
    }
    response = requests.post(url, json=data)
    response = response.json()
    print(response)


def create_patient():
    url = 'http://127.0.0.1:9996/patients/information/'
    for i in range(2, 10):
        fname = f"John{i}"
        lname = f"Doe{i}"
        phone = f"123456789{i}"
        data = {
            "name"        : {
                "fname": fname,
                "lname": lname,
            },
            "day_of_birth": "1980-01-01",
            "gender"      : "Male",
            "address"     : {
                "street"  : "123 Main St",
                "district": "District 1",
                "city"    : "City",
            },
            "phone"       : phone,
        }
        response = requests.post(url, json=data)
        response = response.json()
        print(response)


# create_patient()

def create_medical():
    url = 'http://127.0.0.1:9996/patients/1/history_medical/'
    for i in range(1, 5):
        data = {
            "patient_information" : i,  # ID của bệnh nhân
            "doctor"              : 5,
            "place_of_examination": "Hospital A",
            "pathology"           : "Flu",
            "treatment"           : "Rest and hydration",
            "cost"                : 50000,
            "paymented"           : 50000,
            "description"         : "Patient recovered well",
            "evaluation"          : 5,
        }
        response = requests.post(url, json=data)
        response = response.json()
        print(response)


# create_medical()

def create_appointment():
    url = 'http://127.0.0.1:9995/appointments/'
    for i in range(4, 10):
        data = {
            "patient" : i,
            "doctor"  : 5,
            "place_of_examination"    : "cs1",
            "appointment_date_time": "2022-01-01T00:00:00Z",
            "description"          : "description",
        }
        response = requests.post(url, json=data)
        response = response.json()
        print(response)

# create_appointment()
# data = {
#     'username': 'anhgdt',
#     'password':'Song3goc',
# }
# response = requests.post(url, json=data)
# response = requests.get(url)
# response = response.json()
# print(response)
