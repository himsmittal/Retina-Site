from threading import Thread


class WorkerQueue(object):
    def __init__(self, queue, thread_count):
        self.queue = queue
        self.thread_count = thread_count
        self.results = []

    def parallelize(self, function):
        for i in range(self.thread_count):
            t = Thread(target=function, args=(self.queue,))
            t.daemon = True
            t.start()
        self.queue.join()
