CREATE TABLE sales(
   Product VARCHAR(20) NOT NULL,
   Price INT NOT NULL,
   SaleDate DATE NOT NULL,
   product_attributes JSONB
);

INSERT INTO sales(Product, Price, SaleDate, product_attributes)
VALUES
    ('Smartphone', 500, '2021-01-01', '{"brand": "BrandA", "model": "ModelX", "color": "Black", "storage_capacity": "64GB"}'),
    ('Laptop', 1000, '2021-02-01', '{"brand": "BrandB", "model": "ModelY", "color": "Silver", "storage_capacity": "256GB", "screen_size": "15.6 inch"}'),
    ('Tablet', 300, '2021-03-01', '{"brand": "BrandC", "model": "ModelZ", "color": "Gold", "storage_capacity": "128GB", "screen_size": "10.2 inch"}'),
    ('Desktop', 1200, '2021-04-01', '{"brand": "BrandD", "model": "ModelA", "color": "White", "storage_capacity": "512GB"}'),
    ('Smartwatch', 250, '2021-05-01', '{"brand": "BrandE", "model": "ModelB", "color": "Rose Gold"}'),
    ('Headphones', 150, '2021-06-01', '{"brand": "BrandF", "model": "ModelC", "color": "Black"}'),
    ('Camera', 800, '2021-07-01', '{"brand": "BrandG", "model": "ModelD", "color": "Silver"}'),
    ('TV', 1500, '2021-08-01', '{"brand": "BrandH", "model": "ModelE", "color": "Black", "screen_size": "55 inch"}'),
    ('Speakers', 200, '2021-09-01', '{"brand": "BrandI", "model": "ModelF", "color": "Red"}'),
    ('Gaming Console', 400, '2021-10-01', '{"brand": "BrandJ", "model": "ModelG", "color": "Black"}'),
    ('Smart Home Device', 100, '2021-11-01', '{"brand": "BrandK", "model": "ModelH", "color": "White"}'),
    ('External Hard Drive', 150, '2021-12-01', '{"brand": "BrandL", "model": "ModelI", "color": "Silver", "storage_capacity": "1TB"}'),
    ('Wireless Earbuds', 200, '2022-01-01', '{"brand": "BrandM", "model": "ModelJ", "color": "Black"}'),
    ('Tablet', 300, '2022-02-01', '{"brand": "BrandN", "model": "ModelK", "color": "Gold", "storage_capacity": "256GB", "screen_size": "11 inch"}'),
    ('Printer', 150, '2022-03-01', '{"brand": "BrandO", "model": "ModelL", "color": "White"}'),
    ('Smart Scale', 50, '2022-04-01', '{"brand": "BrandP", "model": "ModelM", "color": "Black"}'),
    ('Smart Thermostat', 80, '2022-05-01', '{"brand": "BrandQ", "model": "ModelN", "color": "Silver"}'),
    ('Wireless Router', 100, '2022-06-01', '{"brand": "BrandR", "model": "ModelO", "color": "Black"}'),
    ('Fitness Tracker', 120, '2022-07-01', '{"brand": "BrandS", "model": "ModelP", "color": "Purple"}'),
    ('Wireless Speaker', 180, '2022-08-01', '{"brand": "BrandT", "model": "ModelQ", "color": "Blue"}'),
    ('External SSD', 250, '2022-09-01', '{"brand": "BrandU", "model": "ModelR", "color": "Silver", "storage_capacity": "512GB"}');
