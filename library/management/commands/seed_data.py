from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from library.models import Book, BookCopy, Visitor


BOOKS = [
    ("108 Vedic Upanishads", "Ajay Kumar Chhawchharia", "18 Volumes", "Spirituality", "A-01"),
    ("2 States", "Chetan Bhagat", "2 States", "Fiction", "B-01"),
    ("3 Mistakes of My Life", "Chetan Bhagat", "3 Mistakes of My Life", "Fiction", "B-02"),
    ("4 Vedas", "R.L. Kashyap", "22 Volumes", "Spirituality", "A-02"),
    ("400 Days", "Chetan Bhagat", "400 Days", "Fiction", "B-03"),
    ("A Good Girl's Guide to Murder", "Holly Jackson", "", "Mystery", "C-01"),
    ("As Good as Dead", "Holly Jackson", "", "Mystery", "C-02"),
    ("Asura", "Anand Neelakantan", "", "Mythology", "A-03"),
    ("Atomic Habits", "James Clear", "", "Self-Help", "E-01"),
    ("Attitude is Everything", "Jeff Keller", "", "Self-Help", "E-02"),
    ("Battle of Bharaich", "Suheldev", "", "History", "F-01"),
    ("Battle of Labyrinth", "Rick Riordan", "Percy Jackson", "Fantasy", "D-01"),
    ("Can We Be Strangers Again", "Arpit Vageria", "", "Fiction", "B-04"),
    ("Catching Fire", "Suzanne Collins", "The Hunger Games", "Dystopian", "D-02"),
    ("Chanakyans Chant", "Ashwin Sanghi", "Chanakyans Chant", "Thriller", "C-03"),
    ("Clear Thinking", "Shane Parrish", "", "Self-Help", "E-03"),
    ("Competetive Success", "Unknown", "", "Self-Help", "E-04"),
    ("Control Your Emotions", "Unknown", "", "Self-Help", "E-05"),
    ("Deep Work", "Cal Newport", "", "Self-Help", "E-06"),
    ("Defy Me", "Tahereh Mafi", "", "Fiction", "B-05"),
    ("Dharmayoddha Vishnu", "Kevin Missal", "Kalki", "Mythology", "A-04"),
    ("Do Epic Shit", "Ankur Warikoo", "", "Self-Help", "E-07"),
    ("Do It Today", "Darius Foroux", "", "Self-Help", "E-08"),
    ("Dopamine Detox", "Thibaut Meurisse", "", "Self-Help", "E-09"),
    ("Economic Times", "Business Standard", "", "Non-Fiction", "F-02"),
    ("Eenadu", "Unknown", "", "Non-Fiction", "F-03"),
    ("Elon Musk", "Walter Isaacson", "", "Biography", "F-04"),
    ("Enemy in the Ranks", "Unknown", "", "Thriller", "C-04"),
    ("Everything is Fucked", "Mark Manson", "", "Self-Help", "E-10"),
    ("Fearful", "Unknown", "", "Fiction", "B-06"),
    ("Fearless", "Max Lucado", "", "Self-Help", "E-11"),
    ("Five Point Someone", "Chetan Bhagat", "Five Point Someone", "Fiction", "B-07"),
    ("Focus on What Matters", "Darius Foroux", "", "Self-Help", "E-12"),
    ("Forbes India", "Unknown", "", "Non-Fiction", "F-05"),
    ("Get Epic Shit Done", "Ankur Warikoo", "", "Self-Help", "E-13"),
    ("Girl in Room 105", "Chetan Bhagat", "Girl in Room 105", "Thriller", "C-05"),
    ("Good Girl Bad Blood", "Holly Jackson", "", "Mystery", "C-06"),
    ("Half Girlfriend", "Chetan Bhagat", "Half Girlfriend", "Fiction", "B-08"),
    ("Herd", "Mark Earls", "", "Non-Fiction", "F-06"),
    ("Hindu Newspaper", "Unknown", "", "Non-Fiction", "F-07"),
    ("Hiranya Kashyap", "Kevin Missal", "Exam Preparation", "Mythology", "A-05"),
    ("How to Become a People Magnet", "Marc Reklau", "", "Self-Help", "E-14"),
    ("How to Talk to Anyone", "Leil Lowndes", "", "Self-Help", "E-15"),
    ("How to Win Friends and Influence People", "Dale Carnegie", "", "Self-Help", "E-16"),
    ("Ignite Me", "Tahereh Mafi", "", "Fiction", "B-09"),
    ("Ikigai", "Hector Garcia", "", "Self-Help", "E-17"),
    ("Imagine Me", "Tahereh Mafi", "", "Fiction", "B-10"),
    ("Imortal India", "Amish Tripathi", "Imortal India", "Non-Fiction", "F-08"),
    ("Imortal of Meluha", "Amish Tripathi", "Shiva Trilogy", "Mythology", "A-06"),
    ("India Today", "Unknown", "", "Non-Fiction", "F-09"),
    ("Influence", "Robert Cialdini", "", "Self-Help", "E-18"),
    ("It Ends with Us", "Colleen Hoover", "", "Romance", "B-11"),
    ("It Starts with Us", "Colleen Hoover", "", "Romance", "B-12"),
    ("Karna", "Kevin Missal", "Karna", "Mythology", "A-07"),
    ("King of Envy", "Ana Huang", "", "Romance", "B-13"),
    ("King of Gluttony", "Ana Huang", "", "Romance", "B-14"),
    ("King of Greed", "Ana Huang", "", "Romance", "B-15"),
    ("King of Lust", "Ana Huang", "", "Romance", "B-16"),
    ("King of Pride", "Ana Huang", "", "Romance", "B-17"),
    ("King of Sloth", "Ana Huang", "", "Romance", "B-18"),
    ("Kings of Wrath", "Ana Huang", "", "Romance", "B-19"),
    ("Krishna Key", "Ashwin Sanghi", "Krishna Key", "Thriller", "C-07"),
    ("Lanka", "Amish Tripathi", "Ram Chandra Series", "Mythology", "A-08"),
    ("Last Olympian", "Rick Riordan", "Percy Jackson", "Fantasy", "D-03"),
    ("Mahabharata", "M.N. Dutt", "2 Languages", "Mythology", "A-09"),
    ("Mahayoddha Shiva", "Kevin Missal", "Kalki", "Mythology", "A-10"),
    ("Manifest", "Roxie Nafousi", "", "Self-Help", "E-19"),
    ("Manorama Year Book", "Unknown", "", "Non-Fiction", "F-10"),
    ("Mastery", "Robert Greene", "", "Self-Help", "E-20"),
    ("Meditations", "Marcus Aurelius", "", "Philosophy", "E-21"),
    ("Meghanadh", "Kevin Missal", "Meghanadh", "Mythology", "A-11"),
    ("Mindset", "Carol S. Dweck", "", "Self-Help", "E-22"),
    ("Moking Jay", "Suzanne Collins", "The Hunger Games", "Dystopian", "D-04"),
    ("Narasimha", "Kevin Missal", "Narasimha", "Mythology", "A-12"),
    ("Oath of Vayuputras", "Amish Tripathi", "Shiva Trilogy", "Mythology", "A-13"),
    ("One Arranged Murder", "Chetan Bhagat", "One Arranged Murder", "Thriller", "C-08"),
    ("One Night in the Call Center", "Chetan Bhagat", "", "Fiction", "B-20"),
    ("Panlo Coelho", "Paulo Coelho", "", "Fiction", "B-21"),
    ("Power", "Robert Greene", "", "Self-Help", "E-23"),
    ("Powerfull", "Patty McCord", "", "Self-Help", "E-24"),
    ("Powerless", "Lauren Roberts", "", "Fiction", "B-22"),
    ("Prahlad", "Kevin Missal", "Narasimha", "Mythology", "A-14"),
    ("Psycho Cybernetics", "Maxwell Maltz", "", "Self-Help", "E-25"),
    ("Raavan", "Amish Tripathi", "Ram Chandra Series", "Mythology", "A-15"),
    ("Ram", "Amish Tripathi", "Ram Chandra Series", "Mythology", "A-16"),
    ("Ramayana of Valmiki", "Ramashraya Sharma", "2 Languages", "Mythology", "A-17"),
    ("Reckless", "Lauren Roberts", "", "Fiction", "B-23"),
    ("Restore Me", "Tahereh Mafi", "", "Fiction", "B-24"),
    ("Rich Dad Poor Dad", "Robert T. Kiyosaki", "", "Finance", "E-26"),
    ("Rich Routines", "Unknown", "", "Self-Help", "E-27"),
    ("Sapiens", "Yuval Noah Harari", "", "Non-Fiction", "F-11"),
    ("Sathyoddha Bhrama", "Kevin Missal", "Kalki", "Mythology", "A-18"),
    ("Secret of Nagas", "Amish Tripathi", "Shiva Trilogy", "Mythology", "A-19"),
    ("Shatter Me", "Tahereh Mafi", "", "Fiction", "B-25"),
    ("Sita", "Amish Tripathi", "Ram Chandra Series", "Mythology", "A-20"),
    ("Social Equations Patrick King", "Patrick King", "", "Self-Help", "E-28"),
    ("Srimad Bhagavatham", "Bhaktivedanta Swami", "18 Volumes", "Spirituality", "A-21"),
    ("Steve Jobs", "Walter Isaacson", "", "Biography", "F-12"),
    ("Talking with Psychopaths and Savages", "Christopher Berry-Dee", "", "Non-Fiction", "F-13"),
    ("Teachings of Lord Chaitanya", "Bhaktivedanta Swami", "", "Spirituality", "A-22"),
    ("The Alchemist", "Paulo Coelho", "", "Fiction", "B-26"),
    ("The Art of Being Alone", "Renuka Singh", "", "Self-Help", "E-29"),
    ("The Art of Dealing with People", "Les Giblin", "", "Self-Help", "E-30"),
    ("The Art of Letting Go", "Darius Foroux", "", "Self-Help", "E-31"),
    ("The Art of Not Over Thinking", "Unknown", "", "Self-Help", "E-32"),
    ("The Art of Persuasion", "Bob Burg", "", "Self-Help", "E-33"),
    ("The Art of Reading People", "Unknown", "", "Self-Help", "E-34"),
    ("The Art of Spending Money", "Unknown", "", "Finance", "E-35"),
    ("The Billion Dollar Secret", "Rafael Badziag", "", "Finance", "E-36"),
    ("The Communication Book 44 Ideas", "Mikael Krogerus", "", "Self-Help", "E-37"),
    ("The Courage to Be Disliked", "Ichiro Kishimi", "", "Self-Help", "E-38"),
    ("The Hunger Games", "Suzanne Collins", "The Hunger Games", "Dystopian", "D-05"),
    ("The Laws of Human Nature", "Robert Greene", "", "Self-Help", "E-39"),
    ("The Lightning Thief", "Rick Riordan", "Percy Jackson", "Fantasy", "D-06"),
    ("The Magic", "Rhonda Byrne", "", "Self-Help", "E-40"),
    ("The Mountain is You", "Brianna Wiest", "", "Self-Help", "E-41"),
    ("The New One Minute Manager", "Ken Blanchard", "", "Self-Help", "E-42"),
    ("The Power of Your Subconscious Mind", "Joseph Murphy", "", "Self-Help", "E-43"),
    ("The Psychology of Money", "Morgan Housel", "", "Finance", "E-44"),
    ("The Sea of Monsters", "Rick Riordan", "Percy Jackson", "Fantasy", "D-07"),
    ("The Secret", "Rhonda Byrne", "", "Self-Help", "E-45"),
    ("The Subtle Art of Not Giving a Fuck", "Mark Manson", "", "Self-Help", "E-46"),
    ("The Titan's Curse", "Rick Riordan", "Percy Jackson", "Fantasy", "D-08"),
    ("The Week", "Unknown", "", "Non-Fiction", "F-14"),
    ("Think and Grow Rich", "Napoleon Hill", "", "Finance", "E-47"),
    ("Three Men in a Boat", "Jerome K. Jerome", "", "Classic Fiction", "B-27"),
    ("TOI", "General News", "", "Non-Fiction", "F-15"),
    ("Twisted Games", "Ana Huang", "", "Romance", "B-28"),
    ("Twisted Hate", "Ana Huang", "", "Romance", "B-29"),
    ("Twisted Lies", "Ana Huang", "", "Romance", "B-30"),
    ("Twisted Love", "Ana Huang", "", "Romance", "B-31"),
    ("Unravel Me", "Tahereh Mafi", "", "Fiction", "B-32"),
    ("Vault of Vishnu", "Ashwin Sanghi", "Vault of Vishnu", "Thriller", "C-09"),
    ("Who Saved India", "Amish Tripathi", "Suheldev", "History", "F-16"),
    ("Wings of Fire", "A.P.J. Abdul Kalam", "", "Biography", "F-17"),
    ("Zero to One", "Peter Thiel", "", "Finance", "E-48"),
    ("Poirot Series", "Agatha Christie", "", "Mystery", "C-10"),
]

VISITORS = [
    ("Ananya Sharma", 28, "12, MG Road, Hyderabad 500001", "ananya@email.com", "9876543210", "XXXX XXXX 4521"),
    ("Rohan Mehta", 35, "45, Banjara Hills, Hyderabad 500034", "rohan.m@email.com", "8765432109", "XXXX XXXX 7832"),
    ("Priya Iyer", 22, "8, Jubilee Hills, Hyderabad 500033", "priya.iyer@email.com", "7654321098", "XXXX XXXX 1190"),
]


class Command(BaseCommand):
    help = 'Seed the database with all SVG Book World books, visitors, and a superuser'

    def handle(self, *args, **kwargs):
        # Create superuser
        if not User.objects.filter(username='librarian').exists():
            User.objects.create_superuser('librarian', 'librarian@svgbookworld.com', 'library@123')
            self.stdout.write(self.style.SUCCESS('✓ Superuser created: librarian / library@123'))
        else:
            self.stdout.write('  Superuser already exists.')

        # Seed books
        created_books = 0
        for i, (title, author, series, genre, shelf) in enumerate(BOOKS):
            isbn = f'SVG-{str(i+1).zfill(4)}'
            search_q = title.replace(' ', '+').replace("'", '')
            cover_url = f'https://covers.openlibrary.org/b/title/{search_q}-M.jpg'
            book, created = Book.objects.get_or_create(
                isbn=isbn,
                defaults=dict(
                    title=title, author=author, series=series,
                    genre=genre, shelf_location=shelf,
                    publication_year=2020, cover_url=cover_url,
                )
            )
            if created:
                BookCopy.objects.create(book=book, copy_code=f'{isbn}a')
                created_books += 1

        self.stdout.write(self.style.SUCCESS(f'✓ {created_books} books seeded ({Book.objects.count()} total)'))

        # Seed visitors
        created_visitors = 0
        for name, age, address, email, phone, aadhaar in VISITORS:
            _, created = Visitor.objects.get_or_create(
                email=email,
                defaults=dict(full_name=name, age=age, address=address, phone=phone, aadhaar_masked=aadhaar)
            )
            if created:
                created_visitors += 1

        self.stdout.write(self.style.SUCCESS(f'✓ {created_visitors} visitors seeded ({Visitor.objects.count()} total)'))
        self.stdout.write(self.style.SUCCESS('\n🎉 SVG Book World is ready! Run: python manage.py runserver'))
