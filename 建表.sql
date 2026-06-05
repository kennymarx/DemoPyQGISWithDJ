select * from users_authorizeduser;

CREATE TABLE "users_authorizeduser" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "openid" varchar(100) NOT NULL UNIQUE, "nickname" varchar(100) NULL, "avatar" varchar(200) NULL, "is_active" bool NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL)

INSERT INTO users_authorizeduser ("id", "openid", "nickname", "avatar", "is_active", "created_at", "updated_at")
VALUES (1, 'oCL9n3cM1_Se8jTlrJhplTHuNqho', 'k', 'k@xxx.com', 1, datetime('now'),datetime('now'));