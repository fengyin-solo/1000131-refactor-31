"""运单管理业务规则：状态流转、字段校验与筛选口径都收在这里。"""
from __future__ import annotations

from app.services.base import ModuleService, ModuleSpec

spec = ModuleSpec(
    module='waybill',
    entity_label='冷链运单',
    domain_label='运单管理',
    required_fields=['运单号', '关联订单', '承运车辆'],
    status_order=['待装车', '运输中', '已签收', '已作废'],
    action_rules={'确认装车': '运输中', '签收运单': '已签收', '作废运单': '已作废'},
    negative_actions=['作废运单'],
)


class WaybillService(ModuleService):
    def __init__(self) -> None:
        super().__init__(spec)
