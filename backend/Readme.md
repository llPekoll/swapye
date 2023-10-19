### Backend


### Coding coventions
http://www.sefidian.com/2021/08/03/how-to-use-black-flake8-and-isort-to-format-python-codes/


### migrations
# Dump db  
>> python manage.py dumpdata --exclude auth.permission --exclude contenttypes > dump.json  

# restaure db  
>> python manage.py loaddata dump.json  


./manage.py migrate trads --database=trad


### Digital Ocean 
# Clean Registry
doctl registry garbage-collection start --include-untagged-manifests

# Run test
`python manage.py test`


# install PDF
https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#installation


migration in not good order
https://stackoverflow.com/questions/44651760/django-db-migrations-exceptions-inconsistentmigrationhistory



# django migtaion 500 on save in admin
https://stackoverflow.com/questions/70274885/insert-or-update-on-table-django-admin-log-violates-foreign-key-constraint


# test jango circle CI
https://jangiacomelli.com/django-tests-on-circleci-step-by-step/