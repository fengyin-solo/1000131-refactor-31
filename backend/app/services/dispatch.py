"""调度派单业务规则：状态流转、字段校验与筛选口径都收在这里。"""
from __future__ import annotations

from app.services.base import ModuleService, ModuleSpec

spec = ModuleSpec(
    module='dispatch',
    entity_label='调度单',
    domain_label='调度派单',
    required_fields=['调度单号', '关联订单', '配送线路'],
    status_order=['待派单', '已派单', '已发车', '已撤销'],
    action_rules={'确认派单': '已派单', '确认发车': '已发车', '撤销派单': '已撤销'},
    negative_actions=['撤销派单'],
)


class DispatchService(ModuleService):
    def __init__(self) -> None:
        super().__init__(spec)
