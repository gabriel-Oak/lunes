from typing import Any, Dict

class IotStatus:
  def __init__(self, status: Dict[str, str]) -> None:
    self.code: str = status['code']
    self.value: str = status['value']