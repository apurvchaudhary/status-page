# State Manager

### We can run this project in single docker-compose statement
#### All pre-reqs will be adjusted automatically (build, run, migrate, collect, default data)
```
docker-compose up -d --build
```

### Default login credentials for superuser

#### Username
```
admin
```
#### Password
```
admin1234
```

### Default groups are Organization-Admin, Organization-Member
#### SIGN UP page will create user with role=member, group=Organization-Member, is_active=False, change permission accordingly.
##### 1. Authorizing member : set is_active=True
##### 2. Authorizing organization admin : set is_active=True, role=Organization Admin, groups=Organization-Admin

#### Deployed on below ec2 (heroku isn't free anymore)
http://52.66.194.246/
#### Note : Do let me know after verification and testing, I will delete this ec2 instance

#### Loom video link
https://www.loom.com/share/a3affff394c24cc89da749752df36eb1?sid=11551659-6495-44f9-8e29-f16550b9a548
