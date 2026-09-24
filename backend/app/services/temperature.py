"""温控监控业务规则：状态流转、字段校验与筛选口径都收在这里。"""
from __future__ import annotations

from app.services.base import ModuleService, ModuleSpec

spec = ModuleSpec(
    module='temperature',
    entity_label='温控记录',
    domain_label='温控监控',
    required_fields=['记录编号', '关联运单', '测点编号'],
    status_order=['正常', '偏高', '偏低', '已离线'],
    action_rules={'确认记录': '正常', '标记超限': '偏高', '重新采集': '正常'},
    negative_actions=[],
)


class TemperatureService(ModuleService):
    def __init__(self) -> None:
        super().__init__(spec)
