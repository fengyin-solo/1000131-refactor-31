"""运单管理接口：维护冷链运单，覆盖确认装车、签收运单、作废运单等动作。"""
from __future__ import annotations

from app.modules import get_spec
from app.routers.factory import build_router

# 接口结构由 app.routers.factory 按模块声明统一生成，本文件只负责装配。
router = build_router(get_spec("waybill"))
