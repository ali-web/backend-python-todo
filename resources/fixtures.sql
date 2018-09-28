INSERT INTO users (username, password) VALUES
('user1', 'pbkdf2:sha256:50000$O7MOC4BV$23d31893a9b67b96304107afd0da5ae5467813a9e81e213dd6420992c08a5abd'),
-- salted value of user1
('user2', 'pbkdf2:sha256:50000$1JKa2VIR$07dc34a908b6b3a9367020030020bfcf7680d2c031af9956385917c70f9391b8'),
-- salted value of user2
('user3', 'pbkdf2:sha256:50000$ORP3BaV7$8200d8021996fd7eb7b942a9edbedc0f6646e8f177415446c3f022b31dc3fd62');
-- salted value of user3

INSERT INTO todos (user_id, description) VALUES
(1, 'Vivamus tempus'),
(1, 'lorem ac odio'),
(1, 'Ut congue odio'),
(1, 'Sodales finibus'),
(1, 'Accumsan nunc vitae'),
(2, 'Lorem ipsum'),
(2, 'In lacinia est'),
(2, 'Odio varius gravida');