import enum


class UserApproveStatusFlag(enum.Enum):
    W = 0  # Wait
    A = 1  # Approved
    D = 2  # Denied
    S = 3  # Stoped
