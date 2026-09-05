Booking management 

List of function: 

1\. Auth \- CreateToken 

2\. Booking \- GetBookingIds 

3\. Booking \- GetBooking 

4\. Booking \- CreateBooking 

5\. Booking \- UpdateBooking 

6\. Booking \- PartialUpdateBooking 

7\. Booking \- DeleteBooking 

**1\. Auth \- CreateToken** 

Creates a new auth token to use for access to the **PUT** and **DELETE** /booking 

**POST**: https://restful-booker.herokuapp.com/auth 

*{* 

*"username" : "admin",* 

*"password" : "password123"* 

*}* 

**Header** 

| Field  | Type  | Description |
| :---- | :---- | :---- |
| Content-Type **required**  | string  | Sets the format of payload you are sending Default value: application/json |

**Request body**

| Field  | Type  | Description |
| :---- | :---- | :---- |
| username **required**  | String  | Username for authentication  Default value: admin |
| password **required**  | String  | Password for authentication  Default value: password123 |

**Success 200** 

| Field  | Type  | Description |
| :---- | :---: | :---- |
| token  | String | Token to use in future requests |

● Response: 

HTTP/1.1 200 OK 

*{* 

*"token": "abc123"* 

*}* 

**2\. All Booking \- GetBookingIds** 

Returns the ids of all the bookings that exist within the API. Can take optional query strings to search and return a subset of booking ids. 

GET: https://restful-booker.herokuapp.com/booking 

**Success 200** 

| Field  | Type  | Description |
| :---- | ----- | ----- |
| object  | object  \[\] | Array of objects that contain unique booking IDs |
| bookingid  | numb  er | ID of a specific booking that matches search criteria |

● Response: 

**HTTP/1.1 200 OK** 

\[ 

{ 

"bookingid": 1 

},  
{ 

"bookingid": 2 

}, 

{ 

"bookingid": 3 

}, 

{ 

"bookingid": 4 

} 

\] 

**3\. A Booking \- GetBooking** 

Returns a specific booking based upon the booking id provided 

**GET**: https://restful-booker.herokuapp.com/booking/id 

**Header** 

| Field  | Type  | Description |
| :---- | :---: | :---- |
| Accept **required**  | string  | Sets what format the response body is returned in. Can be application/json or application/xml  Default value: application/json |

**Url Parameter** 

| Field  | Type  | Description |
| :---- | :---: | :---- |

id String The id of the booking you would like to retrieve 

**Success 200**

| Field  | Type  | Description |
| :---- | :---- | :---- |
| firstname  | String  | Firstname for the guest who made the booking |

| lastname  | String  | Lastname for the guest who made the booking |
| :---- | :---- | :---- |
| totalprice  | Number  | The total price for the booking |
| depositpaid  | Boolean  | Whether the deposit has been paid or not |
| bookingdates  | Object  | Sub-object that contains the checkin and checkout dates |
| checkin  | Date  | Date the guest is checking in |
| checkout  | Date  | Date the guest is checking out |
| additionalneeds  | String  | Any other needs the guest has |

● Response: 

**HTTP/1.1 200 OK** 

{ 

"firstname": "Sally", 

"lastname": "Brown", 

"totalprice": 111, 

"depositpaid": true, 

"bookingdates": { 

"checkin": "2013-02-23", 

"checkout": "2014-10-23" 

}, 

"additionalneeds": "Breakfast" 

} 

**4\. Booking \- CreateBooking** 

Creates a new booking in the API  
**POST**: https://restful-booker.herokuapp.com/booking 

{ 

"firstname" : "Jim", 

"lastname" : "Brown", 

"totalprice" : 111, 

"depositpaid" : true, 

"bookingdates" : { 

"checkin" : "2018-01-01", 

"checkout" : "2019-01-01" 

}, 

"additionalneeds" : "Breakfast" 

} 

**Header** 

| Field  | Type  | Description |
| :---- | :---: | :---- |
| Content-Type **required**  | string  | Sets the format of payload you are sending. Can be application/json or text/xml  Default value: application/json |
| Accept **required**  | string  | Sets what format the response body is returned in. Can be application/json or application/xml  Default value: application/json |

**Request body**

| Field  | Type  | Description |
| :---- | :---- | :---- |
| firstname **required**  | String  | Firstname for the guest who made the booking |
| lastname **required**  | String  | Lastname for the guest who made the booking |

| totalprice required  | Number  | The total price for the booking |
| :---- | ----- | ----- |
| depositpaid **required**  | Boolean  | Whether the deposit has been paid or not |
| checkin **required**  | Date  | Date the guest is checking in |
| checkout **required**  | Date  | Date the guest is checking out |
| additionalneeds **optional**  | String  | Any other needs the guest has |

**Success 200**

| Field  | Type  | Description |
| :---- | :---- | :---- |
| bookingid  | Number  | ID for newly created booking |
| booking  | Object  | Object that contains |
| firstname  lastname  | String  String  | Firstname for the guest who made the booking  Lastname for the guest who made the booking |
| totalprice  | Number  | The total price for the booking |
| depositpaid  | Boolean  | Whether the deposit has been paid or not |

| bookingdates  | Object  | Sub-object that contains the checkin and checkout dates |
| :---- | :---- | :---- |
| checkin  | Date  | Date the guest is checking in |
| checkout  | Date  | Date the guest is checking out |
| additionalneeds  | String  | Any other needs the guest has |

● Response: 

**HTTP/1.1 200 OK** 

{ 

"bookingid": 1, 

"booking": { 

"firstname": "Jim", 

"lastname": "Brown", 

"totalprice": 111, 

"depositpaid": true, 

"bookingdates": { 

"checkin": "2018-01-01", 

"checkout": "2019-01-01" 

}, 

"additionalneeds": "Breakfast" 

} 

} 

**5\. Booking \- UpdateBooking** 

Updates a current booking 

PUT: https://restful-booker.herokuapp.com/booking/id 

{ 

"firstname" : "James", 

"lastname" : "Brown", 

"totalprice" : 111, 

"depositpaid" : true, 

"bookingdates" : {  
"checkin" : "2018-01-01", 

"checkout" : "2019-01-01" 

}, 

"additionalneeds" : "Breakfast" 

} 

**Header**

| Field  | Type  | Description |
| :---- | :---: | :---- |
| Content-Type **required**  | string  | Sets the format of payload you are sending. Can be application/json or text/xml  Default value: application/json |
| Accept **required**  | string  | Sets what format the response body is returned in. Can be application/json or application/xml  Default value: application/json |
| Cookie **required**  | string  | Sets an authorisation token to access the PUT endpoint, can be used as an alternative to the Authorisation  Default value:  token=YWRtaW46cGFzc3dvcmQxMjM |
| Authorisation **required**  | string  | YWRtaW46cGFzc3dvcmQxMjM=\] Basic authorisation header to access the PUT endpoint, can be used as an alternative to the Cookie header  Default value: Basic  YWRtaW46cGFzc3dvcmQxMjM |

**Url Parameter** 

| Field  | Type  | Description |
| :---- | :---- | :---- |
| id **required**  | Number  | ID for the booking you want to update |

**Request body** 

| Field  | Type  | Description |
| :---- | :---- | :---- |
| firstname **required**  | String  | Firstname for the guest who made the booking |
| lastname **required**  | String  | Lastname for the guest who made the booking |
| totalprice **optional**  | Number  | The total price for the booking |
| depositpaid **optional**  | Boolean  | Whether the deposit has been paid or not |
| checkin **optional**  | Date  | Date the guest is checking in |
| checkout **optional**  | Date  | Date the guest is checking out |
| additionalneeds **optional**  | String  | Any other needs the guest has |

**Success 200**

| Field  | Type  | Description |
| :---- | :---- | :---- |

| firstname  | String  | Firstname for the guest who made the booking |
| :---- | :---- | :---- |
| lastname  | String  | Lastname for the guest who made the booking |
| totalprice  | Number  | The total price for the booking |
| depositpaid  | Boolean  | Whether the deposit has been paid or not |
| bookingdates  | Object  | Sub-object that contains the checkin and checkout dates |
| checkin  | Date  | Date the guest is checking in |
| checkout  | Date  | Date the guest is checking out |
| additionalneeds  | String  | Any other needs the guest has |

● Response: 

**HTTP/1.1 200 OK** 

{ 

"firstname" : "James", 

"lastname" : "Brown", 

"totalprice" : 111, 

"depositpaid" : true, 

"bookingdates" : { 

"checkin" : "2018-01-01", 

"checkout" : "2019-01-01" 

}, 

"additionalneeds" : "Breakfast" 

}  
**6\. Booking \- PartialUpdateBooking** 

Updates a current booking with a partial payload 

**PATCH**: https://restful-booker.herokuapp.com/booking/id 

{ 

"firstname" : "James", 

"lastname" : "Brown" 

} 

**Header**

| Field  | Type  | Description |
| :---- | :---: | :---- |
| Content-Type **required**  | string  | Sets the format of payload you are sending. Can be application/json or text/xml  Default value: application/json |
| Accept **required**  | string  | Sets what format the response body is returned in. Can be application/json or application/xml  Default value: application/json |
| Cookie **required**  | string  | Sets an authorisation token to access the PUT endpoint, can be used as an alternative to the Authorisation  Default value: token=  YWRtaW46cGFzc3dvcmQxMjM |
| Authorisation **required**  | string  | YWRtaW46cGFzc3dvcmQxMjM=\] Basic authorisation header to access the PUT endpoint, can be used as an alternative to the Cookie header  Default value: Basic  YWRtaW46cGFzc3dvcmQxMjM |

**Url Parameter** 

| Field  | Type  | Description |
| :---- | :---- | :---- |
| id **required**  | Number  | ID for the booking you want to update |

**Request body** 

| Field  | Type  | Description |
| :---- | :---- | :---- |
| firstname **required**  | String  | Firstname for the guest who made the booking |
| lastname **required**  | String  | Lastname for the guest who made the booking |
| totalprice **optional**  | Number  | The total price for the booking |
| depositpaid **optional**  | Boolean  | Whether the deposit has been paid or not |
| checkin **optional**  | Date  | Date the guest is checking in |
| checkout **optional**  | Date  | Date the guest is checking out |
| additionalneeds **optional**  | String  | Any other needs the guest has |

**Success 200**

| Field  | Type  | Description |
| :---- | :---- | :---- |

| firstname  | String  | Firstname for the guest who made the booking |
| :---- | :---- | :---- |
| lastname  | String  | Lastname for the guest who made the booking |
| totalprice  | Number  | The total price for the booking |
| depositpaid  | Boolean  | Whether the deposit has been paid or not |
| bookingdates  | Object  | Sub-object that contains the checkin and checkout dates |
| checkin  | Date  | Date the guest is checking in |
| checkout  | Date  | Date the guest is checking out |
| additionalneeds  | String  | Any other needs the guest has |

● Response: 

HTTP/1.1 200 OK 

{ 

"firstname" : "James", 

"lastname" : "Brown", 

"totalprice" : 111, 

"depositpaid" : true, 

"bookingdates" : { 

"checkin" : "2018-01-01", 

"checkout" : "2019-01-01" 

}, 

"additionalneeds" : "Breakfast" 

}  
**7\. Booking \- DeleteBooking** 

Returns the ids of all the bookings that exist within the API. Can take optional query strings to search and return a subset of booking ids. 

DELETE: https://restful-booker.herokuapp.com/booking/id 

**Header** 

| Field  | Type  | Description |
| :---- | :---: | :---- |
| Cookie **required**  | string  | Sets an authorisation token to access the DELETE endpoint, can be used as an  alternative to the Authorisation  Default value: token= |
| Authorisation **required**  | string  | YWRtaW46cGFzc3dvcmQxMjM=\] Basic authorisation header to access the DELETE endpoint, can be used as an alternative to the Cookie header  Default value: Basic |

**Url Parameter** 

| Field  | Type  | Description |
| :---- | :---- | :---- |

id **required** Number ID for the booking you want to update 

**Success 204** 

| Field  | Type  | Description |
| :---- | :---: | :---- |

Status String Default HTTP 204 response