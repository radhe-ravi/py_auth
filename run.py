from app import auth_app

app = auth_app()

if __name__ == "__main__":
    app.run(debug=True)
