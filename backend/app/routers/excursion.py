"""温度异常接口：维护温度异常事件，覆盖受理事件、提交处置、忽略事件等动作。"""
from __future__ import annotations

from app.modules import get_spec
from app.routers.factory import build_router

# 接口结构由 app.routers.factory 按模块声明统一生成，本文件只负责装配。
router = build_router(get_spec("excursion"))
