"""温控设备业务规则：状态流转、字段校验与筛选口径都收在这里。"""
from __future__ import annotations

from app.services.base import ModuleService, ModuleSpec

spec = ModuleSpec(
    module='device',
    entity_label='温控设备',
    domain_label='温控设备',
    required_fields=['设备编号', '设备名称', '设备型号'],
    status_order=['在用', '待校准', '故障', '已报废'],
    action_rules={'登记设备': '在用', '提交校准': '待校准', '报废设备': '已报废'},
    negative_actions=[],
)


class DeviceService(ModuleService):
    def __init__(self) -> None:
        super().__init__(spec)
