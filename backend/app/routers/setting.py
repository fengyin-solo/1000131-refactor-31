"""系统设置接口：维护系统参数，覆盖修改参数、回滚参数、生效参数等动作。"""
from __future__ import annotations

from app.modules import get_spec
from app.routers.factory import build_router

# 接口结构由 app.routers.factory 按模块声明统一生成，本文件只负责装配。
router = build_router(get_spec("setting"))
