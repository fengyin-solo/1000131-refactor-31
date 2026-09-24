"""出库管理业务规则：状态流转、字段校验与筛选口径都收在这里。"""
from __future__ import annotations

from app.services.base import ModuleService, ModuleSpec

spec = ModuleSpec(
    module='outbound',
    entity_label='出库单',
    domain_label='出库管理',
    required_fields=['出库单号', '客户名称', '货物名称'],
    status_order=['待拣货', '已拣货', '已发运', '已取消'],
    action_rules={'确认拣货': '已拣货', '安排发运': '已发运', '取消出库': '已取消'},
    negative_actions=[],
)


class OutboundService(ModuleService):
    def __init__(self) -> None:
        super().__init__(spec)
