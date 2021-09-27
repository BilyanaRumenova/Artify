# Artify
 Individual Project Assignment for the Python Web Framework Course @ SoftUni
 
Webb app for users to showcase their artistic skills of photography, paintings, portraits, fashion, etc. 
The users can like posts and follow different artists to explore their latest posts from their feed; could also view posts divided into categories and put into different album according to the category.

The application is implemented using Django Framework; functionality is written in Python, other features are: Bootstrap in JavaScript, HTML, CSS.

Artify app has login/register functionality; public(a part of the website, which is accessible by everyone - un/authenticated users and admins) and private part(accessible only by authenticated users and admins), as well as admin part(accessible only to admins). Unauthenticated users have only 'GET' permissions and authenticated users have full CRUD for all their created content; admins have full CRUD functionalities.
Other functionalities used are: form validations, error handling and data validations;
Tests are written for 65% covarage on the business logic;
Django Templates are implemented using Template Inheritance so that they could be reused multiple times;
Responsive Web Design is implemented so that the application could be used on various devices;
Class-based views are implemented, as well as extended Django user, so that users can sign-up and sign-in using email and password, not using username;
A file storage cloud is used - Cloudinary, for storing the uploaded files 

