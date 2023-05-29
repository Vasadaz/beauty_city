import datetime
import datetime as dt

from django.core.management.base import BaseCommand

from beauty_shop.models import Master, TimeSlot


def create_time_slots(master: Master, time_slots: list[datetime.datetime]):
    #master.time_slots.all().delete()

    for time_slot_at in time_slots:
        if not master.time_slots.all():
            pass
        elif master.time_slots.last().time_slot_at >= time_slot_at:
            continue

        time_slot_obj = TimeSlot(
            master=master,
            time_slot_at=time_slot_at,
        )
        time_slot_obj.save()


def main():
    # Временной слот равен 30 минутам, поэтому необходимо указать
    # целочисленный значения времени в 24м формате начала рабочего дня и конец.
    start_work_day = 8
    end_work_day = 20
    time_slots_count = (end_work_day - start_work_day) * 2
    time_slots = []
    day_count = 10

    for day_num in range(1, day_count + 1):
        future_time_slots_at = dt.datetime.today() + dt.timedelta(days=day_num)
        future_time_slots_at = future_time_slots_at.replace(
            hour=start_work_day,
            minute=0,
            second=0,
            microsecond=0,
        )

        for time_slot_num in range(time_slots_count):
            time_slots.append(future_time_slots_at)
            future_time_slots_at += dt.timedelta(minutes=30)

    for master in Master.objects.all():
        create_time_slots(master, time_slots)


class Command(BaseCommand):
    help = 'Start creating timeslots'

    def handle(self, *args, **options):
        main()
