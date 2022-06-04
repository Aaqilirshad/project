# E-$tore : An online Store
#### Video Demo: https://youtu.be/LE2C7J6aDVE
#### Description: 
**E-$tore** is an online store where you can buy or sell products. On the homepage you'll see all the products from there you can add the item to the wishlist or Contact the seller Through Email, A message will be automated for you if you wish, you can edit the message to whatever you want. The Navigation Bar contains five different paths Home, Sell Your item, Wishlist, My items and logout.

**Sell Your item** is where you can sell you're own item. You should enter product name along with the description and price and you should select the Category from the dropdown menu, Sellers email address is must. With those details you can post the product on the website. When someone contacted the seller Through the contact forum, seller will see their message in their inbox.

**Wishlist** is where you can see all the items you wish to buy, you can add an item to the wishlist by clicking on an item and clicking on "Add to Wishlist" you can also contact the seller from there. You can also remove items from wishlist.

**My items** is where you'll see all the items that you have posted on the website, From there you'll be able to remove items that you have posted.

##### Code:
This web app is developed using Flask. The application has many routes in app.py,  some function declarations in helpers.py and a database file called "shopper.db". 

The sell app route in app.py uses get and post methods, post method is used to submit the form with details of the product and the get method is used to render the template sell.html .
sell.html has a form with multiple fields.

The wishlist app route uses get and post methods, post method is used to add an item to the wishlist by a SQL command. Get method is used to gather the items that have been added to the wishlist by the particular user and display it on wishlist.html using table.A SQL command is used in this case.

The login method also uses both Get and Post methods. With post method and by using some SQL commands both username and password are checked. If they don't match, an apology message will be returned, else the user will be logged in. Get method is used to render the template login.html .

The Register route uses post method to add the new username and the hash of password to the database. An apology message is returned when the username is already exists or when both the password and confirmation password don't match.The route uses Get method to render the template register.html .

And the route called "My items" uses get method to gather the items that the particular user posted and Post method to delete the selected item. 

And finally this application is configured for mail support. It sends an E-mail to the seller when a customer uses the contact forum to send a message to the seller,  By default a message will be automated for the customer describing the product.