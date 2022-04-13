#!/bin/python
from multiprocessing.sharedctypes import Value
import monitor
import qserver
from sys import argv, stderr
from queue import Empty

if __name__ == '__main__':
	print(argv)
	if len(argv) != 3:
		print(f"Usage: {argv[0]} hostname port", file=stderr)
		exit(1)
	host, port = argv[1:3]
	port = int(port)
	qs = qserver.QueueServer(host, port)
	
	mon = monitor.Monitor([[4, 4]], [0, 8], [0, 8], 16)

	mon.draw()

	loop_idx = 0
	while True:
		try:
			data = qs.pop()
			if len(data) != 0:
				print(data)
				mon.plot(data)
				print(f"log::loop index {loop_idx}")
			mon.update()
		except KeyboardInterrupt:
			exit(0)
		except BlockingIOError:
			pass
		except ValueError:
			pass
		except Empty:
			pass

		loop_idx = (loop_idx + 1) % 114514
	
