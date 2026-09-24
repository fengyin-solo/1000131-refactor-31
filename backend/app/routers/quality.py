"""质检管理接口：维护质检单，覆盖开始检测、判定合格、判定不合格等动作。"""
from __future__ import annotations

from app.modules import get_spec
from app.routers.factory import build_router

# 接口结构由 app.routers.factory 按模块声明统一生成，本文件只负责装配。
router = build_router(get_spec("quality"))
