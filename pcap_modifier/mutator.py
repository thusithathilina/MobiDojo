import os
import random
from datetime import datetime
from scapy.all import *

def get_random_byte():
    return random.randint(0, 255)

def save_traffic(packets, count):
    filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{count}.pcap"
    wrpcap(filename, packets)
    print(f"Generated traffic saved as {filename}")

def main():
    # Import the specific mutator
    from mutator_InitialUEMessage import select_seed, select_offsets, generate_traffic

    seed_file = select_seed()
    offsets = select_offsets()
    count = int(input("Enter the number of random traffic to generate: "))
    
    modified_packets = generate_traffic(seed_file, offsets, count)
    save_traffic(modified_packets, count)

if __name__ == "__main__":
    main()