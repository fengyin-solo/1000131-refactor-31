"""告警中心业务规则：状态流转、字段校验与筛选口径都收在这里。"""
from __future__ import annotations

from app.services.base import ModuleService, ModuleSpec

spec = ModuleSpec(
    module='alarm',
    entity_label='告警事件',
    domain_label='告警中心',
    required_fields=['告警编号', '告警类型', '告警等级'],
    status_order=['待确认', '已确认', '已处置', '已忽略'],
    action_rules={'确认告警': '已确认', '处置告警': '已处置', '忽略告警': '已忽略'},
    negative_actions=['忽略告警'],
)


class AlarmService(ModuleService):
    def __init__(self) -> None:
        super().__init__(spec)
