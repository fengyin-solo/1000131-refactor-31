"""模块声明表：每个业务模块只在这里声明一次自己的口径。

新增业务模块时，在 ``MODULE_SPECS`` 里加一条 ``ModuleSpec`` 即可，
清单读取（筛选/分页）、必填校验、动作判定与状态流转都由
``app.services.base.ModuleService`` 与 ``app.routers.factory`` 共用实现提供。

字段说明见 :class:`ModuleSpec`；各字段取值沿用改造前散落在 services/routers
里的常量，顺序与措辞保持不变。
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ModuleSpec:
    """一个业务模块的声明式配置。

    - ``name``：仓库表名 / 接口前缀（``/api/<name>``）
    - ``label``：模块在页面与接口分组里的名称（原 APIRouter tags）
    - ``entity``：业务对象的称呼，用于「{entity} {id} 不存在或已归档」等提示
    - ``keyword_field``：列表关键字检索匹配的字段
    - ``required_fields``：登记时的必填字段，同时是新建记录时写入的字段
    - ``status_order``：允许的状态序列，首项是新建默认态，末项是完结态
    - ``action_rules``：动作 → 目标状态 的映射
    - ``negative_actions``：执行后把记录标记为异常（abnormal=True）的动作
    - ``list_fields``：列表页展示的列（接口本身不裁剪，仅作声明与文档用途）
    """

    name: str
    label: str
    entity: str
    keyword_field: str
    required_fields: tuple[str, ...]
    status_order: tuple[str, ...]
    action_rules: dict[str, str]
    negative_actions: frozenset[str]
    list_fields: tuple[str, ...]


MODULE_SPECS: dict[str, ModuleSpec] = {
    spec.name: spec
    for spec in (
        ModuleSpec(
            name="order",
            label="冷链订单",
            entity="冷链订单",
            keyword_field="订单编号",
            required_fields=("订单编号", "客户名称", "货物名称"),
            status_order=("待受理", "已受理", "已调度", "已完结", "已取消"),
            action_rules={"受理订单": "已受理", "调度派车": "已调度", "取消订单": "已取消"},
            negative_actions=frozenset(),
            list_fields=("订单编号", "客户名称", "货物名称", "货物类别", "起始冷库", "目的冷库", "要求温度区间", "下单时间"),
        ),
        ModuleSpec(
            name="waybill",
            label="运单管理",
            entity="冷链运单",
            keyword_field="运单号",
            required_fields=("运单号", "关联订单", "承运车辆"),
            status_order=("待装车", "运输中", "已签收", "已作废"),
            action_rules={"确认装车": "运输中", "签收运单": "已签收", "作废运单": "已作废"},
            negative_actions=frozenset({"作废运单"}),
            list_fields=("运单号", "关联订单", "承运车辆", "司机姓名", "装车时间", "卸货时间", "运单状态"),
        ),
        ModuleSpec(
            name="vehicle",
            label="冷藏车管理",
            entity="冷藏车辆",
            keyword_field="车牌号码",
            required_fields=("车牌号码", "车辆类型", "制冷机组型号"),
            status_order=("可用", "出车中", "维修中", "已停用"),
            action_rules={"安排出车": "出车中", "回场登记": "可用", "停用车辆": "已停用"},
            negative_actions=frozenset({"停用车辆"}),
            list_fields=("车牌号码", "车辆类型", "制冷机组型号", "车厢容积", "温区数量", "所属车队", "年检到期日"),
        ),
        ModuleSpec(
            name="driver",
            label="司机管理",
            entity="司机档案",
            keyword_field="司机工号",
            required_fields=("司机工号", "司机姓名", "联系电话"),
            status_order=("待上岗", "在岗", "休息中", "已离职"),
            action_rules={"安排上岗": "在岗", "排班休息": "休息中", "办理离职": "已离职"},
            negative_actions=frozenset(),
            list_fields=("司机工号", "司机姓名", "联系电话", "驾驶证号", "从业资格证号", "所属车队", "在途状态"),
        ),
        ModuleSpec(
            name="temperature",
            label="温控监控",
            entity="温控记录",
            keyword_field="记录编号",
            required_fields=("记录编号", "关联运单", "测点编号"),
            status_order=("正常", "偏高", "偏低", "已离线"),
            action_rules={"确认记录": "正常", "标记超限": "偏高", "重新采集": "正常"},
            negative_actions=frozenset(),
            list_fields=("记录编号", "关联运单", "测点编号", "实时温度", "温度上限", "温度下限", "采集时间"),
        ),
        ModuleSpec(
            name="excursion",
            label="温度异常",
            entity="温度异常事件",
            keyword_field="事件编号",
            required_fields=("事件编号", "关联运单", "异常类型"),
            status_order=("待处置", "处置中", "已闭环", "已忽略"),
            action_rules={"受理事件": "处置中", "提交处置": "已闭环", "忽略事件": "已忽略"},
            negative_actions=frozenset({"忽略事件"}),
            list_fields=("事件编号", "关联运单", "异常类型", "超限时长", "最高温度", "发生时间", "处置人"),
        ),
        ModuleSpec(
            name="warehouse",
            label="冷库管理",
            entity="冷库档案",
            keyword_field="冷库编码",
            required_fields=("冷库编码", "冷库名称", "库区温区"),
            status_order=("已启用", "检修中", "已停用"),
            action_rules={"启用冷库": "已启用", "安排检修": "检修中", "停用冷库": "已停用"},
            negative_actions=frozenset({"停用冷库"}),
            list_fields=("冷库编码", "冷库名称", "库区温区", "设定温度", "库容吨位", "责任人", "启用状态"),
        ),
        ModuleSpec(
            name="inbound",
            label="入库管理",
            entity="入库单",
            keyword_field="入库单号",
            required_fields=("入库单号", "供应商名称", "货物名称"),
            status_order=("待收货", "已收货", "已上架", "已退回"),
            action_rules={"确认收货": "已收货", "安排上架": "已上架", "退回入库": "已退回"},
            negative_actions=frozenset(),
            list_fields=("入库单号", "供应商名称", "货物名称", "批次号", "入库数量", "到货温度", "收货人", "入库时间"),
        ),
        ModuleSpec(
            name="outbound",
            label="出库管理",
            entity="出库单",
            keyword_field="出库单号",
            required_fields=("出库单号", "客户名称", "货物名称"),
            status_order=("待拣货", "已拣货", "已发运", "已取消"),
            action_rules={"确认拣货": "已拣货", "安排发运": "已发运", "取消出库": "已取消"},
            negative_actions=frozenset(),
            list_fields=("出库单号", "客户名称", "货物名称", "批次号", "出库数量", "出库温度", "拣货人", "出库时间"),
        ),
        ModuleSpec(
            name="inventory",
            label="库存管理",
            entity="库存批次",
            keyword_field="库存编码",
            required_fields=("库存编码", "货物名称", "批次号"),
            status_order=("正常", "临近保质期", "已冻结", "已清空"),
            action_rules={"冻结库存": "已冻结", "解冻库存": "正常", "盘点修正": "正常"},
            negative_actions=frozenset(),
            list_fields=("库存编码", "货物名称", "批次号", "库位编号", "在库数量", "锁定量", "保质期至", "入库日期"),
        ),
        ModuleSpec(
            name="trace",
            label="批次追溯",
            entity="追溯记录",
            keyword_field="追溯码",
            required_fields=("追溯码", "货物名称", "生产批次"),
            status_order=("待关联", "已关联", "已发布", "已撤回"),
            action_rules={"关联上游": "已关联", "发布追溯": "已发布", "撤回追溯": "已撤回"},
            negative_actions=frozenset(),
            list_fields=("追溯码", "货物名称", "生产批次", "上游供应商", "入库单号", "全程温度区间", "追溯状态"),
        ),
        ModuleSpec(
            name="quality",
            label="质检管理",
            entity="质检单",
            keyword_field="质检单号",
            required_fields=("质检单号", "关联批次", "检测项目"),
            status_order=("待检测", "检测中", "合格", "不合格"),
            action_rules={"开始检测": "检测中", "判定合格": "合格", "判定不合格": "不合格"},
            negative_actions=frozenset(),
            list_fields=("质检单号", "关联批次", "检测项目", "检测值", "标准限值", "检测结论", "检测员", "检测时间"),
        ),
        ModuleSpec(
            name="route",
            label="线路管理",
            entity="配送线路",
            keyword_field="线路编码",
            required_fields=("线路编码", "线路名称", "起点冷库"),
            status_order=("草稿", "已启用", "已停用"),
            action_rules={"启用线路": "已启用", "调整站点": "草稿", "停用线路": "已停用"},
            negative_actions=frozenset({"停用线路"}),
            list_fields=("线路编码", "线路名称", "起点冷库", "终点冷库", "途经站点", "预计时长", "线路里程"),
        ),
        ModuleSpec(
            name="dispatch",
            label="调度派单",
            entity="调度单",
            keyword_field="调度单号",
            required_fields=("调度单号", "关联订单", "配送线路"),
            status_order=("待派单", "已派单", "已发车", "已撤销"),
            action_rules={"确认派单": "已派单", "确认发车": "已发车", "撤销派单": "已撤销"},
            negative_actions=frozenset({"撤销派单"}),
            list_fields=("调度单号", "关联订单", "配送线路", "指派车辆", "指派司机", "计划发车时间", "调度状态"),
        ),
        ModuleSpec(
            name="device",
            label="温控设备",
            entity="温控设备",
            keyword_field="设备编号",
            required_fields=("设备编号", "设备名称", "设备型号"),
            status_order=("在用", "待校准", "故障", "已报废"),
            action_rules={"登记设备": "在用", "提交校准": "待校准", "报废设备": "已报废"},
            negative_actions=frozenset(),
            list_fields=("设备编号", "设备名称", "设备型号", "安装位置", "采集精度", "校准到期日", "责任人"),
        ),
        ModuleSpec(
            name="maint",
            label="维保工单",
            entity="维保工单",
            keyword_field="工单编号",
            required_fields=("工单编号", "关联设备", "故障现象"),
            status_order=("待受理", "处理中", "待验收", "已关闭"),
            action_rules={"受理工单": "处理中", "派工处理": "处理中", "关闭工单": "已关闭"},
            negative_actions=frozenset(),
            list_fields=("工单编号", "关联设备", "故障现象", "紧急程度", "报修人", "受理班组", "期望完成时间"),
        ),
        ModuleSpec(
            name="alarm",
            label="告警中心",
            entity="告警事件",
            keyword_field="告警编号",
            required_fields=("告警编号", "告警类型", "告警等级"),
            status_order=("待确认", "已确认", "已处置", "已忽略"),
            action_rules={"确认告警": "已确认", "处置告警": "已处置", "忽略告警": "已忽略"},
            negative_actions=frozenset({"忽略告警"}),
            list_fields=("告警编号", "告警类型", "告警等级", "触发设备", "触发时间", "处理状态", "处理人"),
        ),
        ModuleSpec(
            name="customer",
            label="客户管理",
            entity="客户档案",
            keyword_field="客户编码",
            required_fields=("客户编码", "客户名称", "客户类型"),
            status_order=("待审核", "合作中", "已暂停", "已终止"),
            action_rules={"审核客户": "合作中", "暂停合作": "已暂停", "终止合作": "已终止"},
            negative_actions=frozenset(),
            list_fields=("客户编码", "客户名称", "客户类型", "联系人", "联系电话", "结算方式", "合作状态"),
        ),
        ModuleSpec(
            name="billing",
            label="计费结算",
            entity="计费单",
            keyword_field="计费单号",
            required_fields=("计费单号", "客户名称", "计费周期"),
            status_order=("待核算", "已核算", "已对账", "已开票"),
            action_rules={"生成账单": "已核算", "确认对账": "已对账", "开具发票": "已开票"},
            negative_actions=frozenset(),
            list_fields=("计费单号", "客户名称", "计费周期", "运输里程", "计费金额", "计费规则", "结算状态"),
        ),
        ModuleSpec(
            name="report",
            label="报表导出",
            entity="报表任务",
            keyword_field="报表名称",
            required_fields=("报表名称", "统计范围", "统计周期"),
            status_order=("排队中", "生成中", "已完成", "已失败"),
            action_rules={"生成报表": "生成中", "重试任务": "排队中", "下载报表": "已完成"},
            negative_actions=frozenset(),
            list_fields=("报表名称", "统计范围", "统计周期", "导出格式", "任务状态", "生成时间"),
        ),
        ModuleSpec(
            name="setting",
            label="系统设置",
            entity="系统参数",
            keyword_field="参数编码",
            required_fields=("参数编码", "参数名称", "参数值"),
            status_order=("已生效", "待生效", "已回滚"),
            action_rules={"修改参数": "待生效", "回滚参数": "已回滚", "生效参数": "已生效"},
            negative_actions=frozenset({"回滚参数"}),
            list_fields=("参数编码", "参数名称", "参数值", "参数类型", "生效范围", "修改人"),
        ),
    )
}

# 列表页注册顺序（即原 routers/__init__.py 的引入顺序）。
MODULE_ORDER: tuple[str, ...] = (
    "order", "waybill", "vehicle", "driver", "temperature", "excursion",
    "warehouse", "inbound", "outbound", "inventory", "trace", "quality",
    "route", "dispatch", "device", "maint", "alarm", "customer", "billing",
    "report", "setting",
)


def get_spec(name: str) -> ModuleSpec:
    """按模块名取声明；未知模块直接报 KeyError，属于装配期错误而不是运行期分支。"""
    return MODULE_SPECS[name]
