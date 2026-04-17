"""Analytics — analyst/metrics dashboards (Phase 1 dummy responses)."""

from __future__ import annotations

from flask import Blueprint, jsonify, request

analytics_bp = Blueprint("analytics", __name__)


@analytics_bp.route("/metrics/latest", methods=["GET"])
def get_latest_metrics():
    return (
        jsonify(
            {
                "metric_id": 1,
                "as_of": "2026-04-16T12:00:00Z",
                "active_users": 120,
                "active_listings": 1284,
                "total_transactions": 210,
                "gmv_cents": 18_400_000,
            }
        ),
        200,
    )


@analytics_bp.route("/activity", methods=["GET"])
def get_activity():
    return (
        jsonify(
            {
                "window": request.args.get("window", "7d"),
                "events": [
                    {"ts": "2026-04-15T10:00:00Z", "type": "listing_created", "count": 42},
                    {"ts": "2026-04-15T11:00:00Z", "type": "transaction_completed", "count": 18},
                ],
            }
        ),
        200,
    )


@analytics_bp.route("/price-trends", methods=["GET"])
def get_price_trends():
    return (
        jsonify(
            {
                "course_id": request.args.get("course_id", "CS3200"),
                "material_type": request.args.get("material_type", "textbook"),
                "points": [
                    {"month": "2026-01", "median_price_cents": 4500},
                    {"month": "2026-02", "median_price_cents": 4300},
                    {"month": "2026-03", "median_price_cents": 4200},
                ],
            }
        ),
        200,
    )


@analytics_bp.route("/demand-gaps", methods=["GET"])
def get_demand_gaps():
    return (
        jsonify(
            {
                "gaps": [
                    {
                        "course_id": "CS3000",
                        "material": "Textbook",
                        "wanted_count": 54,
                        "available_count": 9,
                    },
                    {
                        "course_id": "PHYS1000",
                        "material": "Lab kit",
                        "wanted_count": 31,
                        "available_count": 4,
                    },
                ]
            }
        ),
        200,
    )


@analytics_bp.route("/reports", methods=["POST"])
def create_report():
    body = request.get_json(silent=True) or {}
    return (
        jsonify(
            {
                "report_id": "RPT-1001",
                "status": "queued",
                "format": body.get("format", "csv"),
                "filters": body.get("filters", {}),
            }
        ),
        202,
    )
