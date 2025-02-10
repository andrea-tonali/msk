import pytest
from utils.helpers import extract_schedule_info


@pytest.mark.parametrize(
    "schedule_slug, expected_output",
    [
        ("1m-0d-pre-op", (-30, 0, "operation")),
        ("14w-6m-post-op", (-98, -180, "operation")),
        ("50w-54m-post-op", (-350, -1620, "operation")),
        ("12d-4w-post-op", (-12, -28, "operation")),
        ("0d-2d-post-op", (0, -2, "operation")),
        ("always", (None, None, "operation")),
        ("pre-op", (None, None, "operation")),
        ("post-op", (None, None, "operation")),
        ("op", (None, None, "operation")),
        ("inv", (None, None, "operation")),
        ("1d-6w-post-op", (-1, -42, "operation")),
        ("5y-10y-post-op", (-1825, -3650, "operation")),
        ("6w-12y-post-op", (-42, -4380, "operation")),
        ("2m-0d-pre-op", (-60, 0, "operation")),
        ("0d-7d-post-reg", (0, -7, "operation")),
        ("30d-42d-post-op", (-30, -42, "operation")),
        ("0d-1y-post-op", (0, -365, "operation")),
        ("6m-1y-post-op", (-180, -365, "operation")),
        ("1y-pre-op", (-365, -365, "operation")),
        ("1w-post-op", (-7, -7, "operation")),
        ("2w-3w-post-op", (-14, -21, "operation")),
        ("15y-20y-post-op", (-5475, -7300, "operation")),
    ],
)
def test_extract_schedule_info(schedule_slug, expected_output):
    assert extract_schedule_info(schedule_slug) == expected_output
