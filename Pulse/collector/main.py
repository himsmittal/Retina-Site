from coolanClient import CoolanClient
from machines import Machines
from machinePowerUtilization import MachinePowerUtilization
from worker import WorkerQueue
from Queue import Queue
import os

if __name__ == '__main__':
    user, password = os.getenv('USER'), os.getenv('PASSWORD')
    host, scheme = os.getenv('HOST'), os.getenv('HTTP_SCHEME')
    thread_count = int(os.getenv('THREADS', 20))

    # Login to coolan
    client = CoolanClient(host, scheme)
    client.login(user, password)

    machines = Machines(host, scheme)
    machines.get_total_machines()

    # Populating request queue
    q = Queue()
    for val in xrange(machines.total_machines/machines.params['size']):
        q.put(val)

    # Creating workers and concurrently executing get machine calls
    worker = WorkerQueue(q, thread_count)
    worker.parallelize(machines.get_machines)

    # Writing data to disk
    with open('data/machines.csv', 'w') as fp:
        for machine in machines.list_machines():
            fp.write("%s\n" % ','.join(machine))

    # with open('data/machines.csv', 'r') as fp:
    #     for rec in fp.readlines():
    #         machines.machines.append(tuple(rec.strip().split(',')))

    # Getting machine time series data points
    q = Queue()
    for mId, hName in machines.list_machines()[:20]:
        q.put((mId, hName))

    # Creating workers and concurrently executing get machine power util details
    worker = WorkerQueue(q, thread_count)
    power_util = MachinePowerUtilization(host, scheme)
    worker.parallelize(power_util.get_machine_details)
