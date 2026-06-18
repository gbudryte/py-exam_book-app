-- ==========================================
-- 1. SEED USERS (Visi slaptažodžiai po maišos yra: 'Test123')
-- ==========================================
INSERT INTO users (id, name, email, password_hash, role) VALUES
(1, 'Tomas Adminas', 'admin@example.com', '$2b$12$6R2b0SBlxV23fD6K/EaIe.T0gXW/T09M9hK9wJ1hE2rO3wZqXyF5q', 'ADMIN'),
(2, 'Jonas Vartotojas', 'jonas@example.com', '$2b$12$6R2b0SBlxV23fD6K/EaIe.T0gXW/T09M9hK9wJ1hE2rO3wZqXyF5q', 'USER'),
(3, 'Lina Skaitytoja', 'lina@example.com', '$2b$12$6R2b0SBlxV23fD6K/EaIe.T0gXW/T09M9hK9wJ1hE2rO3wZqXyF5q', 'USER');

-- ==========================================
-- 2. SEED CATEGORIES (5 kategorijos)
-- ==========================================
INSERT INTO categories (id, name, created_by_user_id) VALUES
(1, 'Sci-Fi & Fantasy', 1),
(2, 'Biography & History', 1),
(3, 'Business & Finance', 1),
(4, 'Mystery & Thriller', 1),
(5, 'Technology & Science', 1);

-- ==========================================
-- 3. SEED BOOKS (Po 10 knygų kiekvienam vartotojui = iš viso 30)
-- ==========================================

-- --- 10 Knygų, kurias sukūrė Vartotojas 1 (Admin - Tomas) ---
INSERT INTO books (name, author, category_id, description, rating, created_by_user_id) VALUES
('Dune', 'Frank Herbert', 1, 'Classic sci-fi epic on a desert planet.', 5, 1),
('Steve Jobs', 'Walter Isaacson', 2, 'Biography of Apple co-founder.', 4, 1),
('The Lean Startup', 'Eric Ries', 3, 'How constant innovation creates radically successful businesses.', 5, 1),
('The Girl with the Dragon Tattoo', 'Stieg Larsson', 4, 'Dark psychological thriller.', 4, 1),
('Clean Code', 'Robert C. Martin', 5, 'A handbook of agile software craftsmanship.', 5, 1),
('The Hobbit', 'J.R.R. Tolkien', 1, 'Prequel to the Lord of the Rings.', 5, 1),
('Sapiens', 'Yuval Noah Harari', 2, 'A brief history of humankind.', 4, 1),
('Thinking, Fast and Slow', 'Daniel Kahneman', 3, 'System 1 and System 2 thinking.', 4, 1),
('Gone Girl', 'Gillian Flynn', 4, 'A twisted psychological mystery.', 3, 1),
('Introduction to Algorithms', 'Thomas H. Cormen', 5, 'The bible of computer science algorithms.', 5, 1);

-- --- 10 Knygų, kurias sukūrė Vartotojas 2 (Jonas) ---
INSERT INTO books (name, author, category_id, description, rating, created_by_user_id) VALUES
('Neuromancer', 'William Gibson', 1, 'The foundational cyberpunk novel.', 4, 2),
('Alexander Hamilton', 'Ron Chernow', 2, 'Biography of the US founding father.', 5, 2),
('Zero to One', 'Peter Thiel', 3, 'Notes on startups, or how to build the future.', 4, 2),
('Sherlock Holmes Collection', 'Arthur Conan Doyle', 4, 'Classic detective mysteries.', 5, 2),
('You Don\'t Know JS', 'Kyle Simpson', 5, 'Deep dive into JavaScript mechanics.', 4, 2),
('Foundation', 'Isaac Asimov', 1, 'The rise and fall of a galactic empire.', 5, 2),
('The Wright Brothers', 'David McCullough', 2, 'The story of aviation pioneers.', 4, 2),
('The Intelligent Investor', 'Benjamin Graham', 3, 'The definitive book on value investing.', 5, 2),
('The Da Vinci Code', 'Dan Brown', 4, 'Fast-paced religious conspiracy thriller.', 3, 2),
('Design Patterns', 'Erich Gamma', 5, 'Elements of reusable object-oriented software.', 5, 2);

-- --- 10 Knygų, kurias sukūrė Vartotojas 3 (Lina) ---
INSERT INTO books (name, author, category_id, description, rating, created_by_user_id) VALUES
('Hyperion', 'Dan Simmons', 1, 'Space opera inspired by Canterbury Tales.', 5, 3),
('Napoleon: A Life', 'Andrew Roberts', 2, 'Comprehensive biography of the emperor.', 4, 3),
('Rich Dad Poor Dad', 'Robert Kiyosaki', 3, 'Personal finance classic.', 3, 3),
('Big Little Lies', 'Liane Moriarty', 4, 'Murder mystery wrapped in suburban secrets.', 4, 3),
('Refactoring', 'Martin Fowler', 5, 'Improving the design of existing code.', 5, 3),
('The Name of the Wind', 'Patrick Rothfuss', 1, 'A beautifully written fantasy epic.', 5, 3),
('Team of Rivals', 'Doris Kearns Goodwin', 2, 'The political genius of Abraham Lincoln.', 5, 3),
('Good to Great', 'Jim Collins', 3, 'Why some companies make the leap and others don\'t.', 4, 3),
('The Silent Patient', 'Alex Michaelides', 4, 'A shocking psychological thriller.', 4, 3),
('The Pragmatic Programmer', 'Andrew Hunt', 5, 'Your journey to mastery.', 5, 3);