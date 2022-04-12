import socket
import queue
import re
import selectors

from numpy import block

class QueueServer(object):

	def __init__(self, host, port, tmp_size=1024):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.bind((host, port))
		self.sock.setblocking(False)
		self.sel = selectors.EpollSelector()
		self.sel.register(self.sock, selectors.EVENT_READ)

		self.buf = ''
		self.TMP_SIZE = tmp_size
		self.queue = queue.Queue()

		self.regex = r"\^([\d\.,]+)\$"
		self.delim = r","

	def pop(self):
		if self.queue.empty():	# is loop safe?
			self.parse()
			return []
		# print("log::pop end of block")
		return self.queue.get(block=False)

	def parse(self):
		# print("log::parse enter")
		self.recv()
		while True:
			match = re.search(self.regex, self.buf)
			if not match:
				break
			_, end = match.span()
			self.buf = self.buf[end:]
			substr = match.group(1)
			data = list(map(float, re.split(self.delim, substr)))
			# print("log::match end")
			self.queue.put(data)
		# print("log::parse end")

	def recv(self):
		# print("log::recv enter")
		# tmp, _ = self.sock.recvfrom(self.TMP_SIZE)
		events = self.sel.select(timeout=0)
		# print(len(events))
		for key, _ in events:
			if key.fileobj == self.sock: # and mask & selectors.EVENT_READ:
				tmp, _ = self.sock.recvfrom(self.TMP_SIZE)
				self.buf = ''.join([self.buf, bytes.decode(tmp)])
		# print("log::recv end")
