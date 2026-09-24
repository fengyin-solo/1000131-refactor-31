"""计费结算业务规则：状态流转、字段校验与筛选口径都收在这里。"""
from __future__ import annotations

from app.services.base import ModuleService, ModuleSpec

spec = ModuleSpec(
    module='billing',
    entity_label='计费单',
    domain_label='计费结算',
    required_fields=['计费单号', '客户名称', '计费周期'],
    status_order=['待核算', '已核算', '已对账', '已开票'],
    action_rules={'生成账单': '已核算', '确认对账': '已对账', '开具发票': '已开票'},
    negative_actions=[],
)


class BillingService(ModuleService):
    def __init__(self) -> None:
        super().__init__(spec)
