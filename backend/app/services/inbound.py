"""入库管理业务规则：状态流转、字段校验与筛选口径都收在这里。"""
from __future__ import annotations

from app.services.base import ModuleService, ModuleSpec

spec = ModuleSpec(
    module='inbound',
    entity_label='入库单',
    domain_label='入库管理',
    required_fields=['入库单号', '供应商名称', '货物名称'],
    status_order=['待收货', '已收货', '已上架', '已退回'],
    action_rules={'确认收货': '已收货', '安排上架': '已上架', '退回入库': '已退回'},
    negative_actions=[],
)


class InboundService(ModuleService):
    def __init__(self) -> None:
        super().__init__(spec)
