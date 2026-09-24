"""业务模块共用的数据仓库口径。

清单读取（关键字/状态筛选与分页）、登记时的必填校验、动作判定与状态流转，
都收拢在这一份实现里。各业务模块服务只声明一份 ``ModuleSpec``（模块名、
单据/领域称谓、必填字段、状态序列、动作映射等），不再各抄一遍逻辑，
改口径时只需改这里。
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.store import store


@dataclass(frozen=True)
class ModuleSpec:
    """一个业务模块的声明式配置。

    - ``module``：数据仓库（``store``）里的表名
    - ``entity_label``：单据/对象称谓，如「入库单」，用于提示文案
    - ``domain_label``：业务领域称谓，如「入库管理」，用于提示文案
    - ``required_fields``：登记时的必填字段；首个字段同时作为关键字检索字段
    - ``status_order``：允许的状态序列，首个为新建初始状态，末个为终态
    - ``action_rules``：动作到目标状态的映射
    - ``negative_actions``：命中后把记录标记为异常的动作
    - ``keyword_field``：关键字检索字段，缺省取 ``required_fields`` 的首个字段
    """

    module: str
    entity_label: str
    domain_label: str
    required_fields: list[str]
    status_order: list[str]
    action_rules: dict[str, str]
    negative_actions: list[str] = field(default_factory=list)
    keyword_field: str | None = None

    def __post_init__(self) -> None:
        if not self.required_fields:
            raise ValueError(f"模块 {self.module} 至少要声明一个必填字段")
        if not self.status_order:
            raise ValueError(f"模块 {self.module} 至少要声明一个状态")
        if self.keyword_field is None:
            object.__setattr__(self, "keyword_field", self.required_fields[0])
        bad_targets = sorted(set(self.action_rules.values()) - set(self.status_order))
        if bad_targets:
            raise ValueError(
                f"模块 {self.module} 的动作目标状态 {bad_targets} 不在状态序列 "
                f"{self.status_order} 内"
            )


class ModuleService:
    """清单读取、必填校验与动作判定的统一实现，子类只需提供 ``spec``。"""

    spec: ModuleSpec

    def __init__(self, spec: ModuleSpec) -> None:
        self.spec = spec

    def list_entries(
        self,
        *,
        keyword: str | None = None,
        status: str | None = None,
        page: int = 1,
        size: int = 20,
    ) -> tuple[list[dict[str, Any]], int]:
        rows = store.rows(self.spec.module)
        if keyword:
            keyword_field = self.spec.keyword_field or self.spec.required_fields[0]
            rows = [row for row in rows if keyword in str(row.get(keyword_field, ""))]
        if status:
            rows = [row for row in rows if row.get("status") == status]
        total = len(rows)
        start = max(page - 1, 0) * size
        return rows[start:start + size], total

    def get_entry(self, entry_id: int) -> dict[str, Any] | None:
        return store.find(self.spec.module, entry_id)

    def create_entry(self, values: dict[str, Any]) -> tuple[dict[str, Any] | None, list[str]]:
        missing = [
            field_name
            for field_name in self.spec.required_fields
            if not str(values.get(field_name) or "").strip()
        ]
        if missing:
            return None, missing
        rows = store.rows(self.spec.module)
        entry = {"id": max((int(row.get("id", 0)) for row in rows), default=0) + 1}
        entry.update({field_name: values.get(field_name) for field_name in self.spec.required_fields})
        entry["status"] = self.spec.status_order[0]
        entry["pending"] = True
        entry["abnormal"] = False
        rows.append(entry)
        return entry, []

    def run_action(self, entry_id: int, action: str) -> tuple[dict[str, Any] | None, str]:
        spec = self.spec
        entry = store.find(spec.module, entry_id)
        if entry is None:
            return None, f"{spec.entity_label} {entry_id} 不存在或已归档"
        if action not in spec.action_rules:
            return None, f"动作「{action}」不属于{spec.domain_label}可执行范围"
        target = spec.action_rules[action]
        if target not in spec.status_order:
            return None, f"目标状态「{target}」不在允许的状态序列里"
        entry["status"] = target
        entry["pending"] = target != spec.status_order[-1]
        entry["abnormal"] = action in spec.negative_actions
        return entry, f"{spec.entity_label}已{action}"
