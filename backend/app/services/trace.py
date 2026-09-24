"""批次追溯业务规则：状态流转、字段校验与筛选口径都收在这里。"""
from __future__ import annotations

from app.services.base import ModuleService, ModuleSpec

spec = ModuleSpec(
    module='trace',
    entity_label='追溯记录',
    domain_label='批次追溯',
    required_fields=['追溯码', '货物名称', '生产批次'],
    status_order=['待关联', '已关联', '已发布', '已撤回'],
    action_rules={'关联上游': '已关联', '发布追溯': '已发布', '撤回追溯': '已撤回'},
    negative_actions=[],
)


class TraceService(ModuleService):
    def __init__(self) -> None:
        super().__init__(spec)
