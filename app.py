import os
import logging
import sqlite3
import secrets
from typing import Tuple, List, NamedTuple, Union, Any

from flask import Flask, render_template, redirect, url_for, request, session, g

DATABASE = "ptest.db"

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(32)


def get_db() -> sqlite3.Connection:
    """
    If there are not open database connections in the app context,
    create a new one.
    """
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_connection(exception: Any) -> None:
    """
    Safely close the database connection when the app is closed.
    """
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


def query_db(
    query: str, args: tuple = (), one: bool = False
) -> Union[NamedTuple, List[NamedTuple]]:
    """
    Query the database.

    Parameters:
    query: SQL query to be executed.
    args: list of argumets that will be replaced in the SQL query
    one: returns only the first row if True, returns all rows otherwise

    Returns:
    One or more rows as named tuples.
    """
    cur = get_db().execute(query, args)
    rows = cur.fetchall()
    cur.close()
    return (rows[0] if rows else None) if one else rows


def init_db() -> None:
    """
    Loads static dataset into the database. See the readme file.
    """
    with app.app_context():
        db = get_db()
        with app.open_resource("schema.sql", mode="r") as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.route("/")
def index():
    return redirect(url_for("welcome"))


@app.route("/welcome")
def welcome():
    return render_template("welcome.html")


@app.route("/start")
def start():
    session["score"] = 0
    return redirect(url_for("question", id=0))


@app.route("/question/<int:id>")
def question(id: int):
    score: Union[int, None] = session.get('score', None)
    if score is None:
        return redirect(url_for('welcome'))

    question: Tuple = query_db(
        query="select * from questions where id = ?", args=(id,), one=True
    )
    answers: List[Tuple] = query_db(
        query="select * from answers where question_id = ?", args=(id,)
    )

    if not question:
        logging.error(f"Question with id:${id} not found in the database.")
        return render_template("not_found.html", msg="Question not found."), 404

    return render_template("question.html", question=question, answers=answers)


@app.route("/update_score", methods=["POST"])
def update_score():
    score: Union[int, None] = session.get('score', None)
    if score is None:
        return redirect(url_for('welcome'))

    id = int(request.form["questionId"])
    score = int(request.form["answers"])
    is_last = bool(int(request.form["isLast"]))

    session["score"] += score

    if is_last:
        return redirect(url_for("result"))
    else:
        return redirect(url_for("question", id=id + 1))


@app.route("/result")
def result():
    score: Union[int, None] = session.get('score', None)
    if score is None:
        return redirect(url_for('welcome'))
    
    thrashold: Tuple = query_db(
        query="select c*3/2 from (select count(1) as c from questions)", one=True
    )
    
    is_extrovert: bool = score > thrashold[0]
    return render_template("result.html", is_extrovert=is_extrovert)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("not_found.html", msg="Page not found."), 404
