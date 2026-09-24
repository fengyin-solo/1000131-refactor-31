"""维保工单接口：维护维保工单，覆盖受理工单、派工处理、关闭工单等动作。"""
from __future__ import annotations

from app.modules import get_spec
from app.routers.factory import build_router

# 接口结构由 app.routers.factory 按模块声明统一生成，本文件只负责装配。
router = build_router(get_spec("maint"))
