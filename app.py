from __init__ import create_app
import os

app = create_app()

if __name__ == "__main__":
    app.secret_key = os.urandom(25)
    app.run()
