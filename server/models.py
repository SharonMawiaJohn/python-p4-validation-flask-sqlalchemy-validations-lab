from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def validate_name(self, key, author_name):
        if not author_name:
            raise ValueError("All authors must have a name")
        
        existing_author = Author.query.filter_by(name=author_name).first()
        if existing_author:
            raise ValueError(f"Author with name '{author_name}' already exists")

        return author_name
    
    @validates('phone_number')
    def validate_phone_number(self, key, author_number):
        if len(author_number) != 10:
            raise ValueError("The phone number MUST be 10 digits")
        
        if not author_number.isdigit():
            raise ValueError("The phone number must contain digits only")
        
        return author_number
    
    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('content')
    def validate_content(self, key, content_value):
        if not len(content_value) >= 250:
            raise ValueError("The post content MUST be atleast 250 characters long")
        
        return content_value

    @validates('summary')
    def validate_summary(self, key, summary_value):
        if len(summary_value) > 250:
            raise ValueError("Post summary should be a maximum of 250 characters")
        
        return summary_value
    
    @validates('category')
    def validate_category(self, key, category_type):
        if category_type != 'Fiction' and category_type != 'Non-Fiction':
            raise ValueError("Post category can only be either Fiction or Non-Fiction")
        
        return category_type
    
    @validates('title')
    def validate_title(self, key, post_title):
        clickbait_phrases = ["Won't Believe", "Secret", "Top", "Guess"]
        if not post_title or post_title.strip() == '':
            raise ValueError("Title CANNOT be empty")
        
        if not any(phrase in post_title for phrase in clickbait_phrases):
            raise ValueError("Your title is not click-baity")
        
        return post_title
        
    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
