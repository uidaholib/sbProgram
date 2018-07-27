

To Do:
[ ] Finish Flask Mega Tutorial
[ ] Create unit tests for all models in `models.py`
[ ] Create unit tests for making sure a casc, fy, project, item, etc is all added correctly to the database (add, then check that what was added can be retrieved)
[ ] Integrate Old and New code
[ ] Clean up Javascript and all front end code


When done with migrating code:
* Check basic functionality (using new unit tests where applicable)
    - `app/email.py` (unit test)
    - XFlask Shell and DB-diving
    - XCheck models form and function (unit test)
* Check subsystems
    * Auth
        - XCheck template rendering of emails and pages (particularly emails)
        - XCheck email sending
        - XCheck that changes are made in db for creating user, changing password, email, etc.
    * Errors
        - Check all handled errors
    * Main
        - Check all routes
        - Check editting profile is working
* Check that last chapter's things were done (unit testing improvements, environmental variables, etc.)
