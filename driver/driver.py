import asyncio

import neohubapi.neohub as neohub


async def run():
    # Legacy connection
    # hub = neohub.NeoHub()
    # Or, for a websocket connection:
    hub = neohub.NeoHub(
        host="192.168.1.152", port=4243, token="2aff3cc3-59f3-46b4-98dc-6ede5c1ee03c"
    )
    # system = await hub.get_system()
    hub_data = await hub.get_devices_data()
    devices = hub_data["neo_devices"]
    for device in devices:
        print(f"Temperature in zone {device.name}: {device.temperature}")
        print(f"Is zone {device.name} stsading by?: {device.standby}")
        await device.identify()


asyncio.run(run())
