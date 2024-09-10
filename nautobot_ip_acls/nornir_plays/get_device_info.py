"""Nornir tasks for getting device info."""
from datetime import datetime

from nautobot_plugin_nornir.constants import NORNIR_SETTINGS
from nornir import InitNornir
from nornir.core.task import Result
from nautobot.extras.models import Status
from netutils.ping import tcp_ping
from nornir_netmiko.tasks import netmiko_send_command
from nornir.core.plugins.inventory import InventoryPluginRegister

from nautobot_plugin_nornir.plugins.inventory.nautobot_orm import NautobotORMInventory

InventoryPluginRegister.register("nautobot-inventory", NautobotORMInventory)


import logging
import json


# Create Logger
logger = logging.getLogger(__name__)


def run_get_facts(task, logger):
    """Run the napalm get_facts for a device and store the information in the DiffSync adapter."""
    obj = task.host.data["obj"]
    port = 22
    logger.debug(f"Getting device info for {obj} {obj.primary_ip4}...")
    if tcp_ping(obj.primary_ip4.host, port):
        results = task.run(task=netmiko_send_command, command_string="show version", use_textfsm=True)

        if results[0].failed:
            return results
        output = results[0].result[0]
        logger.debug(
            f"Show version: {output['running_image']}",
        )
        # Loop through each task result for this host
        for task_result in results:
            print(f"Task: {task_result.name}")
            print(f"Result: {task_result.result}")
            print(f"Failed: {task_result.failed}")
            print(f"Changed: {task_result.changed}")
        return Result(host=task.host, result=output)

    else:
        if obj.status.name != "Inventory":
            logger.debug(
                f"Device {obj} is unreachable and Status in Nautobot is {obj.status}.Changing status to offline..",
            )
            obj.status = Status.objects.get(name="Offline")
            obj.validated_save()

        else:
            logger.debug(
                f"Device {obj} is unreachable and Status in Nautobot is {obj.status}.Skiping changing status..",
            )


def get_device_info(job, devices):
    """Get all device info via Nornir."""
    now = datetime.now()
    with InitNornir(
        runner=NORNIR_SETTINGS.get("runner"),
        logging={"enabled": False},
        inventory={
            "plugin": "nautobot-inventory",
            "options": {
                "credentials_class": NORNIR_SETTINGS.get("credentials"),
                "params": NORNIR_SETTINGS.get("inventory_params"),
                "queryset": devices,
                "defaults": {"now": now},
            },
        },
    ) as nornir_obj:
        results = nornir_obj.run(task=run_get_facts, name="GET DEVICE FACTS", logger=logger)
        logger.debug("Completed getting info from devices.")
        for host, multi_result in results.items():
            print(f"Host: {host}")
            
            # Loop through each task result for this host
            for task_result in multi_result:
                print(f"Task: {task_result.name}")
                print(f"Result: {task_result.result}")
                print(f"Failed: {task_result.failed}")
                print(f"Changed: {task_result.changed}")
