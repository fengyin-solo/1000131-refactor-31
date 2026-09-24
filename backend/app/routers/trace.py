"""批次追溯接口：维护追溯记录，覆盖关联上游、发布追溯、撤回追溯等动作。"""
from __future__ import annotations

from app.modules import get_spec
from app.routers.factory import build_router

# 接口结构由 app.routers.factory 按模块声明统一生成，本文件只负责装配。
router = build_router(get_spec("trace"))
