import time
from redis import Redis
from rq import Queue
from rq.job import Job

# rq worker -u redis://172.17.0.3:6379

q = Queue(connection=Redis("172.17.0.2"))

import BqManager as bq


result = q.enqueue(bq.get_datasets)
while not result.is_finished:
    time.sleep(1)
all_ids = []
for datatset in result.return_value:
    result = q.enqueue(
        bq.get_tables_of_dataset,
        args=("mdm-data-preprod", datatset.dataset_id),
        job_timeout="-1",
    )
    all_ids.append(result.id)

jobs = Job.fetch_many(all_ids, connection=Redis("172.17.0.2"))
while not all([job.is_finished for job in jobs]):
    time.sleep(1)
    jobs = Job.fetch_many(all_ids, connection=Redis("172.17.0.2"))
    for job in jobs:
        if job.is_finished or job.is_failed:
            all_ids.remove(job.id)
