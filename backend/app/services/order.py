"""冷链订单业务规则：状态流转、字段校验与筛选口径都收在这里。"""
from __future__ import annotations

from app.services.base import ModuleService, ModuleSpec

spec = ModuleSpec(
    module='order',
    entity_label='冷链订单',
    domain_label='冷链订单',
    required_fields=['订单编号', '客户名称', '货物名称'],
    status_order=['待受理', '已受理', '已调度', '已完结', '已取消'],
    action_rules={'受理订单': '已受理', '调度派车': '已调度', '取消订单': '已取消'},
    negative_actions=[],
)


class OrderService(ModuleService):
    def __init__(self) -> None:
        super().__init__(spec)
