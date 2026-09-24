"""告警中心接口：维护告警事件，覆盖确认告警、处置告警、忽略告警等动作。"""
from __future__ import annotations

from app.modules import get_spec
from app.routers.factory import build_router

# 接口结构由 app.routers.factory 按模块声明统一生成，本文件只负责装配。
router = build_router(get_spec("alarm"))
