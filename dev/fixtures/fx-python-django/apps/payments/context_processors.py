"""Custom context processor for the payments app."""


def payment_totals(request):
    return {
        "payments_count": 0,
        "payments_total_amount": 0,
    }