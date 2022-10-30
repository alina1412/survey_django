<body>
        
# Survey app (django)
        

## Description
It's a django web-application. The site allows user to create surveys and answer surverys of other users.

The site is deployed here: https://survey-django-app.herokuapp.com/survey/home/

## Structure
The app can use `sqlite` or `postgres` database, it keeps data in tables: Survey, Question, Choice, Answer with models for each of them.
For keeping Users it takes a model from django.contrib.auth.models.

### Models
<img src="https://user-images.githubusercontent.com/8655093/198866948-5690511c-6c0f-45b6-9c37-95e0424db625.jpg" height="250"> </img>

### Tables
picture of some tables (except of a default django tables, auth_user - is a default one)
<img src="https://user-images.githubusercontent.com/8655093/198867044-4c7ba45b-c66e-4f7e-8599-2a96ad472dbd.jpg" height="310"> </img>



<details close="">
<summary>  
        
### Structure tree
```
survey_django/
|
|
```
        

</summary> 
        
```
        
|   .env
|   .env-example
|   .gitignore
|   .pylintrc
|   docker-compose.yml
|   Makefile
|   manage.py
|   poetry.lock
|   Procfile
|   pyproject.toml
|   pytest.ini
|   README.md
|   requirements.txt
|   runtime.txt
|   
|       
+---static
|   |   __init__.py
|   |   
|   +---css
|   |       styles.css
|   |       
|   +---images
|   |       favicon.ico
|   |       results-example.jpg
|   |       survey-detail-example.jpg
|   |       your-list-example.jpg
|   |       
|   \---templates
|           add_template.html
|           answer.html
|           base.html
|           home.html
|           login.html
|           messages.html
|           queston_detail.html
|           register.html
|           results.html
|           surveys_list.html
|           surveys_to_pass_list.html
|           survey_detail.html
|           
+---survey_app
|   |   admin.py
|   |   apps.py
|   |   crud.py
|   |   download.py
|   |   forms.py
|   |   models.py
|   |   urls.py
|   |   __init__.py
|   |   
|   +---migrations
|   |       0001_initial.py
|   |       __init__.py
|   |       
|   +---tests
|   |       conftest.py
|   |       tests.py
|   |       test_urls.py
|   |       utils.py
|   |       
|   \---views
|           utils.py
|           views.py
|           views_choices_answers.py
|           views_questions.py
|           views_survey.py
|           view_mixin.py
|           
\---survey_project
        asgi.py
        settings.py
        tests.py
        urls.py
        wsgi.py
        __init__.py
        
 ```
        
</details>


## Example of pages
        
 <div>
   
 <img src="https://user-images.githubusercontent.com/8655093/179979528-a8929f24-56fc-4b48-a759-0b3d461d38e8.jpg" height="300"> </img>
 <img src="https://user-images.githubusercontent.com/8655093/179979519-b02dda72-7606-4d3b-8b6a-23a845f80f14.jpg" height="300"> </img>
  
 <img src="https://user-images.githubusercontent.com/8655093/179979529-27a16627-6185-4434-a0ce-6ef5b08722b2.jpg" height="250"> </img>
   
</div>
  

</body>
