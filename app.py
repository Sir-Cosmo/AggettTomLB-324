import os
from dataclasses import dataclass
from typing import List, Optional

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, session

app = Flask(__name__)
app.secret_key = os.urandom(24)

# .env laden (PASSWORD="...")
load_dotenv()
app.secret_key = os.getenv("SECRET_KEY", "change-me-in-prod")
PASSWORD = os.getenv("PASSWORD", "")


@dataclass
class Entry:
    content: str
    happiness: Optional[str] = None


# einfache In-Memory-Liste als „DB“
entries: List[Entry] = []


@app.get("/")
def index():
    return render_template("index.html", entries=entries)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("password") == PASSWORD:
            session["logged_in"] = True
            flash("Login successful!", "success")
            return redirect("/")
        flash("Incorrect password. Please try again.", "error")
    return render_template("login.html")


@app.get("/logout")
def logout():
    session.pop("logged_in", None)
    flash("Logged out successfully.", "success")
    return redirect("/")


@app.post("/add_entry")
def add_entry():
    content = (request.form.get("content") or "").strip()
    happiness = (request.form.get("happiness") or "").strip() or None
    if content:
        entries.insert(0, Entry(content=content, happiness=happiness))
    # wichtig für deinen Test: exakt '/' im Location-Header
    return redirect("/")
