from crontab import CronTab

cmds = 'python3 /home/pi/KiosSehat/logger_kiossehat.py'

def removeJob(user_id, comment_id):
    my_cron = CronTab(user=user_id)
    for job in my_cron:
        if job.comment == comment_id:
            my_cron.remove(job)
            my_cron.write()

def createJob(user_id, comment_id,hour_every,hour_everyset, cmds):
    my_cron = CronTab(user=user_id)
    jobCommentList = []
    for job in my_cron:
        if job.comment == comment_id:
            print("You have include the cronJob")
        jobCommentList.append(job.comment())

    if comment_id not in jobCommentList:
        job = my_cron.new(, comment = comment_id)

def updateJob_On_Zero(hour_on, hour_onset,hour_every, hour_everyset,comment_id):
    my_cron = CronTab(user=user_id)
    for job in my_cron:
        if job.comment == comment_id:
            if hour_on == True:
                job.hour.on(hour_onset)
                job.minute.on(0)
                my_cron.write()
            elif hour_every == True:
                job.hour.every(hour_everyset)
                job.minute.on(0)
                my_cron.write()


job = my_cron.new(command='python3 /home/pi/KiosSehat/logger_kiossehat.py', comment = comment_id)
job.hour.every(17)
job.
