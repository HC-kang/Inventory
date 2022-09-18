import enum


class WarehouseType(enum.Enum):
    YARD   = 0  # 야적장
    FENCE  = 1  # 울타리
    ROOF   = 2  # 천장
    NORMAL = 3  # 일반
    LOW    = 4  # 냉장
    FREEZE = 5  # 냉동
