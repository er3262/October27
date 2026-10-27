#!/usr/bin/env python3
"""Create schema tables and load class_dataset.csv into Postgres."""

from __future__ import annotations

import csv
import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent


def split_list(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def database_url_from_env() -> str:
    load_dotenv(ROOT / ".env")
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return database_url

    env_path = ROOT / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            stripped = line.strip()
            if stripped and not stripped.startswith("#") and "://" in stripped:
                return stripped.split("=", 1)[-1].strip().strip('"').strip("'")

    raise SystemExit("DATABASE_URL is missing from .env")


def main() -> None:
    database_url = database_url_from_env()

    schema_sql = (ROOT / "schema.sql").read_text()

    with psycopg.connect(database_url, connect_timeout=10) as conn:
        with conn.cursor() as cur:
            cur.execute(schema_sql)

            with (ROOT / "class_dataset.csv").open(newline="") as csvfile:
                rows = list(csv.DictReader(csvfile))

            for row in rows:
                cur.execute(
                    """
                    INSERT INTO students (netid, name, school_year)
                    VALUES (%s, %s, %s)
                    """,
                    (row["netid"], row["name"], row["school_year"]),
                )
                cur.execute(
                    """
                    INSERT INTO survey_responses (
                        netid,
                        intro_programming,
                        skill_programming,
                        skill_data_stats,
                        skill_frontend_design,
                        skill_business_pitch,
                        working_style,
                        interests,
                        semester_goal,
                        submitted_at
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        row["netid"],
                        row["intro_programming"],
                        int(row["skill_programming"]),
                        int(row["skill_data_stats"]),
                        int(row["skill_frontend_design"]),
                        int(row["skill_business_pitch"]),
                        row["working_style"],
                        row["interests"],
                        row["semester_goal"],
                        row["submitted_at"],
                    ),
                )

                for tool_name in split_list(row["tools"]):
                    cur.execute(
                        """
                        INSERT INTO student_tools (netid, tool_id)
                        SELECT %s, tool_id FROM tools WHERE tool_name = %s
                        """,
                        (row["netid"], tool_name),
                    )

                for slot_name in split_list(row["availability"]):
                    cur.execute(
                        """
                        INSERT INTO student_availability (netid, slot_id)
                        SELECT %s, slot_id FROM availability_slots WHERE slot_name = %s
                        """,
                        (row["netid"], slot_name),
                    )

            cur.execute("SELECT COUNT(*) FROM students")
            student_count = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM survey_responses")
            response_count = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM student_tools")
            tool_link_count = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM student_availability")
            avail_link_count = cur.fetchone()[0]

        conn.commit()

    print(
        "Created tables and loaded data: "
        f"{student_count} students, {response_count} responses, "
        f"{tool_link_count} student_tools, {avail_link_count} student_availability"
    )


if __name__ == "__main__":
    main()
