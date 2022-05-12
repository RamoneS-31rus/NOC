# from django.contrib.auth.models import User
# from django.db.models.signals import post_save, pre_save
# from django.dispatch import receiver
# from .models import Vlan, Switch, VlanHistory, SwitchHistory


# @receiver(post_save, sender=Vlan)
# def vlan_history(sender, instance, **kwargs):
#     import inspect
#     for frame_record in inspect.stack():
#         if frame_record[3] == 'get_response':
#             request = frame_record[0].f_locals['request']
#             break
#     else:
#         request = None
#
    # VlanHistory.objects.create(number=instance.number, client=instance.client, used_for=instance.used_for,
    #                            point_a=instance.point_a, point_b=instance.point_b, order=instance.order,
    #                            speed=instance.speed, note=instance.note, user=instance.user, date=instance.date
    #                            )


# @receiver(post_save, sender=Switch)
# def switch_history(sender, instance, **kwargs):
#     # import inspect
#     # for frame_record in inspect.stack():
#     #     if frame_record[3] == 'get_response':
#     #         request = frame_record[0].f_locals['request']
#     #         break
#     # else:
#     #     request = None
#
#     SwitchHistory.objects.create(
#         order=instance.order, address=instance.address, ip=instance.ip, mac=instance.mac, model=instance.model,
#         firmware=instance.firmware, serial=instance.serial, note=instance.note, user=instance.user, date=instance.date
#     )
