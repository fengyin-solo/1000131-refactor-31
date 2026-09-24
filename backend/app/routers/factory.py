"""各业务模块接口的共用装配。

改造前 21 个 router 的接口结构完全一致，只有前缀、分组名、字段与文案差异；
现在差异全部来自 :class:`~app.modules.ModuleSpec`，本工厂按统一模板生成：

- ``GET    /api/<name>``          关键字 + 状态筛选 + 分页
- ``GET    /api/<name>/{id}``     单条明细
- ``POST   /api/<name>``          登记（缺字段返回原因）
- ``POST   /api/<name>/{id}/actions`` 执行动作
- ``GET    /api/<name>/export``   全量导出

路由声明顺序、状态码（size>200 返回 400、明细不存在返回 404）、
响应模型与接口文档文案均与改造前保持一致。
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query

from app.modules import ModuleSpec
from app.schemas import ActionResult, EntryPayload, PageResult
from app.services.base import ModuleService

MAX_PAGE_SIZE = 200
EXPORT_PAGE_SIZE = 10000


def build_router(spec: ModuleSpec) -> APIRouter:
    """按模块声明生成一组与旧接口等价的路由。"""
    service = ModuleService(spec)
    action_names = "、".join(spec.action_rules)
    status_hint = "、".join(spec.status_order)

    router = APIRouter(prefix=f"/api/{spec.name}", tags=[spec.label])

    @router.get("", response_model=PageResult[dict])
    def list_entries(
        keyword: str | None = Query(default=None, description=f"按{spec.keyword_field}检索"),
        status: str | None = Query(default=None, description=status_hint),
        page: int = 1,
        size: int = 20,
    ) -> PageResult[dict]:
        if size > MAX_PAGE_SIZE:
            raise HTTPException(status_code=400, detail="每页最多 200 条，请缩小分页范围")
        items, total = service.list_entries(keyword=keyword, status=status, page=page, size=size)
        return PageResult(items=items, total=total, page=page, size=size)

    @router.get("/{entry_id}", response_model=dict)
    def get_entry(entry_id: int) -> dict:
        entry = service.get_entry(entry_id)
        if entry is None:
            raise HTTPException(status_code=404, detail=f"{spec.entity} {entry_id} 不存在或已归档")
        return entry

    @router.post("", response_model=ActionResult)
    def create_entry(payload: EntryPayload) -> ActionResult:
        entry, missing = service.create_entry(payload.values)
        if missing:
            return ActionResult(ok=False, message=f"缺少必填字段：{'、'.join(missing)}")
        return ActionResult(ok=True, message=f"{spec.entity}已登记", entry=entry)

    @router.post("/{entry_id}/actions", response_model=ActionResult)
    def run_action(entry_id: int, payload: EntryPayload) -> ActionResult:
        action = str(payload.values.get("action") or "").strip()
        entry, message = service.run_action(entry_id, action)
        if entry is None:
            return ActionResult(ok=False, message=message)
        return ActionResult(ok=True, message=message, entry=entry)

    @router.get("/export")
    def export_entries() -> dict[str, Any]:
        items, total = service.list_entries(page=1, size=EXPORT_PAGE_SIZE)
        return {"module": spec.name, "total": total, "items": items}

    # 接口文档（/docs）文案与改造前逐字一致。
    list_entries.__doc__ = (
        f"按{spec.keyword_field}与状态过滤{spec.label}列表；没有数据时返回空页，不报错。"
    )
    get_entry.__doc__ = f"读取单条{spec.entity}明细；不存在时给出可读的错误说明。"
    create_entry.__doc__ = f"登记一条{spec.entity}，缺字段时说明原因而不是静默丢弃。"
    run_action.__doc__ = (
        f"对单条{spec.entity}执行{action_names}；不允许的动作会被拦下并说明原因。"
    )
    export_entries.__doc__ = f"导出{spec.label}清单：返回当前过滤条件下的全量数据。"

    return router
