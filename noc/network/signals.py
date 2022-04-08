# from django.contrib.auth.models import User
# from django.db.models.signals import post_save, pre_save
# from django.dispatch import receiver
# from .models import Vlan, Switch, VlanHistory, SwitchHistory
#
#
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
#     VlanHistory.objects.create(vlan_user=User.objects.get(username=request.user),
#                                vlan_name=Vlan.objects.get(vlan_name=instance.vlan_name),
#                                vlan_client=instance.vlan_client, vlan_order=instance.vlan_order,
#                                vlan_used_for=instance.vlan_used_for, vlan_point_a=instance.vlan_point_a,
#                                vlan_point_b=instance.vlan_point_b, vlan_speed=instance.vlan_speed,
#                                vlan_note=instance.vlan_note, vlan_time=instance.vlan_time)
#
#
# @receiver(post_save, sender=Switch)
# def switch_history(sender, instance, **kwargs):
#     import inspect
#     for frame_record in inspect.stack():
#         if frame_record[3] == 'get_response':
#             request = frame_record[0].f_locals['request']
#             break
#     else:
#         request = None
#
#     SwitchHistory.objects.create(switch_user=User.objects.get(username=request.user),
#                                  switch_order=Switch.objects.get(switch_order=instance.switch_order),
#                                  switch_address=instance.switch_address, switch_ip=instance.switch_ip,
#                                  switch_mac=instance.switch_mac, switch_model=instance.switch_model,
#                                  switch_firmware=instance.switch_firmware, switch_serial=instance.switch_serial,
#                                  switch_note=instance.switch_note, switch_time=instance.switch_time)
