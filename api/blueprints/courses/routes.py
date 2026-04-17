"""Courses — catalog CRUD + deactivate (Phase 1 dummy responses)."""

from __future__ import annotations

from flask import Blueprint, jsonify, request

courses_bp = Blueprint("courses", __name__)

_DUMMY_COURSES = [
    {
        "course_id": "CS3200",
        "department": "CS",
        "title": "Database Design",
        "status": "active",
    },
    {
        "course_id": "MATH1341",
        "department": "MATH",
        "title": "Calculus 1",
        "status": "active",
    },
]


@courses_bp.route("/", methods=["GET", "POST"])
def list_or_create_courses():
    if request.method == "GET":
        return jsonify({"courses": _DUMMY_COURSES, "count": len(_DUMMY_COURSES)}), 200
    body = request.get_json(silent=True) or {}
    created = {
        "course_id": body.get("course_id", "NEW-0000"),
        "department": body.get("department", "UNK"),
        "title": body.get("title", "New course"),
        "status": "active",
    }
    return jsonify({"created": True, "course": created}), 201


@courses_bp.route("/<course_id>", methods=["GET"])
def get_course(course_id: str):
    for row in _DUMMY_COURSES:
        if row["course_id"] == course_id:
            return jsonify(row), 200
    return jsonify({"error": "not_found", "course_id": course_id}), 404


@courses_bp.route("/<course_id>", methods=["PUT"])
def update_course(course_id: str):
    body = request.get_json(silent=True) or {}
    return (
        jsonify(
            {
                "updated": True,
                "course_id": course_id,
                "patch": body,
            }
        ),
        200,
    )


@courses_bp.route("/<course_id>/deactivate", methods=["PUT"])
def deactivate_course(course_id: str):
    return (
        jsonify(
            {
                "deactivated": True,
                "course_id": course_id,
                "status": "inactive",
            }
        ),
        200,
    )
