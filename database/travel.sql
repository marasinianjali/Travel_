create database travel;
use travel;


SHOW TABLES;
DESCRIBE categories;
ALTER TABLE categories MODIFY id BIGINT AUTO_INCREMENT;
SELECT * FROM User;

CREATE TABLE User (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(55) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    address VARCHAR(255),
    gender ENUM('male', 'female', 'other') NULL,
    status ENUM('married', 'unmarried') DEFAULT 'married',
    dob DATE,
    bio TEXT,
    theme ENUM('light', 'dark') DEFAULT 'light'
);

-- Wishlist table for user 
CREATE TABLE Wishlist (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    destination_name VARCHAR(100) NOT NULL,
    description TEXT,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES User(id) ON DELETE CASCADE
);

SELECT * FROM Wishlist;

-- Trips table for user
CREATE TABLE Trip (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    destination VARCHAR(100) NOT NULL,
    start_date DATE,
    end_date DATE,
    status ENUM('planned', 'ongoing', 'completed') DEFAULT 'planned',
    FOREIGN KEY (user_id) REFERENCES User(id) ON DELETE CASCADE
);

SELECT * FROM Trip;


-- Notifications table for user
CREATE TABLE Notification (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    message TEXT NOT NULL,
    notification_type ENUM('deal', 'flight', 'safety'),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_read BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES User(id) ON DELETE CASCADE
);

-- For user social and community 
CREATE TABLE follows (
    id INT AUTO_INCREMENT PRIMARY KEY,
    follower_id INT NOT NULL,
    followed_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (follower_id) REFERENCES User(id) ON DELETE CASCADE,
    FOREIGN KEY (followed_id) REFERENCES User(id) ON DELETE CASCADE,
    UNIQUE (follower_id, followed_id) -- Prevent duplicate follows
);


-- Table for Discussion Groups
CREATE TABLE discussion_groups (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_by INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES User(id) ON DELETE CASCADE
);
CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT
);
-- Table for Posts in Discussion Groups
CREATE TABLE group_posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    group_id INT NOT NULL,
    user_id INT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (group_id) REFERENCES discussion_groups(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES User(id) ON DELETE CASCADE
);
ALTER TABLE group_posts ADD COLUMN image VARCHAR(100) NULL;
ALTER TABLE group_posts ADD COLUMN video VARCHAR(100) NULL;
ALTER TABLE group_posts 
    ADD COLUMN category_id INT NULL,
    ADD FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL;
ALTER TABLE group_posts 
    ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
    
    
-- Table for Tags/Hashtags
CREATE TABLE tags (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for Associating Tags with Posts
CREATE TABLE post_tags (
    id INT AUTO_INCREMENT PRIMARY KEY,
    post_id INT NOT NULL,
    tag_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES group_posts(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE,
    UNIQUE (post_id, tag_id) -- Prevent duplicate tag assignments
);




RENAME TABLE TourPackages TO TourPackage;

create table Admin(
	admin_id INT PRIMARY KEY AUTO_INCREMENT,
	username varchar(100) NOT NULL,
	email varchar(55) NOT NULL,
	password varchar(255) NOT NULL,
	role ENUM('Super Admin', 'Editor')DEFAULT 'Super Admin',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE TourismCompany(
	company_id INT PRIMARY KEY AUTO_INCREMENT,
	user_name varchar(100) NOT NULL,
    user_phone varchar(20) NOT NULL,
    user_email varchar(55) NOT NULL,
    company_name VARCHAR(255) NOT NULL,
    company_phone VARCHAR(255) NOT NULL,
    company_address VARCHAR(255) NOT NULL
);
ALTER TABLE TourismCompany
ADD COLUMN password VARCHAR(128) NOT NULL;
-- to show enable disable accounts 
ALTER TABLE TourismCompany
ADD COLUMN is_active TINYINT(1) DEFAULT 1;
ALTER TABLE TourismCompany
ADD COLUMN user_id INT,
ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES User(id) ON DELETE CASCADE;


 

CREATE TABLE TourPackage (
    package_id INT PRIMARY KEY AUTO_INCREMENT,
    package_name VARCHAR(255) NOT NULL,
    company_name VARCHAR(255) NOT NULL,	
    date DATE,
    description TEXT,
    amount DECIMAL(10,2) NOT NULL CHECK (amount > 0),
    duration INT NOT NULL CHECK (duration > 0),  
    country VARCHAR(255) NOT NULL,
    city VARCHAR(255) NOT NULL,
    tour_type VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
ALTER TABLE TourPackage 
ADD COLUMN company_id INT,
ADD CONSTRAINT fk_company
    FOREIGN KEY (company_id) REFERENCES TourismCompany(company_id);

SELECT * FROM TourPackage;
ALTER TABLE TourPackage ADD COLUMN company_name VARCHAR(255) NOT NULL;
UPDATE TourPackage SET company_name = 'Default Company Name' WHERE company_name IS NULL;
ALTER TABLE TourPackage ADD COLUMN is_approved BOOLEAN DEFAULT FALSE;

#need is_approved for to see if admin approved the tour package or not
SELECT * FROM TourPackage WHERE company_name IS NULL;
SHOW COLUMNS FROM TourPackage LIKE 'company_name';
SHOW CREATE TABLE TourPackages;
ALTER TABLE TourPackage DROP COLUMN company_name;


DESCRIBE Guides;

CREATE TABLE Guides (
    guide_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    dob DATE,
    gender VARCHAR(20) NOT NULL,
    about_us VARCHAR(200) NOT NULL,
    language VARCHAR(255) NOT NULL,
    amount  DECIMAL(10,2) NOT NULL CHECK (amount > 0),
    image longblob,
    location VARCHAR(100) NOT NULL DEFAULT 'Nepal - Kathmandu',
    phone VARCHAR(20) NOT NULL,
    experience INT NOT NULL, 
    expertise TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
ALTER TABLE Guides
ADD COLUMN location VARCHAR(100) NOT NULL DEFAULT 'Nepal - Kathmandu';

SELECT * FROM Guides;
-- not using for a now 
CREATE TABLE HotelBooking(
	hotel_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
	hotel_name VARCHAR (255) NOT NULL,
    amount DECIMAL(10,2) NOT NULL CHECK (amount > 0),
    room_type VARCHAR(20) NOT NULL,
	photo longblob,
    hotel_address VARCHAR (255) NOT NULL,
    contact_number VARCHAR(20) NOT NULL,
    total_person INT NOT NULL,
    arrive_time DATETIME NOT NULL,
    checkout_time DATETIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(id) ON DELETE CASCADE
);


CREATE TABLE Bookings (
    booking_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    hotel_id INT  NULL,
    user_name VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    total_members INT NOT NULL,
    package_id INT NOT NULL,
    guide_id INT NULL,  
    booking_date DATE NOT NULL,
    booking_details varchar (255),
    status ENUM('Pending', 'Confirmed', 'Cancelled') DEFAULT 'Pending',
    promecode VARCHAR(50) NULL,
    pickup_location VARCHAR(255) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(id) ON DELETE CASCADE,
    FOREIGN KEY (hotel_id) REFERENCES HotelBooking(hotel_id) ON DELETE CASCADE,
    FOREIGN KEY (package_id) REFERENCES TourPackage(package_id) ON DELETE CASCADE,
    FOREIGN KEY (guide_id) REFERENCES Guides(guide_id) ON DELETE SET NULL
);

ALTER TABLE hotelbooking_hotelbooking
ADD notify_admin TINYINT(1) NOT NULL DEFAULT 0,
ADD status VARCHAR(50) NOT NULL DEFAULT 'Pending',
ADD amenity VARCHAR(100) NOT NULL DEFAULT 'wifi';


CREATE TABLE Reviews (
    review_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    package_id INT DEFAULT NULL,
    guide_id INT DEFAULT NULL,
    hotel_id INT DEFAULT NULL,
    company_id INT DEFAULT NULL,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    review_text TEXT,
    photo longblob,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES User(id) ON DELETE CASCADE,
    FOREIGN KEY (hotel_id) REFERENCES HotelBooking(hotel_id) ON DELETE CASCADE,
    FOREIGN KEY (package_id) REFERENCES TourPackage(package_id) ON DELETE CASCADE,
     FOREIGN KEY (company_id) REFERENCES TourismCompany(company_id) ON DELETE CASCADE,
    FOREIGN KEY (guide_id) REFERENCES Guides(guide_id) ON DELETE CASCADE
);



CREATE TABLE HotelUser(
	hoteluser_id INT PRIMARY KEY AUTO_INCREMENT,
    hotel_type VARCHAR(20) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    mobile_number VARCHAR(20) NULL,
    photo longblob,
    address VARCHAR(200) NOT NULL,
	email VARCHAR(200) NOT NULL UNIQUE,
    services VARCHAR(255) NOT NULL,
    parking TINYINT(1) NOT NULL DEFAULT 0  -- 0 for No, 1 for Yes
    
);

-- --expenses
-- CREATE TABLE expenses_tripbudget
show tables;

CREATE TABLE Payments (
    payment_id INT PRIMARY KEY AUTO_INCREMENT,
    booking_id INT UNIQUE NOT NULL,
	hotel_id INT DEFAULT NULL,
	guide_id INT ,
    name VARCHAR(255),   -- user 
	hotel_name VARCHAR(255),  -- Storing hotel name
    phone_number VARCHAR(20), -- Storing hotel contact number
    amount DECIMAL(10,2) NOT NULL,
    payment_method ENUM('Credit Card', 'Debit Card', 'PayPal', 'Bank Transfer') NOT NULL,
    status ENUM('Pending', 'Completed', 'Failed') DEFAULT 'Pending',
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (booking_id) REFERENCES Bookings(booking_id) ON DELETE CASCADE,
    FOREIGN KEY (guide_id) REFERENCES Guides(guide_id) ON DELETE CASCADE
	-- FOREIGN KEY (name) REFERENCES Bookings(name) ON DELETE CASCADE
--     FOREIGN KEY (hotel_name) REFERENCES HotelBookings(hotel_name) ON DELETE CASCADE,
--     FOREIGN KEY (phone_number) REFERENCES HotelBookings(phone_number) ON DELETE CASCADE,
--     FOREIGN KEY (amount) REFERENCES Bookings(amount) ON DELETE CASCADE
);