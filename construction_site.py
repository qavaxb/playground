"""
Script showing example of multiple workers-threads usage
"""

import logging
import subprocess
from threading import Thread
from queue import Queue

LIST_OF_JOBS = ['ls',
                'ls -la /etc/',
                "echo 'juz wstalem'",
                'cat ' + __file__
               ]

LOGGER = logging.getLogger("Construction_site")

PERSONS_NAMES = ["John", "Tom", "Will", "Sam", "Tim", "Bart"]

work_results = []

logging.basicConfig(level=logging.DEBUG)

job_queue = Queue(maxsize=100)


class Worker(Thread):
    """
    Threaded worker to process the jobs
    """

    def __init__(self, *args, **kwargs):
        """
        Preparing worker
        """
        Thread.__init__(self, *args, **kwargs)
        self.daemon = True
        self.job_done = 0

    @staticmethod
    def _process_cmd(cmd, timeout=2):
        """
        Function spawning processes with requested commands
        """
        result = ''.encode()
        cmd = cmd.split()

        with subprocess.Popen(cmd, stdout=subprocess.PIPE) as proc:

            try:
                proc_stdout, proc_stderr = proc.communicate(timeout=timeout)

                if proc_stdout:
                    LOGGER.debug("Job result: %s", proc_stdout)
                    result = proc_stdout

                if proc_stderr:
                    LOGGER.error("Accident: %s", proc_stderr)

            except subprocess.TimeoutExpired:
                result = "Timeout expired".encode()

        return result

    def run(self):
        """
        Function processing the jobs
        """
        while True:
            job = job_queue.get()
            LOGGER.debug("{name}: I will process the job: {job}".format(
                name=self.getName(),
                job=job))
            work_results.append(self._process_cmd(job).decode())
            self.job_done += 1
            job_queue.task_done()


def construction_recruitment(number_of_workers=5):
    """
    Recruit the workers
    """
    hr_list = {}
    if number_of_workers > len(PERSONS_NAMES):
        raise ValueError("Too much of workers needed")

    if number_of_workers < 1:
        raise ValueError("If you have work to do, recruit person")

    for number in range(number_of_workers):
        name = PERSONS_NAMES[number]
        hr_list[name] = Worker(name=name)
    return hr_list


def construction_schedule(worker_list):
    """
    Schedule a work for workers
    """
    for name in worker_list:
        worker_list[name].start()

def construction_hall_of_fame(worker_list):
    """
    Schedule a work for workers
    """
    for name in worker_list:
        LOGGER.info("{name} did {count} jobs".format(
            name=name,
            count=worker_list[name].job_done)
                   )

def main():
    """
    Main function to execute as script
    """
    LOGGER.debug("Feeding the queue of jobs")

    for job in LIST_OF_JOBS:
        job_queue.put(job)

    LOGGER.debug("Recruiting workers")
    hr_list = construction_recruitment()

    LOGGER.debug("Establishing time schedule")
    construction_schedule(hr_list)

    LOGGER.debug("Waiting for construction site to be closed")
    job_queue.join()
    construction_hall_of_fame(hr_list)
    LOGGER.debug("Construction site closed")


if __name__ == "__main__":
    main()
