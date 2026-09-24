"""库存管理业务规则：状态流转、字段校验与筛选口径都收在这里。"""
from __future__ import annotations

from app.services.base import ModuleService, ModuleSpec

spec = ModuleSpec(
    module='inventory',
    entity_label='库存批次',
    domain_label='库存管理',
    required_fields=['库存编码', '货物名称', '批次号'],
    status_order=['正常', '临近保质期', '已冻结', '已清空'],
    action_rules={'冻结库存': '已冻结', '解冻库存': '正常', '盘点修正': '正常'},
    negative_actions=[],
)


class InventoryService(ModuleService):
    def __init__(self) -> None:
        super().__init__(spec)
