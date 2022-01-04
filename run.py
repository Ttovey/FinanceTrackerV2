from financeTracker import create_app, db
from financeTracker.models import User

# to link app to flask_app = export FLASK_APP="run:create_app('dev')"
app = create_app()


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User)


@app.cli.command()
def test():
    """Run Unit Tests"""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    app.run(debug=True)
