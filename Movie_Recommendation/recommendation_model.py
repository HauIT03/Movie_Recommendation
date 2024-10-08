from surprise import Dataset, Reader, SVD
import pandas as pd
import joblib
import re
from data_preparation import ratings_df, movies_df, tags_df

# Tải mô hình đã huấn luyện
svd_model = joblib.load('svd_model.pkl')


def extract_year(title):
    match = re.search(r'\b(\d{4})\b', title)  # Tìm năm 4 chữ số
    return int(match.group(0)) if match else None


def recommend_by_user(user_id, svd_model, movies_df, top_n=20):
    all_movies = movies_df['MovieID'].tolist()
    rated_movies = ratings_df[ratings_df['UserID'] == user_id]['MovieID'].tolist()
    unrated_movies = [movie for movie in all_movies if movie not in rated_movies]

    recommendations = [(movie, svd_model.predict(user_id, movie).est) for movie in unrated_movies]
    recommendations.sort(key=lambda x: x[1], reverse=True)

    # Lấy thông tin chi tiết cho các gợi ý
    recommended_movie_ids = [rec[0] for rec in recommendations[:top_n]]
    return get_movie_details(recommended_movie_ids, movies_df)


def recommend_by_rating(movies_df, top_n=20):
    avg_ratings = ratings_df.groupby('MovieID')['Rating'].mean().sort_values(ascending=False)
    top_movies = avg_ratings.head(top_n).index.tolist()
    return movies_df[movies_df['MovieID'].isin(top_movies)][['MovieID', 'Title', 'Genre']].values.tolist()


def recommend_by_tag(tag, tags_df, movies_df, top_n=20):
    tagged_movies = tags_df[tags_df['Tag'].str.contains(tag, case=False)]['MovieID'].unique()
    return movies_df[movies_df['MovieID'].isin(tagged_movies)][['MovieID', 'Title', 'Genre']].head(
        top_n).values.tolist()


def recommend_by_genre(genre, movies_df, top_n=20):
    genre_movies = movies_df[movies_df['Genre'].str.contains(genre, case=False)]
    return genre_movies[['MovieID', 'Title', 'Genre']].head(top_n).values.tolist()


def recommend_by_title(title, movies_df, top_n=20):
    matching_movies = movies_df[movies_df['Title'].str.contains(title, case=False, regex=False)]
    return matching_movies.head(top_n)[['MovieID', 'Title', 'Genre']].values.tolist()


def get_movie_details(movie_ids, movies_df):
    return movies_df[movies_df['MovieID'].isin(movie_ids)][['MovieID', 'Title', 'Genre']].values.tolist()


valid_user_ids = ratings_df['UserID'].unique()


def is_valid_user(user_id):
    return user_id in valid_user_ids


def get_recommendations(user_id=None, rating=False, tag=None, genre=None, title=None, top_n=20):
    recommendations = []
    unique_movie_ids = set()

    # Kiểm tra tính hợp lệ của user_id
    if user_id and not is_valid_user(user_id):
        return {"error": "Invalid user ID."}

    # Khuyến nghị theo Title
    if title:
        title_recommendations = recommend_by_title(title, movies_df, top_n)
        unique_movie_ids.update(movie[0] for movie in title_recommendations)
        recommendations.extend(title_recommendations)

    # Khuyến nghị theo User ID
    if user_id:
        user_recommendations = recommend_by_user(user_id, svd_model, movies_df, top_n)
        filtered_user_recommendations = [rec for rec in user_recommendations if rec[0] not in unique_movie_ids]
        unique_movie_ids.update(movie[0] for movie in filtered_user_recommendations)
        recommendations.extend(filtered_user_recommendations)

    # Khuyến nghị theo Rating
    if rating:
        rating_recommendations = recommend_by_rating(movies_df, top_n)
        filtered_rating_recommendations = [rec for rec in rating_recommendations if rec[0] not in unique_movie_ids]
        unique_movie_ids.update(movie[0] for movie in filtered_rating_recommendations)
        recommendations.extend(filtered_rating_recommendations)

    # Khuyến nghị theo Tag
    if tag:
        tag_recommendations = recommend_by_tag(tag, tags_df, movies_df, top_n)
        filtered_tag_recommendations = [rec for rec in tag_recommendations if rec[0] not in unique_movie_ids]
        unique_movie_ids.update(movie[0] for movie in filtered_tag_recommendations)
        recommendations.extend(filtered_tag_recommendations)

    # Khuyến nghị theo Genre
    if genre:
        genre_recommendations = recommend_by_genre(genre, movies_df, top_n)
        filtered_genre_recommendations = [rec for rec in genre_recommendations if rec[0] not in unique_movie_ids]
        unique_movie_ids.update(movie[0] for movie in filtered_genre_recommendations)
        recommendations.extend(filtered_genre_recommendations)

    # Lọc theo các yếu tố đã cung cấp, bao gồm user_id
    filtered_recommendations = []
    for movie in recommendations:
        matches_title = not title or title.lower() in movie[1].lower()
        matches_genre = not genre or genre.lower() in movie[2].lower()
        matches_tag = not tag or any(
            tag.lower() in t.lower() for t in tags_df[tags_df['MovieID'] == movie[0]]['Tag'].tolist())

        if matches_title and matches_genre and matches_tag:
            # Lọc theo user_id nếu có
            if user_id:
                user_rated_movies = ratings_df[ratings_df['UserID'] == user_id]['MovieID'].tolist()
                if movie[0] not in user_rated_movies:
                    filtered_recommendations.append(movie)
            else:
                filtered_recommendations.append(movie)

    # Giới hạn số lượng gợi ý trả về theo top_n
    movie_details = filtered_recommendations[:min(top_n, len(filtered_recommendations))]

    return movie_details
