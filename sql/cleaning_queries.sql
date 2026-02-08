-- 1) Item-level fact table
DROP TABLE IF EXISTS fact_order_items;
CREATE TABLE fact_order_items AS
SELECT
    oi.order_id,
    o.customer_id,
    c.customer_unique_id,
    o.order_status,
    o.order_purchase_timestamp                             AS order_purchase_ts,
    DATE(o.order_purchase_timestamp)                       AS order_purchase_date,
    STRFTIME('%Y-%m', o.order_purchase_timestamp)          AS order_purchase_ym,

    oi.order_item_id,
    oi.product_id,
    p.product_category_name,
    t.product_category_name_english,
    oi.seller_id,
    oi.shipping_limit_date,
    oi.price,
    oi.freight_value,

    c.customer_city,
    c.customer_state
FROM olist_order_items_dataset oi
LEFT JOIN olist_orders_dataset o
    ON oi.order_id = o.order_id
LEFT JOIN olist_products_dataset p
    ON oi.product_id = p.product_id
LEFT JOIN product_category_name_translation t
    ON p.product_category_name = t.product_category_name
LEFT JOIN olist_customers_dataset c
    ON o.customer_id = c.customer_id;

-- 2) Payments aggregated per order
DROP TABLE IF EXISTS agg_payments;
CREATE TABLE agg_payments AS
SELECT
    order_id,
    SUM(payment_value) AS total_payment_value,
    MAX(payment_installments) AS max_installments,
    COUNT(*) AS n_payment_records,
    MAX(CASE WHEN payment_sequential = 1 THEN payment_type END) AS primary_payment_type
FROM olist_order_payments_dataset
GROUP BY order_id;

-- 3) Reviews aggregated per order
DROP TABLE IF EXISTS agg_reviews;
CREATE TABLE agg_reviews AS
SELECT
    order_id,
    AVG(review_score) AS avg_review_score
FROM olist_order_reviews_dataset
GROUP BY order_id;

-- 4) Order-level fact table
DROP TABLE IF EXISTS fact_orders;
CREATE TABLE fact_orders AS
SELECT
    foi.order_id,
    foi.customer_id,
    foi.customer_unique_id,
    foi.order_status,
    foi.order_purchase_ts,
    foi.order_purchase_date,
    foi.order_purchase_ym,
    foi.customer_city,
    foi.customer_state,

    COUNT(DISTINCT foi.order_item_id)    AS n_items,
    COUNT(DISTINCT foi.product_id)       AS n_products,
    SUM(foi.price)                       AS gross_items_value,
    SUM(foi.freight_value)               AS total_freight_value,

    ap.total_payment_value,
    ap.max_installments,
    ap.n_payment_records,
    ap.primary_payment_type,

    ar.avg_review_score
FROM fact_order_items foi
LEFT JOIN agg_payments ap
    ON foi.order_id = ap.order_id
LEFT JOIN agg_reviews ar
    ON foi.order_id = ar.order_id
GROUP BY foi.order_id;

-- 5) Customer-level aggregates
DROP TABLE IF EXISTS dim_customers_agg;
CREATE TABLE dim_customers_agg AS
SELECT
    fo.customer_unique_id,
    MIN(fo.order_purchase_date)                      AS first_order_date,
    MAX(fo.order_purchase_date)                      AS last_order_date,
    COUNT(DISTINCT fo.order_id)                      AS n_orders,
    SUM(fo.total_payment_value)                      AS total_revenue,
    SUM(fo.gross_items_value)                        AS total_gross_items_value,
    AVG(fo.total_payment_value)                      AS avg_order_value,
    COUNT(DISTINCT fo.order_purchase_ym)             AS active_months,
    MAX(fo.customer_city)                            AS customer_city,
    MAX(fo.customer_state)                           AS customer_state
FROM fact_orders fo
GROUP BY fo.customer_unique_id;
