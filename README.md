# Medical-Appointment-No-show-Analysis

This project analyzes **no-show behavior in medical appointments** using a real-world dataset from Brazil 🇧🇷. It explores key factors like age, gender, health conditions, and scheduling gaps to understand why patients miss their appointments.

---

## 📦 Dataset Overview

This dataset contains information on **110,527 medical appointments**, each with **14 associated features**, such as patient demographics, medical conditions, and whether or not the patient showed up.

**Source:** [Kaggle Dataset by Joni Hoppen](https://www.kaggle.com/datasets/joniarroba/noshowappointments)

### 📚 Features Description

| Feature              | Description                                                                 |
|----------------------|-----------------------------------------------------------------------------|
| `PatientId`          | Unique identifier for each patient                                          |
| `AppointmentID`      | Unique ID for each appointment                                              |
| `Gender`             | Gender of the patient (`Male` / `Female`)                                   |
| `ScheduledDay`       | Date when the appointment was scheduled                                     |
| `AppointmentDay`     | Date of the actual appointment                                               |
| `Age`                | Age of the patient (values between 0 and 100 used)                          |
| `Neighbourhood`      | Location of the hospital or clinic                                          |
| `Scholarship`        | Whether the patient is enrolled in Bolsa Família (social welfare program)   |
| `Hipertension`       | Whether the patient has hypertension (1 = yes, 0 = no)                      |
| `Diabetes`           | Whether the patient has diabetes (1 = yes, 0 = no)                          |
| `Alcoholism`         | Whether the patient is an alcoholic (1 = yes, 0 = no)                       |
| `Handcap`            | Whether the patient is handicapped (1 = yes, 0 = no)                        |
| `SMS_received`       | Whether the patient received an SMS reminder (1 = yes, 0 = no)              |
| `No-show`            | Whether the patient missed the appointment (1 = no-show, 0 = showed up)     |

---

## 🎯 Project Objectives

- Clean and preprocess the data
- Perform **Exploratory Data Analysis (EDA)**
- Visualize no-show patterns and distributions
- Identify trends based on demographics and scheduling behavior

---

## 📊 Visualizations (Matplotlib)

The current version includes visualizations for:

- 📅 Appointments and no-shows by **day**, **month**, and **year**
- 📍 Top neighborhoods with highest no-show rates
- 📈 No-show rates by **age group**, **gender**, and **chronic conditions**
- ⏳ No-show behavior based on time gap between scheduling and appointment
- 📲 Impact of **SMS reminders** on no-show behavior

---

## 🚧 Future Work

> I'm planning to take this project further with the following:

- 🔁 Convert all charts to **interactive visualizations** using `Plotly`
- 📊 Build an interactive dashboard using **Dash**
- 📄 Add a detailed **report** with key findings and insights
- 🤖 Possibly develop a **predictive model** for no-show classification

---
## 💬 Credits

- Dataset provided by [Joni Hoppen & Aquarela Analytics](https://www.kaggle.com/datasets/joniarroba/noshowappointments)
- Inspiration from real-world medical scheduling challenges
- Scholarship reference: [Bolsa Família (Wikipedia)](https://en.wikipedia.org/wiki/Bolsa_Fam%C3%ADlia)

---

Feel free to ⭐ star the repo or fork it if you're interested in healthcare data, EDA, or Python visualization!


