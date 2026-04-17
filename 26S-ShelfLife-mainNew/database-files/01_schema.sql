SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS ADMIN_FLAG;
DROP TABLE IF EXISTS BUNDLE_LISTING;
DROP TABLE IF EXISTS WISHLIST;
DROP TABLE IF EXISTS REVIEW;
DROP TABLE IF EXISTS FLAG;
DROP TABLE IF EXISTS TRANSACTION;
DROP TABLE IF EXISTS LISTING;
DROP TABLE IF EXISTS PRICE_HISTORY;
DROP TABLE IF EXISTS COURSE_MATERIAL;
DROP TABLE IF EXISTS BUNDLE;
DROP TABLE IF EXISTS ITEM;
DROP TABLE IF EXISTS COURSE;
DROP TABLE IF EXISTS DEPARTMENT;
DROP TABLE IF EXISTS USER;
DROP TABLE IF EXISTS ADMIN;
DROP TABLE IF EXISTS ANALYST;
DROP TABLE IF EXISTS REPORT;
DROP TABLE IF EXISTS PLATFORM_METRIC;
SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE USER (
    user_id    INT          NOT NULL AUTO_INCREMENT,
    name       VARCHAR(100) NOT NULL,
    email      VARCHAR(200) NOT NULL UNIQUE,
    is_active  TINYINT(1)   NOT NULL DEFAULT 1,
    avg_rating DECIMAL(3,2) NULL,
    created_at DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id)
);

CREATE TABLE ADMIN (
    admin_id INT          NOT NULL AUTO_INCREMENT,
    name     VARCHAR(100) NOT NULL,
    email    VARCHAR(200) NOT NULL UNIQUE,
    PRIMARY KEY (admin_id)
);

CREATE TABLE ANALYST (
    analyst_id INT          NOT NULL AUTO_INCREMENT,
    name       VARCHAR(100) NOT NULL,
    email      VARCHAR(200) NOT NULL UNIQUE,
    PRIMARY KEY (analyst_id)
);

CREATE TABLE DEPARTMENT (
    dept_id   INT          NOT NULL AUTO_INCREMENT,
    dept_name VARCHAR(100) NOT NULL,
    college   VARCHAR(100) NOT NULL,
    PRIMARY KEY (dept_id)
);

CREATE TABLE PLATFORM_METRIC (
    metric_id          INT      NOT NULL AUTO_INCREMENT,
    active_users       INT      NOT NULL,
    total_listings     INT      NOT NULL,
    total_transactions INT      NOT NULL,
    recorded_at        DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (metric_id)
);

CREATE TABLE COURSE (
    course_id     INT          NOT NULL AUTO_INCREMENT,
    dept_id       INT          NOT NULL,
    course_number VARCHAR(20)  NOT NULL,
    course_name   VARCHAR(200) NOT NULL,
    semester      VARCHAR(20)  NOT NULL,
    is_active     TINYINT(1)   NOT NULL DEFAULT 1,
    PRIMARY KEY (course_id),
    FOREIGN KEY (dept_id) REFERENCES DEPARTMENT(dept_id)
);

CREATE TABLE ITEM (
    item_id   INT          NOT NULL AUTO_INCREMENT,
    title     VARCHAR(200) NOT NULL,
    author    VARCHAR(200) NULL,
    isbn      VARCHAR(20)  NULL UNIQUE,
    category  VARCHAR(50)  NOT NULL,
    PRIMARY KEY (item_id)
);

CREATE TABLE REPORT (
    report_id     INT         NOT NULL AUTO_INCREMENT,
    analyst_id    INT         NOT NULL,
    filter_params TEXT        NULL,
    export_format VARCHAR(10) NOT NULL DEFAULT 'CSV',
    created_at    DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (report_id),
    FOREIGN KEY (analyst_id) REFERENCES ANALYST(analyst_id)
);

CREATE TABLE COURSE_MATERIAL (
    course_material_id INT          NOT NULL AUTO_INCREMENT,
    course_id          INT          NOT NULL,
    item_id            INT          NOT NULL,
    required           TINYINT(1)   NOT NULL DEFAULT 1,
    PRIMARY KEY (course_material_id),
    UNIQUE KEY uq_course_item (course_id, item_id),
    FOREIGN KEY (course_id) REFERENCES COURSE(course_id),
    FOREIGN KEY (item_id)   REFERENCES ITEM(item_id)
);

CREATE TABLE PRICE_HISTORY (
    history_id  INT            NOT NULL AUTO_INCREMENT,
    item_id     INT            NOT NULL,
    semester    VARCHAR(20)    NOT NULL,
    avg_price   DECIMAL(10,2)  NOT NULL,
    low_price   DECIMAL(10,2)  NOT NULL,
    high_price  DECIMAL(10,2)  NOT NULL,
    total_sales INT            NOT NULL DEFAULT 0,
    PRIMARY KEY (history_id),
    FOREIGN KEY (item_id) REFERENCES ITEM(item_id)
);

CREATE TABLE BUNDLE (
    bundle_id   INT            NOT NULL AUTO_INCREMENT,
    user_id     INT            NOT NULL,
    total_price DECIMAL(10,2)  NOT NULL,
    created_at  DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (bundle_id),
    FOREIGN KEY (user_id) REFERENCES USER(user_id)
);

CREATE TABLE LISTING (
    listing_id     INT            NOT NULL AUTO_INCREMENT,
    user_id        INT            NOT NULL,
    item_id        INT            NOT NULL,
    course_id      INT            NOT NULL,
    price          DECIMAL(10,2)  NOT NULL,
    condition_desc VARCHAR(50)    NOT NULL,
    status         VARCHAR(20)    NOT NULL DEFAULT 'Active',
    created_at     DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    search_count   INT            NOT NULL DEFAULT 0,
    PRIMARY KEY (listing_id),
    FOREIGN KEY (user_id)   REFERENCES USER(user_id),
    FOREIGN KEY (item_id)   REFERENCES ITEM(item_id),
    FOREIGN KEY (course_id) REFERENCES COURSE(course_id)
);

CREATE TABLE TRANSACTION (
    transaction_id INT            NOT NULL AUTO_INCREMENT,
    listing_id     INT            NOT NULL UNIQUE,
    buyer_id       INT            NOT NULL,
    sale_price     DECIMAL(10,2)  NOT NULL,
    sold_at        DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    days_to_sale   INT            NULL,
    PRIMARY KEY (transaction_id),
    FOREIGN KEY (listing_id) REFERENCES LISTING(listing_id),
    FOREIGN KEY (buyer_id)   REFERENCES USER(user_id)
);

CREATE TABLE REVIEW (
    review_id   INT      NOT NULL AUTO_INCREMENT,
    listing_id  INT      NOT NULL,
    reviewer_id INT      NOT NULL,
    seller_id   INT      NOT NULL,
    rating      INT      NOT NULL,
    comment     TEXT     NULL,
    created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (review_id),
    CONSTRAINT chk_rating CHECK (rating BETWEEN 1 AND 5),
    FOREIGN KEY (listing_id)  REFERENCES LISTING(listing_id),
    FOREIGN KEY (reviewer_id) REFERENCES USER(user_id),
    FOREIGN KEY (seller_id)   REFERENCES USER(user_id)
);

CREATE TABLE WISHLIST (
    wishlist_id INT      NOT NULL AUTO_INCREMENT,
    user_id     INT      NOT NULL,
    listing_id  INT      NOT NULL,
    saved_at    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (wishlist_id),
    UNIQUE KEY uq_user_listing (user_id, listing_id),
    FOREIGN KEY (user_id)    REFERENCES USER(user_id),
    FOREIGN KEY (listing_id) REFERENCES LISTING(listing_id)
);

CREATE TABLE FLAG (
    flag_id     INT         NOT NULL AUTO_INCREMENT,
    listing_id  INT         NOT NULL,
    reason      TEXT        NOT NULL,
    flag_status VARCHAR(20) NOT NULL DEFAULT 'Pending',
    flagged_at  DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (flag_id),
    FOREIGN KEY (listing_id) REFERENCES LISTING(listing_id)
);

CREATE TABLE BUNDLE_LISTING (
    bundle_id  INT NOT NULL,
    listing_id INT NOT NULL,
    PRIMARY KEY (bundle_id, listing_id),
    FOREIGN KEY (bundle_id)  REFERENCES BUNDLE(bundle_id),
    FOREIGN KEY (listing_id) REFERENCES LISTING(listing_id)
);

CREATE TABLE ADMIN_FLAG (
    admin_id INT NOT NULL,
    flag_id  INT NOT NULL,
    PRIMARY KEY (admin_id, flag_id),
    FOREIGN KEY (admin_id) REFERENCES ADMIN(admin_id),
    FOREIGN KEY (flag_id)  REFERENCES FLAG(flag_id)
);
