--13章

CREATE TABLE board_table(
    board_id INT, AUTO_INCREMENT,
    user_name VARCHAR(100),
    comment VARCHAR(1000),
    date VARCHAR(100)
    );


-- 15章　課題１

SELECT * FROM customer_table 
JOIN order_table 
ON customer_table.customer_id = order_table.customer_id
JOIN order_detail_table
ON order_table.order_id = order_detail_table.order_id
JOIN goods_table
ON order_detail_table.goods_id = goods_table.goods_id;

SELECT * FROM order_table 
JOIN customer_table 
ON order_table.customer_id = customer_table.customer_id
JOIN order_detail_table
ON order_table.order_id = order_detail_table.order_id
JOIN goods_table
ON order_detail_table.goods_id = goods_table.goods_id;

-- 全情報
SELECT order_table.order_id, order_table.order_date, customer_table.customer_name, customer_table.address, customer_table.phone_number, order_table.payment, goods_table.goods_name, goods_table.price, order_detail_table.quantity
FROM customer_table
JOIN order_table
ON customer_table.customer_id = order_table.customer_id
JOIN order_detail_table
ON order_table.order_id = order_detail_table.order_id
JOIN goods_table
ON order_detail_table.goods_id = goods_table.goods_id;

--　佐藤一郎が発注した商品情報を取得
SELECT order_table.order_id, order_table.order_date, customer_table.customer_name, goods_table.goods_name, goods_table.price, order_detail_table.quantity
FROM customer_table
JOIN order_table
ON customer_table.customer_id = order_table.customer_id
JOIN order_detail_table
ON order_table.order_id = order_detail_table.order_id
JOIN goods_table
ON order_detail_table.goods_id = goods_table.goods_id;

--　コーラの売り上げ情報を取得
SELECT goods_table.goods_name, goods_table.price, order_detail_table.quantity, order_table.order_date
FROM order_table
JOIN order_detail_table
ON order_table.order_id = order_detail_table.order_id
JOIN goods_table
ON order_detail_table.goods_id = goods_table.goods_id;

-- 1回あたりの購入数が多い順に全商品の売上情報を取得
SELECT goods_table.goods_name, goods_table.price, order_detail_table.quantity, order_table.order_date
FROM order_table
JOIN order_detail_table
ON order_table.order_id = order_detail_table.order_id
JOIN goods_table
ON order_detail_table.goods_id = goods_table.goods_id
ORDER BY quantity DESC;