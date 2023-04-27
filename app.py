from flask import Flask,render_template,request
import pickle
import pandas as pd
import numpy as np

popular_dict = pickle.load(open('popularity_dict.pkl','rb'))
popular_df = pd.DataFrame(popular_dict)

pt_dict = pickle.load(open('pt_dict.pkl','rb'))
pt=pd.DataFrame(pt_dict)
books_dict = pickle.load(open('books_dict.pkl','rb'))
books_df=pd.DataFrame(books_dict)
similarity_scores=pickle.load(open('similarity_scores.pkl','rb'))


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name = list(popular_df['Book-Title'].values),
                           author = list(popular_df['Book-Author'].values),
                           image = list(popular_df['Image-URL-M'].values),
                           votes = list(popular_df['num_rating'].values),
                           rating = list(popular_df['avg_rating'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')


@app.route("/recommend_books", methods=['post'])
def recommend():
    try:
        user_input= request.form.get('user_input')
        index = np.where(pt.index ==user_input)[0][0]
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:6]

        data = []

        for i in similar_items:
            item = []

            temp_df = books_df[books_df['Book-Title'] == pt.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

            data.append(item)

        return render_template('recommend.html', data=data)
    except Exception as e:
        return "No Such Data Found".upper()


if __name__ == '__main__':
    app.run(debug=True)