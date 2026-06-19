from __future__ import annotations


def calculate_runoff(p_mm: float, cn: float) -> float:
    """
    Compute direct runoff depth Q (mm) using the SCS-CN method.

    Formula:
        S  = (25400 / CN) - 254
        Ia = 0.2 * S
        Q  = (P - Ia)^2 / (P - Ia + S)   for P > Ia, else 0

    Physical constraints:
    - Q >= 0
    - Q <= P
    """
    if p_mm < 0:
        raise ValueError("Rainfall P (mm) must be non-negative.")
    if cn <= 0 or cn > 100:
        raise ValueError("Curve Number (CN) must be in the range (0, 100].")

    s_mm = (25400.0 / cn) - 254.0
    ia_mm = 0.2 * s_mm

    if p_mm <= ia_mm:
        return 0.0

    q_mm = (p_mm - ia_mm) ** 2 / (p_mm - ia_mm + s_mm)
    if q_mm < 0:
        q_mm = 0.0
    if q_mm > p_mm:
        q_mm = p_mm
    return float(q_mm)

