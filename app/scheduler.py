
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_MAX_INSTANCES, EVENT_JOB_EXECUTED
from config import db_url

scheduler = BackgroundScheduler(executors={'default': {'type': 'threadpool', 'max_workers': 50}})
scheduler.add_jobstore('sqlalchemy', url= db_url)

if scheduler.state != 1:
    print('-----Scheduler started-----')
    scheduler.start()

def job_executed(event): 
    job_id = str(event.job_id).capitalize()
    print(f'\n{job_id} was executed successfully at {event.scheduled_run_time}, response: {event.retval}')
    
def job_error(event):
    job_id = str(event.job_id).capitalize()
    print(f'\nAn error occured in {job_id}, response: {event.retval}')
   
def job_max_instances_reached(event): 
    job_id = str(event.job_id).capitalize()
    print(f'Maximum number of running instances reached, *Upgrade* the time interval for {job_id}')
  

   
scheduler.add_listener(job_error, EVENT_JOB_ERROR)
scheduler.add_listener(job_max_instances_reached, EVENT_JOB_MAX_INSTANCES)
scheduler.add_listener(job_executed, EVENT_JOB_EXECUTED)