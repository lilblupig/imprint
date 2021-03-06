# **Imprint**

# Overview
This is a mobile first website designed to encourage tourists and locals alike to bask in the rich and varied history of a small town in Dorset called Shaftesbury.  An historic saxon hilltop town, Shaftesbury and it's inhabitants pride themselves on the extensive history of the town and surrounds.

Imprint takes places within the town centre, and allows users to select an area, which will generate a gallery of images related to that part of the town.  These images will hopefully have been generated and uploaded by site users, providing a true community history of this incredible town.


![Am I Responsive Image](readme-files/am-i-responsive.png)

# Index
1. [UX](#ux)
    * [User Stories](#user-stories)
    * [Strategy](#strategy)
    * [Scope](#scope)
    * [Structure](#structure)
    * [Skeleton](#skeleton)
    * [Surface](#surface)
1. [Features](#features)
    * [Existing Features](#existing-features)
    * [Features for Future Implementation](#features-for-future-implementation)
1. [Testing](#testing)
1. [Development Life Cycle](#development-life-cycle)
1. [Deployment of the Application](#deployment)
    * [Cloning via GitPod](#cloning-a-project-into-gitpod)
    * [Cloning Locally](#how-to-run-the-code-locally)
1. [Technologies Used](#technologies-used)
1. [Credits](#credits)
    * [Website](#website-credits)
    * [README](#readme-credits)

Note, testing information can be found in a separate document:
* [Testing](TESTING.md)

## UX

### **Overview and Broad Design Choices**
The website should be immediately useable from very first navigation with an unobtrusive interface, and the focus on the images from start to finish.

Fonts and colours are chosen to be striking but unfussy, and assist with intuitive navigation and use of the site.

The whole point is to become lost in nostalgia and wonder at how much has changed, yet how much has stayed the same.

### **User Stories**
There are three types of anticipated user:
1. Tourists/visitors
1. Locals
1. Local business owners

For these groups the following needs are identified:
1. As a new tourist user, I want to link what I can see to what has been uploaded - clearly and easily.
1. As a new local user, I want to find images of places I know.
1. As a new business user, I want to be able to find the area which relates to my business.
1. As a returning tourist user, I want to upload my own photographs, and easily find them to relive my memories.
1. As a returning local user, I want to share images and memories of my past and feel part of a community.
1. As a returning business user I want to be able to add value to the profile of my business and attract custom.

These stories are addressed fully in the [Testing](TESTING.md) document.

### **Strategy**
#### **Who is the website for?**
The website is for people who want to celebrate the past and link it to the present.  More specifically, it is aimed at providing an alternate view of the town in all its changing glory.

#### **What does the owner of the website need/want?**
The website owner wants to help build interest in the town, the businesses it has grown and the people it serves.

#### **What do the users of the website need/want?**
The users of the website want to utilise the history of the town to enhance their experience of it, though in a number of different ways.

#### **Broadly, how does the website meet these needs?**
The website focuses on historic imagery of the town as uploaded by the users into location specific categories.  This meets the needs of the owner by promoting curiosity about the town and its past, and of the users by providing them with evocative pictures to compliment their visit or experience, and to help build the brand of a business.

Owner aims:
* Add a new dimension to local tourism
* Bring attention to local businesses
* Attract back the interest of locals

User aims:
* Learn about surroundings
* Share experiences and memories
* Promote business

### **Scope**
The website exists to encourage tourism and active discovery of local history.  Nostalgia and enjoyment are the primary aims.

#### Feature Viability

| # | Feature | Importance | Viability | Comment |
|---| ------- | :--------: | :-------: | ------- |
1.| Location map which ties to images  | 5 | 4 | Y - Whole purpose of site
2.| Users create and manage profiles | 5 | 5 | Y - Needed for community aspect
3.| Users can add and manage images  | 5 | 5 | Y - Community contributions will add value
4.| Display content relative to signed in user  | 5 | 5 | Y - Allows user to manage contributions
5.| Designed strictly mobile first | 5 | 5 | Y - Most likely device to be used to access site by far
6.| Comments section for images | 4 | 2 | N - Unsure how this would work with non-relational database
7.| Have form/user group for businesses | 2 | 2 | N - Not required for site function, but would be nice in future
T.| Total score | 31 | 28 |

#### Feature Plan
First increment:
* Interactive map
* User profiles
* Users can upload images
* Display relevant content for user
* Mobile first design

Second increment:
* Drill down to individual image and view image info as uploaded
* Filter returned images

Third increment:
* Business accounts
* Comments
* Use Google maps to show user location on map

### **Structure**
* See Information Grouping [mind map here](readme-files/documents/structure.pdf).

### **Skeleton**
In line with structure planning.

#### **Wireframes**
1. [Mobile](readme-files/documents/imprint-mobile.pdf) 375px
1. [Tablet](readme-files/documents/imprint-tablet.pdf) 768px
1. [PC/Laptop](readme-files/documents/imprint-pc.pdf) 1200px

##### Summary of Changes
* Primary change is from separate map page as landing page, to gallery page as landing page.  Implementation of the clickable map was going to be very time consuming and tricky to make scaleable.  Additionally, realistically, locals will use it far more than visitors and they want to see the pictures, not the map.

### **Surface**

#### Colours
The colours used for the site are based on the colours which comprise the historic Shaftesbury coat of arms.  These are primarily blue and white, with yellow highlights.  A deep red was chosen as a second complimentary colour, and is the colour used by the Town Council.  In the end, the lighter blue was not used.  The subtler deep blue is classic and does not take attention from the images, and the yellow provides a good contrast for interactive elements and feedback, the red is used for warnings such as delete functions.

The colours were tested on [Coolors](https://coolors.co/) to ensure that a colourblind user would be able to differentiate between all colours, and that the colours remained visually pleasing.

![Colours option 1](readme-files/colors-opt-1.png)

#### Typography
The fonts for the site were chosen for a clean but striking aesthetic.  Appropriate letter and word spacing for dyslexic users was researched and [Google fonts](https://fonts.google.com/) scanned for eye catching examples, which were then checked against researched criteria from the British Dyslexia Association.

Cinzel was chosen for headings because of its historic feel, but relative lack of accents.

Nunito is used for the body font, providing a clean open feel.

![Example heading font](readme-files/typography-heading.png)
![Example body font](readme-files/typography-body.png)

## Features

### **Existing Features**
Features common to all pages/sections:
* Responsive collapsible navbar and footer
* Designed with mobile view in mind
* Clean interface

### **Features for Future Implementation**
1. Force https | Required for map marker and much more secure
1. Implement Cloudinary plugin to screen images for inappropriate content | At the moment a user can upload any image and relies on a moderator checking and removing anything unsuitable
1. Full screen image modals | To show the full image in a pleasing way not possible using a regular page
1. Add comments to pictures | Encourages greater interaction from users
1. Add business account types and tags | Add an additional perspective to images and history

## Testing

This information is held in the [Testing](TESTING.md) file.

## Development Life Cycle

This section is to provide a brief insight into how the approach to the code structure of the website was expected to work, what changed and why, and then to summarise how the creator would now approach replicating the project.

Changes to design are documented in the [UX section](#ux) under [wireframes](#wireframes).

The project was deployed using GitHub linked Heroku, once the basic structure of the page was complete.  This allowed for continuous delivery as each major change was made, pushed and merged and enabled testing of the page throughout development on different devices.  It also reduced the pressure towards submission, as all wrinkles relating to config vars and mail app passwords had been addressed.

### **Reflections on General Approach to Build**

### **Lessons Learned**
As always with these projects, understand the languages and frameworks better before starting so that it is known what can be achieved rather than going through various iterations to find something that works.

#### Preparation
Did not anticipate the need to store images as have only worked on standard server hosted sites to date.  Heroku and MongoDB both have very limited storage options and finding Cloudinary was a lifeline for the project.

#### Build
Did not understand how Flask routing passes information to and retrieves information from the templates.  This led to enormous confusion trying to get user profiles and single image views to work, however persistence rewarded with understanding, so lots of code refactored throughout the project.

### **Revised Development Process**
Based on the experience of producing the website, the creator would now take the following approach.

#### Preparation
Take into account live environment and the limitations it introduces, not just the code and data structure.  Be realistic and aim for a project that people will enjoy using, not just a concept which has caught the imagination.

#### Build
Knowing how the mini framework actually passes and receives information between models and views is critical to an efficient build.  Ideally, smaller projects would be undertaken prior to commencing in order to consolidate understanding gained from tutorials.

## Deployment
The website was created using [GitPod](https://www.gitpod.io/). Version control was undertaken by committing to [Git](https://git-scm.com/) and pushing to [GitHub](https://github.com/) using the functions within GitPod.  [Heroku]((https://heroku.com/)) was used to deploy the live site.

### **Deployment of the Page**
Continuous deployment via GitHub-Heroku link was utilised for this project.  As such, deployment was amongst the first tasks undertaken.
1. In the IDE, ensure that a small test application exists, and all changes are committed and pushed to GitHub.
1. Create a requirements file, which will be used by Heroku in creation of the deployment.
    * In the terminal, type "pip3 freeze --local > requirements.txt".
    * Commit this to Git.
1. Create a Procfile, which is used by Heroku to determine the language for the app.
    * In the terminal, type "echo web: python app.py > Procfile".
    * This is case sensitive, and should have a capital P, and should have no file extension.
    * Commit this to Git.
1. Push these files to GitHub.
1. [Sign in to Heroku](https://id.heroku.com/login) (or [create a Heroku account](https://signup.heroku.com/) if you do not already have one), and choose "New > Create New App".
![Heroku Dashboard snip](readme-files/heroku-1.png)
1. Choose an app name, which must be unique, and select the nearest region.  Then click "Create App".
![Heroku new app snip](readme-files/heroku-2.png)
1. Once generated choose the "Deploy" tab, select "Connect to GitHub" sub-tab and click the "Connect to GitHub" button.
![Heroku Deploy snip](readme-files/heroku-3.png)
![Heroku GitHub snip](readme-files/heroku-4.png)
1. Follow the on-screen instructions to link Heroku to your GitHub account.
1. Click the "Settings" tab from the main menu, and scroll down to find "Reveal Config Vars".  This section should be populated with any sensitive data which is not appropriate to send to GitHub, usually in an "env.py" document.
![Heroku GitHub snip](readme-files/heroku-vars.png)
1. Back on the Deploy tab, once linked, Heroku will prompt for the repository name, complete this and click "Search".
![Heroku GitHub snip](readme-files/heroku-5.png)
1. The repo listing should appear, click "Connect".
1. Heroku will process the request before showing that the connection has been made successfully, and showing two new options.  Click the first of these, which is to "Enable Automatic Deploys".
![Heroku GitHub snip](readme-files/heroku-6.png)
1. The second option is to "Deploy Branch".  Click the button and Heroku will process for some time.
![Heroku GitHub snip](readme-files/heroku-7.png)
1. Once complete, Heroku will display a checklist, followed by a "View" button.  Click this to open the app in a new tab.
![Heroku GitHub snip](readme-files/heroku-8.png)
1. Celebrate! Your app should now update in line with any changes pushed to GitHub.

### **How to Clone and Run the Code Locally**
There are slightly different approaches should you choose to use GitPod to clone the project, or a local IDE.

#### Cloning a Project into GitPod
1. Use [Google Chrome](https://www.google.com/intl/en_uk/chrome/). *(This can also be undertaken in Firefox)*
1. If you do not already have one, [create a GitHub account](https://github.com/join).
1. Install the [GitPod browser extension for Chrome](https://chrome.google.com/webstore/detail/gitpod-dev-environments-i/dodmmooeoklaejobgleioelladacbeki). *(Or Firefox if appropriate)*
1. Restart Chrome.
1. In GitHub, find the [project repository](https://github.com/ci-14-task-manager).
1. From the repository menu, choose the green GitPod button.
![GitPod button snip](readme-files/cloning-gitpod.png)
1. A new GitPod workspace will open containing the project code.

#### Cloning a Project into a Local IDE
1. Navigate to the [GitHub Repository](https://github.com/ci-14-task-manager).
1. Choose the Code dropdown menu, and copy the URL.
![GitHub code download snip](readme-files/clone-local-ide.png)
1. Open your local IDE and then open a terminal.
1. Set the current working directory to your preferred location for the cloned project.
1. Type in "git clone " followed by the copied URL. Be sure to include a space between git clone and the url, then press enter.
1. The cloned project will be created.

You can find more information on cloning a repository from GitHub [here](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository).

## Technologies Used

### **Languages**
* [HTML5](https://www.w3.org/) is used to provide the basic structure of the website.
* [CSS3](https://www.w3.org/) is used to provide most of the styling for the website.
* [JavaScript](https://www.javascript.com/) is used to provide the interactive nature of some components throughout the website, including the map.
* [Python3](https://www.python.org/) is used to write the logic and back end code for the website.

### **Libraries and Frameworks**
* [Bootstrap 5](https://getbootstrap.com/) is used to provide fundamental styling and structure.
* [jQuery](https://jquery.com/) is used to simplify the implementation of interactive JavaScript components.
* [Flask](https://flask.palletsprojects.com/en/2.0.x/) is used to provide a structure the Python application, and make use of the Jinja templating language.
* [Flask Pymongo](https://flask-pymongo.readthedocs.io/en/latest/) was used to allow Flask to communicate with MongoDB.
* [DNS Python](https://www.dnspython.org/) was installed in order to use the Mongo SRV connection string.
* [Flask_WTF](https://flask-wtf.readthedocs.io/en/1.0.x/) and [WTForms](https://wtforms.readthedocs.io/en/3.0.x/validators/) are used to provide form structure, functionality and data validation.
* [Werkzeug](https://werkzeug.palletsprojects.com/en/2.0.x/) is used to provide user security around passwords and storage.
* [Flask-Mail](https://pythonhosted.org/flask-mail/) is used to facilitate email sending from the contact form.
* [Flask-Talisman](https://github.com/GoogleCloudPlatform/flask-talisman) is used to force https and provide other basic security considerations.
* [Cloudinary](https://support.cloudinary.com/) is used to store, manipulate and manage the images.
* [Google Fonts](https://fonts.google.com/) are used to provide the typography for the website.
* [Font Awesome](https://fontawesome.com/) is used to provide the icons for the website.
* [Google ReCaptcha](https://www.google.com/recaptcha/) is used to protect the contact and sign up forms.
* [Google Maps](https://www.google.com/maps) provides the map, location indicator and marker

### **Tools**
* [Git](https://git-scm.com/)/[GitHub](https://github.com/) was used for version control and repository storage.
* [GitPod](https://www.gitpod.io/) was the IDE used to write the project.
* [Chrome Dev Tools](https://developers.google.com/web/tools/chrome-devtools) were used for specific responsiveness testing and drilling down into bug fixing.
* [Lighthouse](https://developers.google.com/web/tools/lighthouse) was used for macro testing and identification of errors for rectification.
* [W3C CSS Validation Service](https://jigsaw.w3.org/css-validator/) was used to remove any remaining errors in CSS code.
* [W3C HTML Validation Service](https://validator.w3.org/) was used to remove any remaining errors in HTML code.
* [JS Hint Validation Service](https://jshint.com/) was used to check for major errors in JavaScript.
* [Responsively](https://responsively.app/) was used to explore responsiveness across various devices.
* [RandomKeyGen](https://randomkeygen.com/) was used to produce the database Secret Key, amongst other security.
* [Flaticon](https://www.flaticon.com/) was used to make the favicon.

### **Other Resources**
* [Code Institute Full Template](https://github.com/Code-Institute-Org/gitpod-full-template) was used to set up the repository.

## Credits

### **Website Credits**
The following resources provided strong underlying understanding for items within the website, even where the approach has ended up being different.
* General understanding of model, view, controller concept in relation to Flask came from [Real Python](https://realpython.com/the-model-view-controller-mvc-paradigm-summarized-with-legos/) article
* Forms - [Hackers & Slackers](https://hackersandslackers.com/flask-wtforms-forms/) tutorial.
* Recaptcha link up - [Easy ReCAPTCHA with Flask-WTF](https://john.soban.ski/add-recaptcha-to-your-flask-application.html) blog.
* Contact email sending - [Intro to Flask: Adding a Contact Page](https://code.tutsplus.com/tutorials/intro-to-flask-adding-a-contact-page--net-28982) tutorial and [Mailtrap Flask Email Sending](https://mailtrap.io/blog/flask-email-sending/) article.
* Dynamic select for upload form - Stack Overflow articles [here](https://stackoverflow.com/questions/43548561/populate-a-wtforms-selectfield-with-an-sql-query/43551126) and [here](https://stackoverflow.com/questions/23273123/list-all-values-of-a-certain-field-in-mongodb)
* Edit post form populate content from [Stack Overflow thread](https://stackoverflow.com/questions/12099741/how-do-you-set-a-default-value-for-a-wtforms-selectfield)
* Force https from blog post recommended by Heroku, [From http to https](https://betterprogramming.pub/from-http-to-https-easily-secure-flask-web-apps-with-talisman-3359692d3eac)

#### Content

The website does not really contain any standalone content in terms of imagery, all content is uploaded by users.

#### Media
* The 6 black and white photographs uploaded to the website by the admin account were taken from a local news [article published in the Bournemouth Echo](https://www.bournemouthecho.co.uk/news/19381037.pictures-shaftesbury-old-postcards---part-1-2/)

* The other photographs uploaded to the website as at release were taken by the creator.

#### Acknowledgements
Thank you in particular to:
* Reuben Ferrante for mentoring the project.
* My poor, poor family for being made to try out every single deployment.

### **README Credits**

#### Content
Structure and content based heavily on:
* [Code Institute Solutions - README Template](https://github.com/Code-Institute-Solutions/readme-template)
* [Daisy McGirr - Code Institute Testing Webinar](https://us02web.zoom.us/rec/play/9FIKllHX2ZiQNFRhYPn_hBh_ZeA8964ZvIDLnhpKGAf1NLVc3_hBJ6zSL8Hv5Hx7ALnPtDmbg8CmFAs.YVsZ9LR_uI7OjEwH)

#### Media
The images for this README are from the following sources:
* Snips taken from GitHub.
* [Am I Responsive](http://ami.responsivedesign.is/).
* Wireframes created with [Balsamiq](https://balsamiq.com/).
* Colour mockups created with [Coolors](https://coolors.co/).
* Snips taken of Google Fonts.

#### Other
* Markdown basic taken from [Mastering Markdown](https://guides.github.com/features/mastering-markdown/).

**This website was produced as an educational project for the Code Institute Full Stack Development course.**

**Created by Amy Hacker.**

[Back to Top](#imprint)