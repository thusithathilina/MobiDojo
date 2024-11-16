import os
import tkinter as tk
from tkinter import ttk, filedialog
import binascii
from scapy.all import *
from scapy.layers.inet import IP
from scapy.layers import sctp
from scapy.packet import Packet
from scapy.fields import *

# Define a basic NGAP layer
class NGAP(Packet):
    name = "NGAP"
    fields_desc = [
        ByteEnumField("PDU_Type", 0, {0: "Initiating Message", 1: "Successful Outcome", 2: "Unsuccessful Outcome"}),
        ByteField("ProcedureCode", 0),
        ShortField("ProtocolIE_ID", 0),
    ]

# Bind NGAP to SCTP
bind_layers(SCTP, NGAP, dport=38412)
bind_layers(SCTP, NGAP, sport=38412)

def get_file_name():
    file_name = filedialog.askopenfilename(filetypes=[("PCAP files", "*.pcap")])
    if not file_name:
        print("No file selected.")
        return None
    if not os.path.isfile(file_name):
        print(f"The {file_name} does not exist.")
        return None
    return file_name

def read_pcap(file_name):
    return rdpcap(file_name)

def update_display():
    global current_packet_raw
    if not modified_packets:
        hex_display.delete(1.0, tk.END)
        hex_display.insert(tk.END, "No PCAP file loaded. Please select a file.")
        return
    
    current_packet = modified_packets[current_packet_index]
    current_packet_raw = raw(current_packet)
    hex_dump = binascii.hexlify(current_packet_raw).decode()
    formatted_hex = ' '.join(hex_dump[i:i+2] for i in range(0, len(hex_dump), 2))
    hex_lines = [formatted_hex[i:i+48] for i in range(0, len(formatted_hex), 48)]
    
    hex_display.delete(1.0, tk.END)
    for i, line in enumerate(hex_lines):
        hex_display.insert(tk.END, f"{i*16:04x}   {line}\n")
    
    # Color coding
    total_bytes = len(current_packet_raw)
    eth_end = min(14, total_bytes)
    ip_end = min(34, total_bytes)
    sctp_end = min(62, total_bytes)
    
    def byte_to_text_index(byte_num):
        line = byte_num // 16 + 1
        col = (byte_num % 16) * 3 + 7
        return f"{line}.{col}"

    hex_display.tag_add("ethernet", "1.7", byte_to_text_index(eth_end))
    if eth_end < total_bytes:
        hex_display.tag_add("ipv4", byte_to_text_index(eth_end), byte_to_text_index(ip_end))
    if ip_end < total_bytes:
        hex_display.tag_add("sctp", byte_to_text_index(ip_end), byte_to_text_index(sctp_end))
    if sctp_end < total_bytes:
        hex_display.tag_add("ngap", byte_to_text_index(sctp_end), tk.END)

def on_hex_click(event):
    index = hex_display.index(f"@{event.x},{event.y}")
    line, col = map(int, index.split('.'))
    byte_offset = (line - 1) * 16 + (col - 7) // 3
    selected_offset.set(byte_offset)
    offset_label.config(text=f"Selected Offset: {byte_offset:04x}")

def modify_byte():
    global current_packet_raw
    if not modified_packets:
        return
    offset = selected_offset.get()
    new_value = int(new_byte_value.get(), 16)
    
    modified_packet = current_packet_raw[:offset] + bytes([new_value]) + current_packet_raw[offset+1:]
    modified_packets[current_packet_index] = Ether(modified_packet)
    
    update_display()

def next_packet():
    global current_packet_index
    if modified_packets and current_packet_index < len(modified_packets) - 1:
        current_packet_index += 1
        update_display()

def prev_packet():
    global current_packet_index
    if modified_packets and current_packet_index > 0:
        current_packet_index -= 1
        update_display()

def save_pcap():
    if file_name:
        wrpcap(file_name, modified_packets)

def save_as_pcap():
    if modified_packets:
        new_file_name = save_as_entry.get()
        if new_file_name:
            wrpcap(new_file_name, modified_packets)

def select_file():
    global file_name, packets, modified_packets, current_packet_index, current_packet_raw
    file_name = get_file_name()
    if file_name:
        packets = read_pcap(file_name)
        modified_packets = [p for p in packets]
        current_packet_index = 0
        current_packet_raw = None
        update_display()
        root.title(f"PCAP Builder - {os.path.basename(file_name)}")

# Create the main window
root = tk.Tk()
root.title("PCAP Builder")

# Create and pack the hex display
hex_display = tk.Text(root, font=("Courier", 12), wrap=tk.NONE, height=20)
hex_display.pack(expand=True, fill=tk.BOTH)
hex_display.bind("<Button-1>", on_hex_click)

# Define colors for different areas
hex_display.tag_configure("ethernet", background="#FFD3B6")  # Light Peach
hex_display.tag_configure("ipv4", background="#DCEDC1")      # Light Lime
hex_display.tag_configure("sctp", background="#A8E6CF")      # Light Mint
hex_display.tag_configure("ngap", background="#FF8B94")      # Light Pink

# Create a frame for legend
legend_frame = ttk.Frame(root)
legend_frame.pack(pady=5)

# Add legend items
ttk.Label(legend_frame, text="Ethernet", background="#FFD3B6", padding=5).pack(side=tk.LEFT, padx=5)
ttk.Label(legend_frame, text="IPv4", background="#DCEDC1", padding=5).pack(side=tk.LEFT, padx=5)
ttk.Label(legend_frame, text="SCTP", background="#A8E6CF", padding=5).pack(side=tk.LEFT, padx=5)
ttk.Label(legend_frame, text="NGAP", background="#FF8B94", padding=5).pack(side=tk.LEFT, padx=5)

# Create a frame for input fields
input_frame = ttk.Frame(root)
input_frame.pack(pady=10)

# Create and pack input fields
selected_offset = tk.IntVar()
offset_label = ttk.Label(input_frame, text="Selected Offset: 0000")
offset_label.grid(row=0, column=0, padx=5)

ttk.Label(input_frame, text="New Value (hex):").grid(row=0, column=1, padx=5)
new_byte_value = ttk.Entry(input_frame, width=10)
new_byte_value.grid(row=0, column=2, padx=5)

# Create and pack the modify button
modify_button = ttk.Button(input_frame, text="Modify", command=modify_byte)
modify_button.grid(row=0, column=3, padx=5)

# Create navigation buttons
nav_frame = ttk.Frame(root)
nav_frame.pack(pady=10)

prev_button = ttk.Button(nav_frame, text="Previous Packet", command=prev_packet)
prev_button.grid(row=0, column=0, padx=5)

next_button = ttk.Button(nav_frame, text="Next Packet", command=next_packet)
next_button.grid(row=0, column=1, padx=5)

# Create save buttons and entry
save_frame = ttk.Frame(root)
save_frame.pack(pady=10)

save_button = ttk.Button(save_frame, text="Save", command=save_pcap)
save_button.grid(row=0, column=0, padx=5)

save_as_button = ttk.Button(save_frame, text="Save As...", command=save_as_pcap)
save_as_button.grid(row=0, column=1, padx=5)

save_as_entry = ttk.Entry(save_frame, width=20)
save_as_entry.grid(row=0, column=2, padx=5)

# Create file selection button
file_select_frame = ttk.Frame(root)
file_select_frame.pack(pady=10)

select_file_button = ttk.Button(file_select_frame, text="Select PCAP File", command=select_file)
select_file_button.pack()

# Initialize global variables
file_name = None
packets = []
modified_packets = []
current_packet_index = 0
current_packet_raw = None

# Initial display update
update_display()

# Start the GUI event loop
root.mainloop()