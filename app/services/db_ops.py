from app.models import User, CourseEmbedding
from app import db

def get_user_by_email(email):
    return User.query.filter_by(email=email).first()

def get_user_by_id(user_id):
    return User.query.filter_by(id=user_id).first()

def get_all_users():
    return User.query.all()

def create_user(email, password):
    user = User(email=email, password=password)
    db.session.add(user)
    db.session.commit()
    return user

def delete_user(user):
    db.session.delete(user)
    db.session.commit()

def delete_all_users():
    users = get_all_users()
    for user in users:
        delete_user(user)
    db.session.commit()

def create_course_embedding(course_name, embedding):
    course_embedding = CourseEmbedding(course_name=course_name, embedding=embedding)
    db.session.add(course_embedding)
    db.session.commit()
    return course_embedding

def get_embedding_by_course_name(course_name):
    return CourseEmbedding.query.filter_by(course_name=course_name).first()

def get_all_course_embeddings():
    return CourseEmbedding.query.all()

def update_course_embedding(course_name, new_embedding):
    course_embedding = get_embedding_by_course_name(course_name)
    if course_embedding:
        course_embedding.embedding = new_embedding
        db.session.commit()
    else:
        create_course_embedding(course_name, new_embedding)

def delete_course_embedding(course_name):
    course_embedding = get_embedding_by_course_name(course_name)
    if course_embedding:
        db.session.delete(course_embedding)
        db.session.commit()

def delete_all_course_embeddings():
    embeddings = get_all_course_embeddings()
    for embedding in embeddings:
        delete_course_embedding(embedding.course_name)
    db.session.commit()

def bulk_insert_embeddings(embeddings):
    db.session.bulk_insert_mappings(CourseEmbedding, embeddings)
    db.session.commit()

def get_all_course_names():
    return [course.course_name for course in CourseEmbedding.query.with_entities(CourseEmbedding.course_name).all()]