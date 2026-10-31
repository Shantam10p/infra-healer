CREATE TABLE menu (
    id     SERIAL PRIMARY KEY,
    name   TEXT UNIQUE NOT NULL,
    price  NUMERIC(5,2) NOT NULL
);

CREATE TABLE orders (
    id          SERIAL PRIMARY KEY,
    first_name  TEXT NOT NULL,
    last_name   TEXT,
    status      TEXT NOT NULL DEFAULT 'pending'
                CHECK (status IN ('pending', 'processing', 'ready', 'failed')),
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE order_items (
    id        SERIAL PRIMARY KEY,
    order_id  INT NOT NULL REFERENCES orders(id),
    drink_id  INT NOT NULL REFERENCES menu(id),
    size      TEXT NOT NULL CHECK (size IN ('small', 'medium', 'large')),
    sugar     BOOLEAN NOT NULL DEFAULT false,
    quantity  INT NOT NULL CHECK (quantity > 0),
    price     NUMERIC(5,2) NOT NULL
);

INSERT INTO menu (name, price) VALUES
    ('Latte', 4.50),
    ('Cappuccino', 4.00),
    ('Espresso', 3.00),
    ('Americano', 3.50);
