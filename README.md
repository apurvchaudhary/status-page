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
