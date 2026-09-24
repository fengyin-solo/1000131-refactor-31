"""批次追溯业务声明：必填字段、状态序列与动作映射在 app.modules 中统一登记。

清单读取（筛选/分页）、必填校验与动作判定不再在本模块重复实现，
统一由 app.services.base.ModuleService 按声明执行；改口径只需改 modules.py。
"""
from __future__ import annotations

from app.modules import get_spec
from app.services.base import ModuleService

MODULE = "trace"

# 模块声明（必填字段 / 状态序列 / 动作映射）集中在 app.modules.MODULE_SPECS。
SPEC = get_spec(MODULE)
REQUIRED_FIELDS = list(SPEC.required_fields)
STATUS_ORDER = list(SPEC.status_order)
ACTION_RULES = dict(SPEC.action_rules)
NEGATIVE_ACTIONS = list(SPEC.negative_actions)

# 共用服务实例；需要定制口径时再在此模块扩展 ModuleService。
service = ModuleService(SPEC)
