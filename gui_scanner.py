import socket
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from queue import Queue
import os
from datetime import datetime

# ---------------- MAIN WINDOW ----------------
root = tk.Tk()
root.title("Advanced TCP Port Scanner")
root.geometry("900x680")
root.configure(bg="#0f172a")

# ---------------- STYLE ----------------
style = ttk.Style()
style.theme_use("clam")

PRIMARY = "#0f172a"
SECONDARY = "#1e293b"
ACCENT = "#38bdf8"
SUCCESS = "#22c55e"
TEXT = "#e2e8f0"

style.configure("TLabel", background=PRIMARY, foreground=TEXT, font=("Segoe UI", 10))
style.configure("Header.TLabel", font=("Segoe UI", 22, "bold"), foreground=ACCENT)
style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6)

style.configure("Card.TLabelframe",
                background=SECONDARY,
                foreground=ACCENT)

style.configure("Card.TLabelframe.Label",
                background=SECONDARY,
                foreground=ACCENT,
                font=("Segoe UI", 11, "bold"))

# ---------------- VARIABLES ----------------
open_ports = []
closed_ports = []
scanning = False
port_queue = Queue()
TOTAL_PORTS = 0

# ---------------- SCAN FUNCTION ----------------
def scan_port(target):
    global scanning

    while not port_queue.empty() and scanning:
        port = port_queue.get()

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((target, port))

            if result == 0:
                open_ports.append(port)
                result_box.insert(tk.END, f"[OPEN]   Port {port}\n")
            else:
                closed_ports.append(port)

            sock.close()

        except:
            pass

        progress_bar["value"] += (100 / TOTAL_PORTS)
        root.update_idletasks()
        port_queue.task_done()


# ---------------- START SCAN ----------------
def start_scan():
    global scanning, TOTAL_PORTS

    if scanning:
        return

    target = target_entry.get()
    start_port = start_port_entry.get()
    end_port = end_port_entry.get()

    if not target or not start_port or not end_port:
        messagebox.showerror("Error", "All fields are required")
        return

    try:
        target = socket.gethostbyname(target)
        start_port = int(start_port)
        end_port = int(end_port)
    except:
        messagebox.showerror("Error", "Invalid input")
        return

    if start_port < 1 or end_port > 65535 or start_port > end_port:
        messagebox.showerror("Error", "Invalid port range")
        return

    # Reset
    result_box.delete(1.0, tk.END)
    progress_bar["value"] = 0
    open_ports.clear()
    closed_ports.clear()

    TOTAL_PORTS = end_port - start_port + 1

    for port in range(start_port, end_port + 1):
        port_queue.put(port)

    scanning = True
    status_bar.config(text="Status: Scanning...")

    for _ in range(100):
        thread = threading.Thread(target=scan_port, args=(target,))
        thread.daemon = True
        thread.start()

    threading.Thread(target=finish_scan, daemon=True).start()


# ---------------- FINISH SCAN ----------------
def finish_scan():
    port_queue.join()

    if scanning:
        result_box.insert(tk.END, "\n------------------------------\n")
        result_box.insert(tk.END, "Scan Completed\n")
        result_box.insert(tk.END, f"Open Ports  : {len(open_ports)}\n")
        result_box.insert(tk.END, f"Closed Ports: {len(closed_ports)}\n")
        result_box.insert(tk.END, "------------------------------\n")

    stop_scan()


# ---------------- STOP SCAN ----------------
def stop_scan():
    global scanning
    scanning = False
    status_bar.config(text="Status: Idle")


# ---------------- CLEAR RESULTS ----------------
def clear_results():
    result_box.delete(1.0, tk.END)
    progress_bar["value"] = 0
    status_bar.config(text="Status: Cleared")


# ---------------- EXPORT RESULTS ----------------
def export_results():
    if not open_ports and not closed_ports:
        messagebox.showwarning("Warning", "No results to export")
        return

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"scan_results_{timestamp}.txt"

    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, filename)

    with open(file_path, "w") as file:
        file.write("TCP PORT SCAN RESULTS\n")
        file.write("="*50 + "\n\n")
        file.write(f"Scan Time: {datetime.now()}\n\n")

        file.write("OPEN PORTS:\n")
        for port in open_ports:
            file.write(f"Port {port} - OPEN\n")

        file.write("\nCLOSED PORTS:\n")
        for port in closed_ports:
            file.write(f"Port {port} - CLOSED\n")

        file.write("\n")
        file.write("="*50 + "\n")
        file.write(f"Total Open Ports  : {len(open_ports)}\n")
        file.write(f"Total Closed Ports: {len(closed_ports)}\n")

    status_bar.config(text=f"Status: Results saved → {filename}")
    messagebox.showinfo("Success", f"Results saved in project folder:\n{filename}")


# ---------------- HEADER ----------------
header = ttk.Label(root, text="TCP PORT SCANNER", style="Header.TLabel")
header.pack(pady=20)

# ---------------- INPUT CARD ----------------
input_card = ttk.LabelFrame(root, text="Scan Configuration", style="Card.TLabelframe")
input_card.pack(fill="x", padx=30, pady=10)

ttk.Label(input_card, text="Target IP / Domain:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
target_entry = ttk.Entry(input_card, width=35)
target_entry.insert(0, "127.0.0.1")
target_entry.grid(row=0, column=1, padx=10)

ttk.Label(input_card, text="Start Port:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
start_port_entry = ttk.Entry(input_card, width=35)
start_port_entry.insert(0, "1")
start_port_entry.grid(row=1, column=1)

ttk.Label(input_card, text="End Port:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
end_port_entry = ttk.Entry(input_card, width=35)
end_port_entry.insert(0, "1024")
end_port_entry.grid(row=2, column=1)

# ---------------- BUTTONS ----------------
button_frame = tk.Frame(root, bg=PRIMARY)
button_frame.pack(pady=15)

ttk.Button(button_frame, text="Start Scan", command=start_scan).grid(row=0, column=0, padx=15)
ttk.Button(button_frame, text="Stop Scan", command=stop_scan).grid(row=0, column=1, padx=15)
ttk.Button(button_frame, text="Clear", command=clear_results).grid(row=0, column=2, padx=15)
ttk.Button(button_frame, text="Export Results", command=export_results).grid(row=0, column=3, padx=15)

# ---------------- PROGRESS BAR ----------------
progress_bar = ttk.Progressbar(root, length=750, mode="determinate")
progress_bar.pack(pady=10)

# ---------------- RESULTS CARD ----------------
result_card = ttk.LabelFrame(root, text="Scan Results", style="Card.TLabelframe")
result_card.pack(fill="both", expand=True, padx=30, pady=10)

result_frame = tk.Frame(result_card, bg="#000000")
result_frame.pack(fill="both", expand=True, padx=10, pady=10)

scrollbar = tk.Scrollbar(result_frame)
scrollbar.pack(side="right", fill="y")

result_box = tk.Text(result_frame,
                     bg="#000000",
                     fg=SUCCESS,
                     insertbackground="white",
                     font=("Consolas", 11),
                     yscrollcommand=scrollbar.set)

result_box.pack(fill="both", expand=True)
scrollbar.config(command=result_box.yview)

# ---------------- STATUS BAR ----------------
status_bar = tk.Label(root,
                      text="Status: Idle",
                      bg=SECONDARY,
                      fg=TEXT,
                      
                      anchor="w",
                      padx=10)

status_bar.pack(fill="x", side="bottom")

root.mainloop()