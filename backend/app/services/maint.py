"""维保工单业务规则：状态流转、字段校验与筛选口径都收在这里。"""
from __future__ import annotations

from app.services.base import ModuleService, ModuleSpec

spec = ModuleSpec(
    module='maint',
    entity_label='维保工单',
    domain_label='维保工单',
    required_fields=['工单编号', '关联设备', '故障现象'],
    status_order=['待受理', '处理中', '待验收', '已关闭'],
    action_rules={'受理工单': '处理中', '派工处理': '处理中', '关闭工单': '已关闭'},
    negative_actions=[],
)


class MaintService(ModuleService):
    def __init__(self) -> None:
        super().__init__(spec)
