from modules.iot.iot_status import IotStatus
from typing import Any, Dict, List


class IotDevice:
  def __init__(self, device: Dict[str, Any]) -> None:
    self.active_time: int = device['active_time']
    self.biz_type: int = device['biz_type']
    self.category: str = device['category']
    self.create_time: int = device['create_time']
    self.icon: str = device['icon']
    self.id: str = device['id']
    self.ip: str = device['ip']
    self.lat: str = device['lat']
    self.lon: str = device['lon']
    self.local_key: str = device['local_key']
    self.name: str = device['name']
    self.online: bool = device['online']
    self.owner_id: str = device['owner_id']
    self.product_id: str = device['product_id']
    self.product_name: str = device['product_name']
    self.status: List[IotStatus] = list(map(lambda item: IotStatus(item), device['status']))
    self.sub: bool = device['sub']
    self.time_zone: str = device['time_zone']
    self.uid: str = device['uid']
    self.update_time: str = device['update_time']
    self.uuid: str = device['uuid']