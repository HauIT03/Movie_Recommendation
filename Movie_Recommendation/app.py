from flask import Flask, request, render_template, jsonify
from data_preparation import movies_df, ratings_df, tags_df, users_df
from recommendation_model import get_recommendations, recommend_by_title

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        tag = request.form.get('tag')
        genre = request.form.get('genre')
        title = request.form.get('title')
        rating = request.form.get('rating') == 'on'  # checkbox value is 'on'
        top_n = request.form.get('top_n', type=int, default=20)

        user_id = int(user_id) if user_id and user_id.isdigit() else None
        top_n = min(max(top_n, 1), 9742)  # Đảm bảo top_n nằm trong khoảng 1-9742

        # Kiểm tra lỗi đầu vào
        error_message = ""
        if user_id is not None and (user_id < 1 or user_id > 610):
            error_message = "User ID phải nằm trong khoảng từ 1 đến 610."
        elif top_n < 1 or top_n > 9742:
            error_message = "Số lượng gợi ý phải nằm trong khoảng từ 1 đến 9742."

        if error_message:
            return render_template('index.html', error=error_message)

        # Gọi hàm gợi ý
        recommendations = get_recommendations(
            user_id=user_id,
            rating=rating,
            tag=tag,
            genre=genre,
            title=title,
            top_n=top_n
        )

        # Kiểm tra xem có lỗi hay không
        if isinstance(recommendations, dict) and "error" in recommendations:
            error_message = recommendations["error"]
            return render_template('index.html', error=error_message)

        return render_template('recommendations.html', recommendations=recommendations)

    return render_template('index.html')

@app.route('/suggest', methods=['GET'])
def suggest():
    title = request.args.get('title')
    suggestions = recommend_by_title(title, movies_df)
    return jsonify(suggestions)

if __name__ == '__main__':
    app.run(debug=True)
