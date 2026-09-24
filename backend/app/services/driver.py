"""司机管理业务规则：状态流转、字段校验与筛选口径都收在这里。"""
from __future__ import annotations

from app.services.base import ModuleService, ModuleSpec

spec = ModuleSpec(
    module='driver',
    entity_label='司机档案',
    domain_label='司机管理',
    required_fields=['司机工号', '司机姓名', '联系电话'],
    status_order=['待上岗', '在岗', '休息中', '已离职'],
    action_rules={'安排上岗': '在岗', '排班休息': '休息中', '办理离职': '已离职'},
    negative_actions=[],
)


class DriverService(ModuleService):
    def __init__(self) -> None:
        super().__init__(spec)
