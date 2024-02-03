CREATE TABLE owners (
    id SERIAL PRIMARY KEY,
    name VARCHAR(30)
);

CREATE TABLE accounts (
    id SERIAL PRIMARY KEY,
    name VARCHAR(30),
    owner_id INTEGER REFERENCES owners
);

CREATE TABLE buy_events (
    id SERIAL PRIMARY KEY,
    account_id INTEGER REFERENCES accounts,
    date DATE,
    stock VARCHAR(30),
    number INTEGER,
    price DECIMAL,
    sold INTEGER
);

CREATE TABLE sell_events (
    id SERIAL PRIMARY KEY,
    account_id INTEGER REFERENCES accounts,
    date DATE,
    stock VARCHAR(30),
    number INTEGER,
    price DECIMAL
);

CREATE TABLE stocks (
    name VARCHAR(30),
    dividend DECIMAL
);

CREATE TABLE pairing (
    buy_id INTEGER REFERENCES events,
    sell_id INTEGER REFERENCES events,
    number INTEGER
);