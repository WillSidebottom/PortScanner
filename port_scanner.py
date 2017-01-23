#! /usr/bin/python3

"""
This port scanner uses an implemented version of the threader module to create a
priorty queue port scanner.
- Uses the socket library to open up connections. Cool.
- Creates a sub-class of the Thread class which was imported. +1 for polymorphism I guess.
- Synchronizes the threads using a Multi Threaded Priorty Queue with Locks. Hopefully...
- Uses Argparse - a fancy/shmancy argument parser library
"""

import socket
import threading
import queue
import argparse

class MyThread(threading.Thread):
	def __init__(self, host, q, print_lock):
		threading.Thread.__init__(self)
		self.host = host
		self.q = q 
		self.print_lock = print_lock

	def run(self):
		while True:
			if not self.q.empty():
				port = self.q.get()
				connection_scan(self.host, port, self.print_lock)
				self.q.task_done()

def connection_scan(host, port, print_lock):
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.settimeout(1)
		s.connect((host, port))
		print_lock.acquire()
		print('[+] tcp open on port: {}'.format(port))
	except socket.error:
		print_lock.acquire()
		print('[-] tcp close on port {}'.format(port))
	finally:
		print_lock.release()
	try:
		s.sendall(b'hello')
		banner = s.recv(100)
		print_lock.acquire()
		print('\t[+] Banner: {}'.format(banner.decode().strip('\r\n')))
		print_lock.release()
	except:
		pass
	finally:
		s.close()

def port_scan(host, ports):
	try:
		target_ip = socket.gethostbyname(host)
	except Exception as e:
		print('[-] Cannot resolve {} : Unknown host : {}'.format(host, e))
		return
	else:
		print('Scan results for: {}'.format(target_ip))
		q = queue.Queue()
		print_lock = threading.Lock()

		for x in range(30):
			thread = MyThread(host, q, print_lock)
			thread.daemon = True
			thread.start()

		for port in ports:
			q.put(port)

		q.join()

def main():
	parser = argparse.ArgumentParser(description='A simple port scanner')
	parser.add_argument('host', type=str, help='A host IP address')
	parser.add_argument('ports', type=int, nargs='+', help='A space separated list of ports')
	args = parser.parse_args()

	if (args.host == None) | (args.ports == None):
		print(parser.usage)
		exit(0)

	port_scan(args.host, args.ports)

if __name__ == '__main__':
	main()