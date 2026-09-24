"""质检管理业务规则：状态流转、字段校验与筛选口径都收在这里。"""
from __future__ import annotations

from app.services.base import ModuleService, ModuleSpec

spec = ModuleSpec(
    module='quality',
    entity_label='质检单',
    domain_label='质检管理',
    required_fields=['质检单号', '关联批次', '检测项目'],
    status_order=['待检测', '检测中', '合格', '不合格'],
    action_rules={'开始检测': '检测中', '判定合格': '合格', '判定不合格': '不合格'},
    negative_actions=[],
)


class QualityService(ModuleService):
    def __init__(self) -> None:
        super().__init__(spec)
