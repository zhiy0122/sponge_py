import time
import socket
import threading
import asyncio


class TCPScanner(object):
    # port_list = [21, 22, 25, 80, 110, 118, 137,
    #              138, 139, 143, 443, 1433, 3306, 3389, 8080]
    output = {}

    def __init__(self, host, target_ports=None):
        self.host = host
        if target_ports is None:
            self.target_ports = [int(i) for i in range(0, 9999)]
        else:
            self.target_ports = target_ports

    async def scanner(self, host, port, output, file):
        print('scanning port {} at {}'.format(port, time.time()))
        try:
            await asyncio.open_connection(host, port)
            # await asyncio.wait_for(asyncio.open_connection(ip, port), timeout=30)
            file.write('port {} "OPEN"\n'.format(port))
            print('port {} "OPEN"\n'.format(port))
            output[port] = 'OPEN'
        except ConnectionRefusedError as conn_error:
            print('port {} "CLOSED"'.format(port))
        except OSError:
            print('port {} "CLOSED"'.format(port))
        except asyncio.TimeoutError:
            print('port {} "TIME OUT"'.format(port))

    def scan(self, batch_size):
        loop = asyncio.get_event_loop()
        ports_length = len(self.target_ports)
        range_times = ports_length // batch_size
        start_index = 0
        if range_times == 0:
            range_times = 1
        if range_times == 1:
            end_index = ports_length
        else:
            end_index = batch_size
        with open('open_port.txt', 'w') as file:
            file.write(self.host)
            for _ in range(range_times):
                port_range = self.target_ports[start_index: end_index]
                tasks = [self.scanner(self.host, port, self.output, file)
                         for port in port_range]
                start_index = end_index
                if end_index + batch_size > ports_length:
                    end_index = start_index + (ports_length % batch_size)
                else:
                    end_index = start_index + batch_size
                loop.run_until_complete(asyncio.wait(tasks))
            loop.close()


if __name__ == "__main__":
    scanner = TCPScanner('localhost')
    scanner.scan(2000)



