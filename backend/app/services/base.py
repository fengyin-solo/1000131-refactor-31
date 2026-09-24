"""各业务模块共用的服务实现：清单读取、必填校验、动作判定收拢到这里。

改造前这些逻辑在 21 个 service 里逐字重复；现在各模块只通过
:class:`~app.modules.ModuleSpec` 声明必填字段、状态序列与动作映射，
``ModuleService`` 按同一份口径执行：

- 清单读取：关键字匹配 ``spec.keyword_field``，再按 ``status`` 精确过滤，最后分页；
- 必填校验：``spec.required_fields`` 里去空白后为空即视为缺失，按声明顺序返回；
- 动作判定：动作必须在 ``spec.action_rules`` 内、目标状态必须在
  ``spec.status_order`` 内，随后统一写入 status / pending / abnormal。

返回约定保持改造前不变：
``(entry, missing)`` / ``(entry, message)``，失败时首项为 ``None``。
"""
from __future__ import annotations

from typing import Any

from app.modules import ModuleSpec
from app.store import store


class ModuleService:
    """声明驱动的通用业务服务；一个模块实例化一份。"""

    def __init__(self, spec: ModuleSpec) -> None:
        self.spec = spec
        self.module = spec.name

    # ---- 清单读取 -------------------------------------------------------

    def list_entries(
        self,
        *,
        keyword: str | None = None,
        status: str | None = None,
        page: int = 1,
        size: int = 20,
    ) -> tuple[list[dict[str, Any]], int]:
        rows = store.rows(self.module)
        if keyword:
            field = self.spec.keyword_field
            rows = [row for row in rows if keyword in str(row.get(field, ""))]
        if status:
            rows = [row for row in rows if row.get("status") == status]
        total = len(rows)
        start = max(page - 1, 0) * size
        return rows[start:start + size], total

    def get_entry(self, entry_id: int) -> dict[str, Any] | None:
        return store.find(self.module, entry_id)

    # ---- 必填校验与登记 -------------------------------------------------

    def create_entry(self, values: dict[str, Any]) -> tuple[dict[str, Any] | None, list[str]]:
        missing = [
            field
            for field in self.spec.required_fields
            if not str(values.get(field) or "").strip()
        ]
        if missing:
            return None, missing
        rows = store.rows(self.module)
        entry: dict[str, Any] = {
            "id": max((int(row.get("id", 0)) for row in rows), default=0) + 1
        }
        entry.update({field: values.get(field) for field in self.spec.required_fields})
        entry["status"] = self.spec.status_order[0]
        entry["pending"] = True
        entry["abnormal"] = False
        rows.append(entry)
        return entry, []

    # ---- 动作判定 -------------------------------------------------------

    def run_action(self, entry_id: int, action: str) -> tuple[dict[str, Any] | None, str]:
        spec = self.spec
        entry = store.find(self.module, entry_id)
        if entry is None:
            return None, f"{spec.entity} {entry_id} 不存在或已归档"
        if action not in spec.action_rules:
            return None, f"动作「{action}」不属于{spec.label}可执行范围"
        target = spec.action_rules[action]
        if target not in spec.status_order:
            return None, f"目标状态「{target}」不在允许的状态序列里"
        entry["status"] = target
        entry["pending"] = target != spec.status_order[-1]
        entry["abnormal"] = action in spec.negative_actions
        return entry, f"{spec.entity}已{action}"
