"""温控设备接口：维护温控设备，覆盖登记设备、提交校准、报废设备等动作。"""
from __future__ import annotations

from app.modules import get_spec
from app.routers.factory import build_router

# 接口结构由 app.routers.factory 按模块声明统一生成，本文件只负责装配。
router = build_router(get_spec("device"))
