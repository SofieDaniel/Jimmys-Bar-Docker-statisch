-- MySQL dump for Jimmy's Tapas Bar
-- Generated automatically

DROP DATABASE IF EXISTS jimmys_tapas_bar;
CREATE DATABASE jimmys_tapas_bar;
USE jimmys_tapas_bar;

-- Create users table
CREATE TABLE users (
    id VARCHAR(36) PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin', 'user') DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL
);

-- Create menu_items table
CREATE TABLE menu_items (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    detailed_description TEXT,
    price VARCHAR(20),
    category VARCHAR(100),
    origin VARCHAR(100),
    allergens TEXT,
    additives TEXT,
    preparation_method TEXT,
    ingredients TEXT,
    vegan BOOLEAN DEFAULT FALSE,
    vegetarian BOOLEAN DEFAULT FALSE,
    glutenfree BOOLEAN DEFAULT FALSE,
    order_index INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create reviews table
CREATE TABLE reviews (
    id VARCHAR(36) PRIMARY KEY,
    author_name VARCHAR(100),
    rating INT CHECK (rating >= 1 AND rating <= 5),
    review_text TEXT,
    is_approved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create contact_messages table
CREATE TABLE contact_messages (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone VARCHAR(50),
    subject VARCHAR(200),
    message TEXT NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert admin user (password: jimmy2024)
INSERT INTO users (id, username, email, password_hash, role) VALUES 
('admin-id', 'admin', 'admin@jimmys-tapasbar.de', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'admin');