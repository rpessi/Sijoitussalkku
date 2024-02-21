CREATE TABLE users (
    id SERIAL,
    username VARCHAR(20),
    password TEXT,
    PRIMARY KEY (id)
);

CREATE TABLE owners (
    id SERIAL,
    name VARCHAR(30),
    user_id INTEGER,
    PRIMARY KEY (id), 
    FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE accounts (
    id SERIAL,
    name VARCHAR(30),
    owner_id INTEGER,
    PRIMARY KEY (id),
    FOREIGN KEY (owner_id) REFERENCES owners (id)
);

CREATE TABLE stocks (
    name VARCHAR(30),
    dividend DECIMAL,
    user_id INTEGER,
    PRIMARY KEY (name),
    FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE buy_events (
    id SERIAL,
    account_id INTEGER,
    date DATE,
    stock VARCHAR(30),
    number INTEGER,
    price DECIMAL,
    sold INTEGER,
    PRIMARY KEY (id), 
    FOREIGN KEY (account_id) REFERENCES accounts (id)
);

CREATE TABLE sell_events (
    id SERIAL,
    account_id INTEGER,
    date DATE,
    stock VARCHAR(30),
    number INTEGER,
    price DECIMAL,
    PRIMARY KEY (id), 
    FOREIGN KEY (account_id) REFERENCES accounts (id)
);

CREATE TABLE pairing (
    id SERIAL,
    buy_id INTEGER,
    sell_id INTEGER,
    number INTEGER,
    PRIMARY KEY (id),
    FOREIGN KEY (buy_id) REFERENCES buy_events (id),
    FOREIGN KEY (sell_id) REFERENCES sell_events (id)
);