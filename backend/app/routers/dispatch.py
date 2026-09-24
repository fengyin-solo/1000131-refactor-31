"""调度派单接口：维护调度单，覆盖确认派单、确认发车、撤销派单等动作。"""
from __future__ import annotations

from app.modules import get_spec
from app.routers.factory import build_router

# 接口结构由 app.routers.factory 按模块声明统一生成，本文件只负责装配。
router = build_router(get_spec("dispatch"))
