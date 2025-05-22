#!/usr/bin/env python3

from random import choice as rc

from faker import Faker

from app import app
from models import db, Author, Post

fake = Faker()

with app.app_context():

    Author.query.delete()
    Post.query.delete()

    authors = []
    clickbait_titles = [
        "You Won't Believe What Happened Next",
        "Secret Tips That Doctors Don't Want You to Know",
        "Top 10 Amazing Facts About Python",
        "Guess What This Developer Did to Solve This Bug",
        "Won't Believe How Easy This Is",
        "Secret Methods for Better Code",
        "Top Reasons Why Flask is Amazing",
        "Guess Which Framework is Best"
    ]
    
    # Create valid phone numbers (exactly 10 digits)
    for n in range(25):
        # Generate exactly 10 digits for phone number
        phone_digits = ''.join([str(fake.random_digit()) for _ in range(10)])
        author = Author(name=fake.unique.name(), phone_number=phone_digits)
        authors.append(author)

    db.session.add_all(authors)

    posts = []
    for n in range(25):
        # Content must be at least 250 characters
        # Create content by repeating text until we have at least 250 characters
        base_content = fake.paragraph(nb_sentences=10)
        content = base_content
        while len(content) < 250:
            content += " " + fake.sentence()
        
        # Summary must be maximum 250 characters
        summary = fake.text(max_nb_chars=200)  # Keep it under 250 to be safe
        
        # Choose random clickbait title
        title = rc(clickbait_titles)
        
        # Choose valid category
        category = rc(['Fiction', 'Non-Fiction'])
        
        post = Post(
            title=title, 
            content=content, 
            category=category, 
            summary=summary
        )
        posts.append(post)

    db.session.add_all(posts)
    db.session.commit()
    
    print(f"Created {len(authors)} authors and {len(posts)} posts successfully!")