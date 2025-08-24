
### 📚 UniGrade

**UniGrade** is a lightweight desktop application designed for university students who want to manage their academic records digitally. The app helps users keep track of all their exams, calculate their **weighted GPA**, and monitor their academic performance—all **locally on their machine**, without requiring an internet connection.

With UniGrade, users can:

* Register themselves and manage their personal academic profile
* Add, edit, and remove exams with their corresponding grades and credits (CFU)
* Calculate both **weighted** and **arithmetic GPA** in real-time
* Customize personal settings to fit their preferences
* Store all data securely using **SQLite**, ensuring full offline functionality

### Developer Build Instructions

To build the program from source, run the following command in your terminal:

```sh
pyinstaller --onefile --windowed --icon=assets/unigrade-logo-icon.ico --add-data "assets;assets" app.py --name UniGrade
```

UniGrade is perfect for students who want a simple, intuitive, and offline tool to manage their university transcript efficiently.

