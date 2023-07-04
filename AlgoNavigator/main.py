from website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True) # Setting debug = true allows the terminal to keep running as we make changes
