"""Courses routes backed by real DB data."""

from __future__ import annotations

from flask import Blueprint, jsonify, request

from api.db import get_cursor

courses_bp = Blueprint("courses", __name__)

@courses_bp.route("/", methods=["GET", "POST"])
def list_or_create_courses():
    if request.method == "GET":
        with get_cursor() as cur:
            cur.execute(
                """
                SELECT
                    c.course_id,
                    c.course_number,
                    c.course_name,
                    c.semester,
                    c.is_active,
                    d.dept_name,
                    d.college
                FROM COURSE c
                JOIN DEPARTMENT d ON d.dept_id = c.dept_id
                ORDER BY c.course_id DESC
                """
            )
            rows = cur.fetchall()
        return jsonify({"courses": rows, "count": len(rows)}), 200

    body = request.get_json(silent=True) or {}
    with get_cursor() as cur:
        cur.execute(
            """
            INSERT INTO COURSE (dept_id, course_number, course_name, semester, is_active)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                body.get("dept_id"),
                body.get("course_number"),
                body.get("course_name"),
                body.get("semester", "Spring 2026"),
                body.get("is_active", 1),
            ),
        )
        course_id = cur.lastrowid
        cur.execute(
            """
            SELECT course_id, dept_id, course_number, course_name, semester, is_active
            FROM COURSE
            WHERE course_id = %s
            """,
            (course_id,),
        )
        created = cur.fetchone()
    return jsonify({"created": True, "course": created}), 201


@courses_bp.route("/<course_id>", methods=["GET"])
def get_course(course_id: str):
    with get_cursor() as cur:
        cur.execute(
            """
            SELECT
                c.course_id,
                c.course_number,
                c.course_name,
                c.semester,
                c.is_active,
                d.dept_name,
                d.college
            FROM COURSE c
            JOIN DEPARTMENT d ON d.dept_id = c.dept_id
            WHERE c.course_id = %s
            """,
            (course_id,),
        )
        row = cur.fetchone()
    if row:
        return jsonify(row), 200
    return jsonify({"error": "not_found", "course_id": course_id}), 404


@courses_bp.route("/<course_id>", methods=["PUT"])
def update_course(course_id: str):
    body = request.get_json(silent=True) or {}
    with get_cursor() as cur:
        cur.execute(
            """
            UPDATE COURSE
            SET dept_id = COALESCE(%s, dept_id),
                course_number = COALESCE(%s, course_number),
                course_name = COALESCE(%s, course_name),
                semester = COALESCE(%s, semester),
                is_active = COALESCE(%s, is_active)
            WHERE course_id = %s
            """,
            (
                body.get("dept_id"),
                body.get("course_number"),
                body.get("course_name"),
                body.get("semester"),
                body.get("is_active"),
                course_id,
            ),
        )
        changed = cur.rowcount > 0
    return (
        jsonify(
            {
                "updated": changed,
                "course_id": course_id,
                "patch": body,
            }
        ),
        200 if changed else 404,
    )


@courses_bp.route("/<course_id>/deactivate", methods=["PUT"])
def deactivate_course(course_id: str):
    with get_cursor() as cur:
        cur.execute("UPDATE COURSE SET is_active = 0 WHERE course_id = %s", (course_id,))
        changed = cur.rowcount > 0
    return (
        jsonify(
            {
                "deactivated": changed,
                "course_id": course_id,
                "status": "inactive",
            }
        ),
        200 if changed else 404,
    )
