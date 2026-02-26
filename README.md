🔍 Advanced TCP Port Scanner








📌 Overview

The Advanced TCP Port Scanner is a multi-threaded network scanning application built using Python and Tkinter.
It allows users to scan a target IP address or domain to identify open and closed TCP ports within a specified range.

This project demonstrates practical knowledge of:

Network socket programming

Multi-threading for performance optimization

GUI-based tool development

Real-time progress monitoring

File handling and result exporting

Basic cybersecurity scanning concepts

🚀 Features

✅ Multi-threaded TCP scanning

✅ Custom target (IP / Domain)

✅ Custom port range (1 – 65535)

✅ Real-time scan progress bar

✅ Start / Stop scan functionality

✅ Open & closed port detection

✅ Scrollable results panel

✅ Auto-export results to .txt file

✅ Professional dark-themed GUI

✅ Clean and structured output

🛠 Technologies Used

Python 3.x

socket – TCP connection handling

threading – Concurrent scanning

queue – Thread-safe task management

tkinter – GUI framework

datetime – Timestamped exports

⚙ Installation
1️⃣ Clone the Repository
git clone https://github.com/RehmanAjaz/TCP-Port-Scanner.git
cd port-scanner
2️⃣ Run the Application
python scanner.py

No external dependencies are required (uses standard Python libraries).

🖥 How It Works

User enters:

Target IP address or domain

Start port

End port

The scanner:

Resolves the domain to IP

Creates multiple threads

Attempts TCP connection using socket.connect_ex()

Identifies port state based on response code

Results:

Displayed in real-time

Logged internally

Saved automatically as a timestamped .txt file

📂 Project Structure
port-scanner/
│── scanner.py
│── scan_results_YYYY-MM-DD_HH-MM-SS.txt
│── README.md
📊 Example Output
[OPEN]   Port 80
[OPEN]   Port 443
[OPEN]   Port 22

------------------------------
Scan Completed
Open Ports  : 3
Closed Ports: 1021
------------------------------
🎯 Use Cases

Basic network auditing

Identifying running services

Cybersecurity lab assignments

Educational network programming practice

Portfolio demonstration project

🔐 Ethical Use Disclaimer

This tool is intended strictly for educational purposes and authorized network testing only.

⚠ Do not scan networks or systems without explicit permission.

Unauthorized scanning may violate laws and regulations.

📈 Future Improvements

SYN scanning (using Scapy)

Service detection & banner grabbing

OS fingerprinting

Export to CSV / JSON

Scan history database

Integration with vulnerability APIs

Cross-platform packaging (.exe)

👨‍💻 Author

Developed as a cybersecurity and network programming project.
