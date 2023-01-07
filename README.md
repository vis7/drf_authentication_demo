# drf_authentication_demo
Django Rest Framework Application implementing Authentication

# Features
Added api for below features.
- login, register, and reset password features. (System has 2 roles: Admin, Customer).
- Customer should be able to update his profile

# Validations
- email unique
- phone number validation
- profile photo size less then 2 MB
- date_of_birth can not be a future date

# to do
- [ ] Add fixtures
- [ ] Add other userfull tools - (swagger, django_extentions, isort, linter etc.)
- [X] Add unit tests for main functionalities

# tests
- Register and login
- Change profile - bd in future not allowed, 
- Change profile - pic more then 2 MB not allowed
