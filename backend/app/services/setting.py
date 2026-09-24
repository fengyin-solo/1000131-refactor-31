"""系统设置业务规则：状态流转、字段校验与筛选口径都收在这里。"""
from __future__ import annotations

from app.services.base import ModuleService, ModuleSpec

spec = ModuleSpec(
    module='setting',
    entity_label='系统参数',
    domain_label='系统设置',
    required_fields=['参数编码', '参数名称', '参数值'],
    status_order=['已生效', '待生效', '已回滚'],
    action_rules={'修改参数': '待生效', '回滚参数': '已回滚', '生效参数': '已生效'},
    negative_actions=['回滚参数'],
)


class SettingService(ModuleService):
    def __init__(self) -> None:
        super().__init__(spec)
