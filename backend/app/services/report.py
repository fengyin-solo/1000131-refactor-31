"""报表导出业务规则：状态流转、字段校验与筛选口径都收在这里。"""
from __future__ import annotations

from app.services.base import ModuleService, ModuleSpec

spec = ModuleSpec(
    module='report',
    entity_label='报表任务',
    domain_label='报表导出',
    required_fields=['报表名称', '统计范围', '统计周期'],
    status_order=['排队中', '生成中', '已完成', '已失败'],
    action_rules={'生成报表': '生成中', '重试任务': '排队中', '下载报表': '已完成'},
    negative_actions=[],
)


class ReportService(ModuleService):
    def __init__(self) -> None:
        super().__init__(spec)
