from flask import Flask

from pizza_boom.api import create_app


app: Flask = create_app()
