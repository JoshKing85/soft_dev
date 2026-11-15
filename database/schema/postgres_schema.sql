

-- USER

CREATE TABLE IF NOT EXISTS users(
    user_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone_number VARCHAR(15) NOT NULL,
    address VARCHAR(100) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender VARCHAR(30) NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- MEMBERSHIPS

--  Membership entities
CREATE TABLE IF NOT EXISTS membership_plans(

    memp_id INT PRIMARY KEY,
    memp_name VARCHAR(100) NOT NULL,
    memp_cost NUMERIC(8, 2) NOT NULL
);

-- Populate membership plans
INSERT INTO membership_plans (memp_id, memp_name, memp_cost)
VALUES (1, 'Standard', 15.99);

INSERT INTO membership_plans (memp_id, memp_name, memp_cost)
VALUES (2, 'Plus', 29.99);

INSERT INTO membership_plans (memp_id, memp_name, memp_cost)
VALUES (3, 'Premium', 39.99);

-- Memberships table
CREATE TABLE IF NOT EXISTS memberships(
    user_id BIGINT NOT NULL REFERENCES users(user_id),
    memp_id INT NOT NULL REFERENCES membership_plans(memp_id),
    start_date DATE NOT NULL,
    end_date DATE,

    PRIMARY KEY(user_id, memp_id)
);



