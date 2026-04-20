<<<<<<< HEAD
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
=======

from flask import Blueprint, jsonify, request
from backend.db_connection import get_db

courses_bp = Blueprint("courses", __name__)


@courses_bp.route("/", methods=["GET"])
def get_courses():
    cursor = get_db().cursor(dictionary=True)
    cursor.execute('''
        SELECT c.course_id, c.course_number, c.course_name,
               c.is_active, d.dept_name, d.college
        FROM COURSE c
        JOIN DEPARTMENT d ON c.dept_id = d.dept_id
        ORDER BY c.course_number
    ''')
    return jsonify({"courses": cursor.fetchall()}), 200


@courses_bp.route("/", methods=["POST"])
def create_course():
    body = request.get_json(silent=True) or {}
    cursor = get_db().cursor(dictionary=True)
    cursor.execute('''
        INSERT INTO COURSE (course_number, course_name, is_active, dept_id)
        VALUES (%s, %s, TRUE, %s)
    ''', (
        body.get("course_number"),
        body.get("course_name"),
        body.get("dept_id", 1)
    ))
    get_db().commit()
    return jsonify({"created": True, "course_id": cursor.lastrowid}), 201


@courses_bp.route("/<int:course_id>", methods=["GET"])
def get_course(course_id):
    cursor = get_db().cursor(dictionary=True)
    cursor.execute('''
        SELECT c.course_id, c.course_number, c.course_name,
               c.is_active, d.dept_name, d.college
        FROM COURSE c
        JOIN DEPARTMENT d ON c.dept_id = d.dept_id
        WHERE c.course_id = %s
    ''', (course_id,))
    result = cursor.fetchone()
    if not result:
        return jsonify({"error": "not_found"}), 404
    return jsonify(result), 200


@courses_bp.route("/<int:course_id>", methods=["PUT"])
def update_course(course_id):
    body = request.get_json(silent=True) or {}
    cursor = get_db().cursor(dictionary=True)
    cursor.execute('''
        UPDATE COURSE
        SET course_name = %s, is_active = %s
        WHERE course_id = %s
    ''', (
        body.get("course_name"),
        body.get("is_active", True),
        course_id
    ))
    get_db().commit()
    return jsonify({"updated": True, "course_id": course_id}), 200


@courses_bp.route("/<int:course_id>/deactivate", methods=["PUT"])
def deactivate_course(course_id):
    cursor = get_db().cursor(dictionary=True)
    cursor.execute('''
        UPDATE COURSE SET is_active = FALSE WHERE course_id = %s
    ''', (course_id,))
    get_db().commit()
    return jsonify({"deactivated": True, "course_id": course_id}), 200


@courses_bp.route("/<int:course_id>/price-history", methods=["GET"])
def get_price_history(course_id):
    cursor = get_db().cursor(dictionary=True)
    cursor.execute('''
        SELECT ph.semester, ph.avg_price, i.title
        FROM PRICE_HISTORY ph
        JOIN ITEM i ON ph.item_id = i.item_id
        JOIN COURSE_ITEM ci ON i.item_id = ci.item_id
        WHERE ci.course_id = %s
        ORDER BY ph.semester
    ''', (course_id,))
    return jsonify({"history": cursor.fetchall()}), 200


@courses_bp.route("/departments", methods=["GET"])
def get_departments():
    cursor = get_db().cursor(dictionary=True)
    cursor.execute('SELECT dept_id, dept_name, college FROM DEPARTMENT')
    return jsonify({"departments": cursor.fetchall()}), 200
>>>>>>> b973242ce211e97bc1b86a60c6c43d1ad8a64c00
