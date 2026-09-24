"""冷藏车管理业务规则：状态流转、字段校验与筛选口径都收在这里。"""
from __future__ import annotations

from app.services.base import ModuleService, ModuleSpec

spec = ModuleSpec(
    module='vehicle',
    entity_label='冷藏车辆',
    domain_label='冷藏车管理',
    required_fields=['车牌号码', '车辆类型', '制冷机组型号'],
    status_order=['可用', '出车中', '维修中', '已停用'],
    action_rules={'安排出车': '出车中', '回场登记': '可用', '停用车辆': '已停用'},
    negative_actions=['停用车辆'],
)


class VehicleService(ModuleService):
    def __init__(self) -> None:
        super().__init__(spec)
