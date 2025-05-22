from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators
    @validates('name')
    def validate_name(self, key, name):
        """Validate that name is not empty and is unique"""
        if not name or name.strip() == '':
            raise ValueError("Author name is required and cannot be empty")
        
        # Check for uniqueness
        existing_author = Author.query.filter_by(name=name).first()
        if existing_author and existing_author.id != self.id:
            raise ValueError(f"Author with name '{name}' already exists")
        
        return name

    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        """Validate that phone number is exactly ten digits"""
        if phone_number is not None:
            # Remove any spaces or formatting
            digits_only = ''.join(filter(str.isdigit, phone_number))
            
            if len(digits_only) != 10:
                raise ValueError("Phone number must be exactly ten digits")
            
            # Check if all characters are digits
            if not phone_number.replace(' ', '').replace('-', '').replace('(', '').replace(')', '').isdigit():
                raise ValueError("Phone number must contain only digits")
        
        return phone_number

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
    @validates('title')
    def validate_title(self, key, title):
        """Validate that title is not empty and contains clickbait keywords"""
        if not title or title.strip() == '':
            raise ValueError("Post title is required and cannot be empty")
        
        # Check for clickbait keywords
        clickbait_words = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(keyword in title for keyword in clickbait_words):
            raise ValueError("Post title must contain one of: 'Won't Believe', 'Secret', 'Top', 'Guess'")
        
        return title

    @validates('content')
    def validate_content(self, key, content):
        """Validate that content is at least 250 characters long"""
        if content is not None and len(content) < 250:
            raise ValueError("Post content must be at least 250 characters long")
        
        return content

    @validates('summary')
    def validate_summary(self, key, summary):
        """Validate that summary is maximum 250 characters"""
        if summary is not None and len(summary) > 250:
            raise ValueError("Post summary must be a maximum of 250 characters")
        
        return summary

    @validates('category')
    def validate_category(self, key, category):
        """Validate that category is either Fiction or Non-Fiction"""
        if category is not None:
            valid_categories = ['Fiction', 'Non-Fiction']
            if category not in valid_categories:
                raise ValueError("Post category must be either 'Fiction' or 'Non-Fiction'")
        
        return category

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'