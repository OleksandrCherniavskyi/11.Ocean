live preview [https://92md4d-8080.csb.app/](https://5tq79j-8080.csb.app/)

Service where any user can upload an image in PNG or JPG format. 
-  three builtin account tiers: Basic, Premium and Enterprise
-  each tires have self arbitrary thumbnail sizes
-  admin UI

Login: pass
- admin: admin  ```superuser```
- basic_user: basic123  ```basic```
- premium_user: premium123 ```premium```
- enterprise_user: enterprise1234 ```enterprise```


Quiq build with docker
- clone repository 
- docker build -t image_name .
- docker run -p 8080:8080 image_name
