"""库存管理接口：维护库存批次，覆盖冻结库存、解冻库存、盘点修正等动作。"""
from __future__ import annotations

from app.modules import get_spec
from app.routers.factory import build_router

# 接口结构由 app.routers.factory 按模块声明统一生成，本文件只负责装配。
router = build_router(get_spec("inventory"))
