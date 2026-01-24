-- =========================
-- USERS TABLE
-- =========================
CREATE TABLE users (
    uid BIGSERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    dec TEXT,
    email VARCHAR(100) UNIQUE NOT NULL,
    img VARCHAR(255) DEFAULT '/images/default.png',

    -- 성별: M / F
    gender CHAR(1) CHECK (gender IN ('M', 'F')),

    -- 생년월일 (나이는 계산값)
    birth_date DATE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================
-- MOVIE TABLE
-- =========================
CREATE TABLE movie (
    mid BIGSERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    dec TEXT,
    rat NUMERIC(2,1) DEFAULT 0,
    release_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================
-- GENRE TABLE
-- =========================
CREATE TABLE genre (
    gid BIGSERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- =========================
-- MOVIE_GENRE (N:M)
-- =========================
CREATE TABLE movie_genre (
    mid BIGINT NOT NULL,
    gid BIGINT NOT NULL,
    PRIMARY KEY (mid, gid),
    FOREIGN KEY (mid) REFERENCES movie(mid) ON DELETE CASCADE,
    FOREIGN KEY (gid) REFERENCES genre(gid) ON DELETE CASCADE
);

-- =========================
-- REVIEW TABLE
-- =========================
CREATE TABLE review (
    rid BIGSERIAL PRIMARY KEY,
    uid BIGINT NOT NULL,
    mid BIGINT NOT NULL,
    title VARCHAR(200),
    dec TEXT NOT NULL,

    -- 별점: 1 ~ 5
    rat NUMERIC(2,1) CHECK (rat BETWEEN 1 AND 5),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- 유저는 영화당 리뷰 1개
    UNIQUE (uid, mid),

    FOREIGN KEY (uid) REFERENCES users(uid) ON DELETE CASCADE,
    FOREIGN KEY (mid) REFERENCES movie(mid) ON DELETE CASCADE
);

-- =========================
-- COMMENT TABLE
-- =========================
CREATE TABLE comment (
    cid BIGSERIAL PRIMARY KEY,
    rid BIGINT NOT NULL,
    uid BIGINT NOT NULL,
    dec TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (rid) REFERENCES review(rid) ON DELETE CASCADE,
    FOREIGN KEY (uid) REFERENCES users(uid) ON DELETE CASCADE
);

-- =========================
-- REVIEW LIKE / DISLIKE
-- =========================
CREATE TABLE review_like (
    lid BIGSERIAL PRIMARY KEY,
    rid BIGINT NOT NULL,
    uid BIGINT NOT NULL,

    -- L = Like, D = Dislike
    type CHAR(1) CHECK (type IN ('L', 'D')),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- 한 유저는 리뷰에 한 번만 반응
    UNIQUE (rid, uid),

    FOREIGN KEY (rid) REFERENCES review(rid) ON DELETE CASCADE,
    FOREIGN KEY (uid) REFERENCES users(uid) ON DELETE CASCADE
);

-- =========================
-- COMMENT LIKE / DISLIKE
-- =========================
CREATE TABLE comment_like (
    lid BIGSERIAL PRIMARY KEY,
    cid BIGINT NOT NULL,
    uid BIGINT NOT NULL,

    -- L = Like, D = Dislike
    type CHAR(1) CHECK (type IN ('L', 'D')),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- 한 유저는 댓글에 한 번만 반응
    UNIQUE (cid, uid),

    FOREIGN KEY (cid) REFERENCES comment(cid) ON DELETE CASCADE,
    FOREIGN KEY (uid) REFERENCES users(uid) ON DELETE CASCADE
);
