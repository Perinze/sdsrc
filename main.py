from multiprocessing.sharedctypes import Value
import monitor
import qserver
from sys import argv, stderr

if __name__ == '__main__':
	print(argv)
	if len(argv) != 3:
		print(f"Usage: {argv[0]} hostname port", file=stderr)
		exit(1)
	host, port = argv[1:3]
	port = int(port)
	qs = qserver.QueueServer(host, port)
	
	mon = monitor.Monitor([[1, 1], [4, 6]], [0, 8], [0, 8], 16)

	mon.draw()
	while True:
		try:
			data = qs.pop()
			print(data)
			mon.plot(data)
			mon.update()
		except KeyboardInterrupt:
			exit(0)
		except BlockingIOError:
			pass
		except ValueError:
			pass
	
