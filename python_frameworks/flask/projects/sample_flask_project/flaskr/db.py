import sqlite3

import click
from flask import current_app, g
from pymongo import MongoClient




def get_db():
    client = MongoClient('mongodb://localhost:27017/')
    g.db = client['training']
    return g.db

def init_db():
    db = get_db()

    


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    
    app.cli.add_command(init_db_command)

