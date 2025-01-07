from flask import Flask, render_template
import pandas as pd
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    # Завантажуємо результати
    df = pd.read_csv('voting_results.csv')

    # Підготовка даних для відображення
    top_candidates = df.head(15)
    other_candidates = df.iloc[15:]

    # Останнє оновлення
    last_update = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    return render_template('index.html',
                           top_candidates=top_candidates,
                           other_candidates=other_candidates,
                           last_update=last_update)

if __name__ == '__main__':
    app.run(debug=True)
