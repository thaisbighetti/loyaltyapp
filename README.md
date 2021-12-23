# loyaltyapp

Loyalty app where a member can invite a new member by generating a coupon.

Some rules must be followed:
- An indicator can have multiple (unlimited) indications;
- A person can only be indicated by a single indicator. two different users cannot nominate the same person;
- The user cannot nominate himself (be nominated and nominate for the same nomination);
- The indication is valid for 30 days. After that, the nominee cannot accept the nomination and another member can make the nomination;
- Once the nomination is accepted, the person who was nominated cannot be indicated again

## Running the project

This project uses [docker](https://www.docker.com/) and [docker-compose](https://docs.docker.com/compose/).

Run:
``` 
docker-compose up --build loyaltyapp
``` 
To tests:

``` 
docker-compose up --build tests
``` 
Will be available [here](http://localhost:8000).

## Endpoints

   - **POST** register/ - Create a Member
   - **GET/UPDATE**  member/cpf - Get a specific user and update
   - **POST** coupon/ - Create a coupon
   - **GET** cpf1/coupon-to/cpf2 - Get all coupons generated from cpf1 to cpf2
   - **GET** search/coupon/ - On this page all coupons are listed and you can search for a specific coupon
   - **GET** search/member/ - On this page all members are listed and you can search for a specific member

## More about the project

Available on [Heroku](https://www.heroku.com/home), you can acess [here](https://thaisbighetti-loyaltyapp.herokuapp.com).