# Issue manager

## Create an issue management system (MVP)

### Criteria
1. This directory (`issue_mgr`) should house our django project.
2. You should have pages for:
2.1. Home page
2.2. About us page
3. Create an app for accounts
3.1. Create the user model with the instructions below in accounts/models.py
3.2. The user model must extend the AbstractUser class (see below).
4. Have at a minimum, pages (accessible through the front end) for:
4.1. A list of issues
4.2. A detail view for issues
4.3. A creation form for issues
5. Generate an issue model with the following attributes:
5.1. Summary
5.2. Description
5.3. Status (foreign key)
5.4. Priority
5.5. Assignee (foreign key to the user)
5.6. Reporter (foreign key to the user)
5.7. Created on (time stamp, should auto-populate when new issues are created)

## Note
Do not run the migrations!

### Models:
```
from django.contrib.auth import AbstractUser

class CustomUser(AbstractUser)
    # You should create any additional (necessary) models to make this work:
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
```

```
class Issue(models.Model):
    # apart from the fields above, we need to make sure we have
    # foreign key constraints to the additional required models
    # you should create those models as needed
```
