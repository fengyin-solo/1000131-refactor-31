"""计费结算接口：维护计费单，覆盖生成账单、确认对账、开具发票等动作。"""
from __future__ import annotations

from app.modules import get_spec
from app.routers.factory import build_router

# 接口结构由 app.routers.factory 按模块声明统一生成，本文件只负责装配。
router = build_router(get_spec("billing"))
