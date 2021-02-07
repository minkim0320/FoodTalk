# FoodTalk

A new Webapp that enables customers and small restaurants, to, well, talk about food. This app helps connects businesses and their offers/items with local users!

## Inspiration
Small businesses have suffered throughout the COVID-19 pandemic. In order to help them get back on track once life comes back to normal, this app can attract new and loyal customers alike to the restaurant.

## What it does
Businesses can sign up and host their restaurant online, where users can search them up, follow them, and scroll around and see their items. Owners can also offer virtual coupons to attract more customers, or users can buy each other food vouchers that can be redeemed next time they visit the store.

## How we built it
The webapp was built using Flask and Google's Firebase for the backend development. Multiple flask modules were used, such as flask_login, flask_bcrypt, pyrebase, and more. HTML/CSS with Jinja2 and Bootstrap were used for the View (structuring of the code followed an MVC model).

## Challenges we ran into
-Restructuring of the project:
Sometime during Saturday, we had to restructure the whole project because we ran into a circular dependency, so the whole structure of the code changed making us learn the new way of deploying our code
-Many 'NoneType Object is not subscriptable', and not attributable errors
Getting data from our Firebase realtime database proved to be quite difficult at times, because there were many branches, and each time we would try to retrieve values we ran into the risk of getting this error. Depending on the type of user, the structure of the database changes but the users are similarly related (Business inherits from Users), so sometimes during login/registration the user type wouldn't be known properly leading to NoneType object errors.

-Having pages different for each type of user
This was not as much of a challenge as the other two, thanks to the help of Jinja2. However, due to the different pages for different users, sometimes the errors would return (like names returning as None, because the user types would be different).

## Accomplishments that we're proud of
-Having a functional search and login/registration system
-Implementing encryption with user passwords
-Implementing dynamic URLs that would show different pages based on Business/User type 
-Allowing businesses to add items on their menu, and uploading them to Firebase
-Fully incorporating our data and object structures in Firebase,

## What we learned
Every accomplishment is something we have learned. These are things we haven't implemented before in our projects. We learned how to use Firebase with Python, and how to use Flask with all of its other mini modules.

## What's next for foodtalk
Due to time constraints, we still have to implement businesses being able to post their own posts. The coupon voucher and gift receipt system have yet to be implemented, and there could be more customization for users and businesses to put on their profile, like profile pictures and biographies.
