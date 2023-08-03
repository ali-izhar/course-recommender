import os
import pandas as pd
from fuzzywuzzy import process
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer


class Recommender:
    def __init__(self):
        assets_path = os.path.join(os.path.dirname(__file__), 'assets')
        csv_path = os.path.join(assets_path, 'Coursera.csv')
        self.df = pd.read_csv(csv_path)

    @staticmethod
    def vectorize_strings(strings: list) -> list:
        """
        Vectorize the given strings using the CountVectorizer.

        Args:
            strings (list): A list of strings to vectorize.

        Returns:
            A dense vector representation of the given strings.
        """
        vectorizer = CountVectorizer()
        vectors = vectorizer.fit_transform(strings)
        dense_vectors = vectors.toarray()
        return dense_vectors

    @staticmethod
    def compute_similarity(dense_vectors: list) -> list:
        """
        Compute the cosine similarity between the first vector and the rest of the vectors.

        Args:
            dense_vectors (list): A list of dense vectors.

        Returns:
            A list of cosine similarities between the first vector and the rest of the vectors.
        """
        similarities = cosine_similarity([dense_vectors[0]], dense_vectors)
        return similarities

    def recommend(self, course_name: str) -> list:
        """
        Recommend a list of courses similar to the given course name.

        Args:
            course_name (str): The name of the course to find similar courses for.

        Returns:
            A dictionary containing the top 5 recommended courses and their similarity scores.
        """
        course_name = course_name.lower()
        if course_name not in self.df['course_name'].str.lower().values:
            matches = process.extract(course_name, self.df['course_name'].str.lower().values, limit=5)
            strings = [course_name] + [match[0] for match in matches]
        else:
            strings = [course_name]

        dense_vectors = self.vectorize_strings(strings)
        similarities = self.compute_similarity(dense_vectors)

        recommended_courses = {}
        for i in range(1, len(strings)):
            name = self.df[self.df['course_name'].str.lower() == strings[i]].iloc[0]['course_name']
            url = self.df[self.df['course_name'].str.lower() == strings[i]].iloc[0]['course_url']
            similarity = round(similarities[0][i], 2)
            if similarity >= 0.30:
                recommended_courses[name] = {'url': url, 'similarity': similarity}

        sorted_courses = {k: v for k, v in sorted(recommended_courses.items(),
                                                  key=lambda item: item[1]['similarity'], reverse=True)}

        # [print(f"{k}: {v['similarity']}") for k, v in sorted_courses.items()]
        return list(sorted_courses.items())