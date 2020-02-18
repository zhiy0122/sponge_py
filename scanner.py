import time
import asyncio


class Scanner(object):
    '''
    Attributes:
        batch_size:
            Asyncio will establish batch_size connection requests each time,
            the smaller the batch_size, the highter the accuracy and the slower the speed,
            type: int
            default: 2000
        file:
            The path where results will be sotred
            type: str
            default: "abailable_ports.txt"
    '''

    def __init__(self, batch_size: int = 2000, file: str = 'available_ports.txt'):
        assert type(batch_size) == int, \
            '''the type of batch_size must be int'''
        self.batch_size = batch_size
        self.file = file
        self.output = {}

    async def scanner(self, host, port, file):
        '''
        scanner is the starter of method "scan"
        Args:
            host: target host
            port: a specifed port
            file: the path where results will be stored
        '''
        print(f'scanning port {port} at {time.time()}')
        try:
            await asyncio.open_connection(host, port)
            # await asyncio.wait_for(asyncio.open_connection(ip, port), timeout=30)
            file.write(f'port {port} "OPEN"\n')
            print(f'port {port} "OPEN"\n')
            self.output[port] = 'OPEN'
        except ConnectionRefusedError:
            print(f'port {port} "CLOSED"')
        except OSError:
            print(f'port {port} "CLOSED"')
        except asyncio.TimeoutError:
            print(f'port {port} "TIME OUT"')

    def scan(self, tgt_host, tgt_ports=None):
        '''
        scan target_host:target_ports
        Args:
            tgt_host: target host
            tgt_ports: a list of target ports
        '''
        assert tgt_host is not None, \
            '''you must specify a tgt_host'''

        if not tgt_ports:
            tgt_ports = [int(i) for i in range(0, 9999)]
        loop = asyncio.get_event_loop()
        batch_size = self.batch_size
        ports_length = len(tgt_ports)
        range_times = ports_length // batch_size
        start_index = 0
        if range_times == 0:
            range_times = 1
        end_index = ports_length if range_times == 1 else batch_size
        with open(f'{self.file}', 'w') as file:
            file.write(f'{tgt_host}\n')
            for _ in range(range_times):
                port_batch = tgt_ports[start_index: end_index]
                tasks = [self.scanner(tgt_host, port, file)
                         for port in port_batch]
                start_index = end_index
                if end_index + batch_size > ports_length:
                    end_index = start_index + (ports_length % batch_size)
                else:
                    end_index = start_index + batch_size
                loop.run_until_complete(asyncio.wait(tasks))
            loop.close()
        print()
        print(self.output)


if __name__ == "__main__":
    scanner = Scanner()
    scanner.scan('localhost')
