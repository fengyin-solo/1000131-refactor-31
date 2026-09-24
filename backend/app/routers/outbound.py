"""出库管理接口：维护出库单，覆盖确认拣货、安排发运、取消出库等动作。"""
from __future__ import annotations

from app.modules import get_spec
from app.routers.factory import build_router

# 接口结构由 app.routers.factory 按模块声明统一生成，本文件只负责装配。
router = build_router(get_spec("outbound"))
