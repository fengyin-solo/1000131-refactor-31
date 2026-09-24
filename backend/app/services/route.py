"""线路管理业务规则：状态流转、字段校验与筛选口径都收在这里。"""
from __future__ import annotations

from app.services.base import ModuleService, ModuleSpec

spec = ModuleSpec(
    module='route',
    entity_label='配送线路',
    domain_label='线路管理',
    required_fields=['线路编码', '线路名称', '起点冷库'],
    status_order=['草稿', '已启用', '已停用'],
    action_rules={'启用线路': '已启用', '调整站点': '草稿', '停用线路': '已停用'},
    negative_actions=['停用线路'],
)


class RouteService(ModuleService):
    def __init__(self) -> None:
        super().__init__(spec)
