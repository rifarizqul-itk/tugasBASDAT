CREATE DATABASE sales_db;
USE sales_db;

CREATE TABLE IF NOT EXISTS customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15),
    address TEXT,
    birthdate DATE COMMENT 'Tanggal lahir pelanggan'
);

CREATE TABLE IF NOT EXISTS products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL
);

CREATE TABLE IF NOT EXISTS orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS order_details (
    order_detail_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) AS (quantity * price) STORED,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
        ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
        ON DELETE CASCADE
);

INSERT INTO customers (name, email, phone, address, birthdate) VALUES
('Budi Santoso', 'budi@example.com', '081234567890', 'Jl. Mawar No. 10', '1998-05-12'),
('Siti Aminah', 'siti@example.com', '082345678901', 'Jl. Melati No. 22', '1995-11-03'),
('Agus Wijaya', 'agus@example.com', '083456789012', 'Jl. Kenanga No. 7', '1999-01-25'),
('Dewi Lestari', 'dewi@example.com', '084567890123', 'Jl. Dahlia No. 3', '2000-04-09'),
('Rizky Pratama', 'rizky@example.com', '085678901234', 'Jl. Anggrek No. 15', '1997-09-18');

INSERT INTO products (name, description, price, stock) VALUES
('Laptop Asus X441', 'Laptop untuk kebutuhan harian', 5500000, 12),
('Mouse Logitech M330', 'Mouse wireless silent click', 180000, 50),
('Keyboard Rexus K9', 'Mechanical keyboard blue switch', 350000, 30),
('Monitor Samsung 24 Inch', 'Full HD 75Hz monitor', 1500000, 20),
('Headset HyperX', 'Gaming headset bass kuat', 700000, 15);

INSERT INTO orders (customer_id, total_amount, order_date) VALUES
(1, 5680000, '2025-01-05 10:30:00'),
(2, 1530000, '2025-01-10 14:15:00'),
(3, 720000,  '2025-01-15 09:50:00'),
(4, 1500000, '2025-01-20 16:20:00'),
(5, 5850000, '2025-01-22 11:10:00');

INSERT INTO order_details (order_id, product_id, quantity, price) VALUES
(1, 1, 1, 5500000),
(1, 2, 1, 180000),
(2, 4, 1, 1500000),
(2, 2, 1, 30000),
(3, 3, 2, 350000),
(4, 4, 1, 1500000),
(5, 1, 1, 5500000),
(5, 5, 1, 350000);