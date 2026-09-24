"""客户管理业务规则：状态流转、字段校验与筛选口径都收在这里。"""
from __future__ import annotations

from app.services.base import ModuleService, ModuleSpec

spec = ModuleSpec(
    module='customer',
    entity_label='客户档案',
    domain_label='客户管理',
    required_fields=['客户编码', '客户名称', '客户类型'],
    status_order=['待审核', '合作中', '已暂停', '已终止'],
    action_rules={'审核客户': '合作中', '暂停合作': '已暂停', '终止合作': '已终止'},
    negative_actions=[],
)


class CustomerService(ModuleService):
    def __init__(self) -> None:
        super().__init__(spec)
