import time
import asyncio

import optparse


class Scanner(object):
    '''
    Attributes:
        batch_size:
            Asyncio will establish batch_size connection requests each time,
            the smaller the batch_size, the highter the accuracy and the slower the speed,
            type: int
            default: 4000
        file:
            The path where results will be sotred
            type: str
            default: "abailable_ports.txt"
    '''

    def __init__(self, batch_size: int = 4000, file: str = 'available_ports.txt'):
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
            print(f'port {port} "OPEN"')
            self.output[port] = 'OPEN'
        except:
            print(f'port {port} "CLOSED"')

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
    start = time.time()
    parser = optparse.OptionParser("usage -%prog + -H <tgtHost> -P <tgtPorts>")
    parser.add_option('-H', dest='tgtHost', type='string',
                      help='specify a host')
    parser.add_option('-P', dest='tgtPorts', type='string',
                      help='specify target port(s)')
    (options, args) = parser.parse_args()
    host = options.tgtHost
    ports = options.tgtPorts
    if ports:
        ports = ports.split(',')
    if not host:
        host = 'localhost'
    scanner = Scanner()
    scanner.scan(host, ports)
    print(time.time() - start)
