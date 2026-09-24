"""入库管理接口：维护入库单，覆盖确认收货、安排上架、退回入库等动作。"""
from __future__ import annotations

from app.modules import get_spec
from app.routers.factory import build_router

# 接口结构由 app.routers.factory 按模块声明统一生成，本文件只负责装配。
router = build_router(get_spec("inbound"))
