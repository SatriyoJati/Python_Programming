from crontab import CronTab

cron = CronTab(user = 'root')

cron = CronTab(tabfile ='BLEReset.tab')

job= cron.new(command='sudo reboot', comment='dateinfo')
job.hour.every(7)
job.hour.every(12)
job.hour.every(17)
cron.write()

iter1 = cron.find_command('comment')

for item in iter1:
    print(item)
