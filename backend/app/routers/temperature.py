"""温控监控接口：维护温控记录，覆盖确认记录、标记超限、重新采集等动作。"""
from __future__ import annotations

from app.modules import get_spec
from app.routers.factory import build_router

# 接口结构由 app.routers.factory 按模块声明统一生成，本文件只负责装配。
router = build_router(get_spec("temperature"))
