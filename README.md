#### Project Description
ReviewerX stands as a sophisticated web application meticulously designed to present comprehensive insights into various businesses. It serves as an immersive platform where users can not only access essential business information but also delve into a plethora of reviews and comments contributed by the dynamic user community.

Enabling a seamless interaction experience, users are empowered to share their perspectives by crafting detailed reviews for the businesses they engage with. The richness of these reviews is enhanced by the option to seamlessly integrate photos, providing a visual dimension to the narrative.

Moreover, the engagement doesn't end with reviews alone—users have the ability to augment the conversation by leaving insightful comments on existing reviews. This interactive layer fosters a vibrant community where discussions flourish and opinions are exchanged.

Adding a touch of visual appeal, both reviews and businesses can be adorned with captivating photos, offering a vivid portrayal of experiences. This visual element serves to enrich the user experience and adds a layer of authenticity to the shared content.

Social validation takes center stage as users can express their approval by "liking" both reviews and comments. This feature not only adds a social dimension to the platform but also provides a quick and effective way for users to express their agreement or appreciation.

To enhance user convenience and facilitate seamless exploration, ReviewerX integrates a robust search functionality. This empowers users to effortlessly locate businesses of interest, ensuring that the platform serves as a comprehensive and user-friendly hub for all things related to business reviews and information.

#### Distinctiveness and Complexity
Why you believe your project satisfies the distinctiveness and complexity requirements, mentioned above.
This project satisfies complexity requirements by implementing:
* 9 Django models (these models define the structure and relationships within the Django application, capturing the essence of users, businesses, reviews, comments, likes, and associated photos in a comprehensive manner.)

* 20 Django function views (functions for rendering the index page, displaying business details, handling user authentication, managing business-related forms, updating business information, and interacting with reviews and comments. The views include operations such as adding, updating, and deleting businesses, reviews, and comments. Additionally, there are functionalities for setting primary photos, liking reviews and comments, and handling user registration and login/logout processes. )

* 6 Django forms (these forms collectively contribute to the seamless and intuitive user experience on the ReviewerX platform, encapsulating key aspects of business information, multimedia content, and user-generated reviews and comments.)

* Javascript
* Bootstrap 
* Mobile responsiveness 

#### What’s contained in each file you created.
##### reviewerx/models.py
Contains models representing entities and their relationships to each other, as well as helper functions required to generate random filenames for the uploaded files.

User Model (User):

This model represents users on the platform and extends the default Django user model (AbstractUser).
It includes fields for first name, last name, and a profile photo.
The photo is stored in a designated location on the server, and there's a default image in case a user hasn't uploaded one.
Business Model (Business):

Represents businesses on the platform.
Stores information such as name, description, type, website, location details (street, city, state, country, zip code), contact details (phone, email), schedule, and creation/update timestamps.
Utilizes a foreign key to associate each business with a user who owns it.
Allows the addition of photos and reviews associated with the business.
Defines a method to calculate and retrieve the average rating of the business based on its reviews.
Review Model (Review):

Represents reviews posted by users for businesses.
Includes a title, text, rating, creation/update timestamps, and a flag indicating if the review has been deleted.
Utilizes a foreign key to associate each review with a user who posted it.
Allows the addition of photos and comments associated with the review.
Defines a method to calculate and retrieve the average rating of the business based on its reviews.
Comment Model (Comment):

Represents comments posted by users on reviews.
Includes text, creation/update timestamps, and a flag indicating if the comment has been deleted.
Utilizes a foreign key to associate each comment with a user who posted it.
Allows the addition of likes associated with the comment.
Like Models (ReviewLike, CommentLike):

Represents likes given by users to reviews and comments, respectively.
Includes a foreign key to associate each like with a user and a timestamp.
Photo Models (BusinessPhoto, ReviewPhoto, CommentPhoto):

Store photos associated with businesses, reviews, and comments, respectively.
Include a timestamp, and for business photos, a flag indicating if the photo is the primary one.
BusinessType Model (BusinessType):

Represents the types or categories that businesses can belong to.
Stores the name of each business type.

##### reviewerx/urls.py
The URL patterns include routes for the index page, user authentication (login, logout, and registration), business-related actions (such as viewing details, adding reviews, comments, and businesses), and managing updates or deletions of businesses, reviews, and comments. Additionally, there are routes for handling actions like setting primary photos, liking reviews and comments, and searching for businesses. These URL configurations establish a clear structure for user navigation and interaction within the ReviewerX platform, ensuring a logical flow of paths to access and manage different features offered by the application.


##### reviewerx/views.py
Contains views that query data, validate data, and forward data to the templates for rendering. 
It encompasses functions for rendering the index page, displaying business details, handling user authentication, managing business-related forms, updating business information, and interacting with reviews and comments. The views include operations such as adding, updating, and deleting businesses, reviews, and comments. Additionally, there are functionalities for setting primary photos, liking reviews and comments, and handling user registration and login/logout processes.

##### reviewerx/forms.py
The BusinessForm facilitates the addition and modification of business information, offering a range of fields such as name, type, description, contact details, and location. It incorporates widgets and labels for a user-friendly interface. The BusinessPhotoForm allows users to upload and manage photos associated with businesses, with an option to designate a primary photo. The CommentForm provides a structured input for users to submit comments, and the ReviewForm is designed for creating and updating reviews, including fields for title, text, and a rating system. Lastly, the ReviewPhotoForm enables users to upload photos accompanying their reviews. 

##### reviewerx/static/reviewerx/reviewerx.js
This JavaScript file defines event listeners and functions that handle user interactions on the ReviewerX web application. The document.addEventListener listens for clicks and checks if the clicked element has specific class names, such as 'review-like' or 'comment-like'. Depending on the class, it triggers corresponding functions (reviewLikeAction or commentLikeAction) that perform asynchronous fetch requests to the server, updating the like counts for reviews and comments. These functions utilize the CSRF token to authenticate the requests, and upon receiving the server response, they update the like counts in the HTML. Additionally, there's a getCookie function to retrieve the CSRF token from cookies. The file also includes functionality to dynamically draw star ratings based on the data provided in the HTML elements with the class 'star-rating', creating a visual representation of user ratings on the platform.

##### reviewerx/templates/reviewerx/*.html
The add_business_form.html template is used to render a form for adding a new business, add_comment.html for adding comments, and add_review_form.html for adding reviews. The business_detail.html template displays detailed information about a specific business. Templates like index.html and search_business.html are used for rendering the main index page and search results. layout.html is a base template providing the overall structure for other templates. login.html and register.html handle user authentication and registration, while top_nav_bar.html renders the top navigation bar. Additionally, templates like pagination.html and businesses_pagination.html handle the presentation of paginated content, and update_business_form.html, update_comment.html, and update_review.html handle the update forms for businesses, comments, and reviews, respectively.

#### How to run your application.
1. Pull the project from the git repository
2. Create virtual environment (pip -m venv venv)
3. Activate virtual environment (source venv/bin/activate)
4. Install dependencies (pip install -r requirements.txt)
5. Run application (python3 manage.py runserver)
6. Access in the browser (127.0.0.1:8000)


#### Additional information
Admin superuser is created in advance with credentials: admin/1001. admin can has access admin panel at the 127.0.0.1/admin 

Several other users had been created to test the application:
* bob/1001
* ksenia/1001


#### Video
https://youtu.be/ApFXwHX-VfM