Things covered in terms of security:
* password hashing/salting
* basic authentication
* prevent unauthorozied access to resources
* giving users minimal knowledge about resources that are not of their concnern (404 instead of 403)
* sql injection prevention (handled by SQLAlchemy)


Some typical secuirty work that could be done:
* tying session to non-frequently-changing client info such as user agent string
* csrf attack protection
* xss attack prevention
* locking user login on a certain number failed login attempts with a certain ip
* Captcha requirement for registration and login after failed login attempts
* etc.