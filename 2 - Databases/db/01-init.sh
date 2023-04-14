set -e
export PGPASSWORD=$POSTGRES_PASSWORD;
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
  CREATE TABLE ft_transaction (
    receipt_id INT NOT NULL,
    member_id VARCHAR(50) NOT NULL,
    order_datetime TIMESTAMP NOT NULL,
    total_price DECIMAL NOT NULL,
    total_weight DECIMAL NOT NULL
)
;

CREATE TABLE ft_itemlevel (
    itemlevel_autoid INT NOT NULL,
    receipt_id INT NOT NULL,
    sku_id VARCHAR(50) NOT NULL,
    quantity INT NOT NULL
)
;

CREATE TABLE lu_iteminfo (
    sku_id varchar(50) NOT NULL,
    item_name VARCHAR(100),
    unit_price DECIMAL NOT NULL,
    unit_weight DECIMAL NOT NULL,
    manufacturer_name VARCHAR(100) NOT NULL
)
;

CREATE TABLE lu_member (
    member_id varchar(50) NOT NULL,
    first_name varchar(50) NOT NULL,
    last_name varchar(50) NOT NULL,
    date_of_birth DATE NOT NULL,
    mobile_no varchar(8) NOT NULL,
    email varchar(5) NOT NULL
)
;
EOSQL