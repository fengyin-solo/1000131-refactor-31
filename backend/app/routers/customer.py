"""客户管理接口：维护客户档案，覆盖审核客户、暂停合作、终止合作等动作。"""
from __future__ import annotations

from app.modules import get_spec
from app.routers.factory import build_router

# 接口结构由 app.routers.factory 按模块声明统一生成，本文件只负责装配。
router = build_router(get_spec("customer"))
