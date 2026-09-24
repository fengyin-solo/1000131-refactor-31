"""温度异常业务规则：状态流转、字段校验与筛选口径都收在这里。"""
from __future__ import annotations

from app.services.base import ModuleService, ModuleSpec

spec = ModuleSpec(
    module='excursion',
    entity_label='温度异常事件',
    domain_label='温度异常',
    required_fields=['事件编号', '关联运单', '异常类型'],
    status_order=['待处置', '处置中', '已闭环', '已忽略'],
    action_rules={'受理事件': '处置中', '提交处置': '已闭环', '忽略事件': '已忽略'},
    negative_actions=['忽略事件'],
)


class ExcursionService(ModuleService):
    def __init__(self) -> None:
        super().__init__(spec)
