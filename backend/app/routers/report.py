"""报表导出接口：维护报表任务，覆盖生成报表、重试任务、下载报表等动作。"""
from __future__ import annotations

from app.modules import get_spec
from app.routers.factory import build_router

# 接口结构由 app.routers.factory 按模块声明统一生成，本文件只负责装配。
router = build_router(get_spec("report"))
