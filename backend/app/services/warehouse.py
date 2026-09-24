"""冷库管理业务规则：状态流转、字段校验与筛选口径都收在这里。"""
from __future__ import annotations

from app.services.base import ModuleService, ModuleSpec

spec = ModuleSpec(
    module='warehouse',
    entity_label='冷库档案',
    domain_label='冷库管理',
    required_fields=['冷库编码', '冷库名称', '库区温区'],
    status_order=['已启用', '检修中', '已停用'],
    action_rules={'启用冷库': '已启用', '安排检修': '检修中', '停用冷库': '已停用'},
    negative_actions=['停用冷库'],
)


class WarehouseService(ModuleService):
    def __init__(self) -> None:
        super().__init__(spec)
