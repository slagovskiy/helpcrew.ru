from django.utils import timezone
import datetime
from holidays import HolidayBase
import businesstimedelta

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'test'

    def handle(self, **options):
        from ....helpdesk.models import CrewTask, Crew
        t = CrewTask.objects.all()[0]
        working_days = []
        if t.crew.work_day_0:
            working_days.append(0)
        if t.crew.work_day_1:
            working_days.append(1)
        if t.crew.work_day_2:
            working_days.append(2)
        if t.crew.work_day_3:
            working_days.append(3)
        if t.crew.work_day_4:
            working_days.append(4)
        if t.crew.work_day_5:
            working_days.append(5)
        if t.crew.work_day_6:
            working_days.append(6)

        print(working_days)

        workday = businesstimedelta.WorkDayRule(
            start_time=datetime.time(t.crew.work_start_time),
            end_time=datetime.time(t.crew.work_end_time),
            working_days=working_days,
            tz=timezone.get_current_timezone()
        )
        print(workday.start_time)
        print(workday.end_time)

        lunchbreak = businesstimedelta.LunchTimeRule(
            start_time=datetime.time(t.crew.launch_start_time),
            end_time=datetime.time(t.crew.launch_end_time),
            working_days=working_days,
            tz=timezone.get_current_timezone()
        )
        print(lunchbreak.start_time)
        print(lunchbreak.end_time)

        holidays = HolidayBase()
        btd = None

        if t.crew.holidays:
            holidays.append(t.crew.holidays.split('\n'))
            btd = businesstimedelta.Rules([workday, lunchbreak, holidays])
        else:
            btd = businesstimedelta.Rules([workday, lunchbreak])

        date_in = t.date_in
        delta = None
        if t.service:
            delta = businesstimedelta.BusinessTimeDelta(btd, hours=t.service.time2)
        else:
            delta = businesstimedelta.BusinessTimeDelta(btd, hours=t.crew.incident_time_two)
        print(delta)
        print(date_in)
        print(date_in + delta)
