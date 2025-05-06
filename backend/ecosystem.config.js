module.exports = {
  apps: [{
    name: "address_book_backend",
    script: "gunicorn",
    args: "app:app -b 0.0.0.0:5000",
    interpreter: "venv/bin/python3",
    env: {
      "FLASK_APP": "app.py",
      "FLASK_ENV": "production"
    }
  }]
} 