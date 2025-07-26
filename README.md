# Identity-Reconciliation

Let's first try to understand whatever we know so far. We see that there is a user say Doc and there's FluxKart.com who sells parts building contraption. Bitespeed helps FluxKart.com manage customer experience. 
Problem we have is linking different orders made with different contact information to the same person.
We have to identify different email and phone numbers belonging to the same person. say in first order the user has 'abc' email, '123' phone and in second order 'xyz' email, '123' phone and in third order 'abc' email and '456' phone, then all these transactions belong to the same user. Contact rows are linked if they have either of email or phone as common.
so whenever there is a new request, 
if same email and phone, no new contact is created.
if same email or phone, then earliest becomes primary and others become secondary.
else no email or phone match, then its a new user and we make the record as primary.

Our goal is to create a endpoint /identify which recieves HTTP POST request with email and/or phoneNumber and respond with User with all the emails, phoneNumebrs and secondary contacts related to them.


Database table:

Contact
| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| id          | INTEGER   | Unique identifier for the contact |
| phoneNumber | String? | Phone number of the contact |
| email       | String?   | Email address of the contact |
| linkedId   | INTEGER?  | the ID of another Contact linked to this one
| linkPrecedence | "primary" | "secondary" | Indicates if this contact is primary or secondary in relation to the linked contact |
| createdAt   | DateTime  | Timestamp when the contact was created |
| updatedAt   | DateTime  | Timestamp when the contact was last updated |
| deletedAt  | DateTime? | Timestamp when the contact was deleted, if applicable |



Initial State of database:
| id | phoneNumber | email          | linkedId | linkPrecedence | createdAt           | updatedAt           | deletedAt |
|----|-------------|----------------|----------|----------------|---------------------|---------------------|------------|
| 1  | 123456      | lorraine@hillvalley.edu| null     | primary        | 2023-04-01 00:00:00.374+00 | 2023-04-01 00:00:00.374+00 | null       |
| 23 | 123456      | mcfly@hillvalley.edu | 1        | secondary      | 2023-04-20 05:30:00.11+00   | 2023-04-20 05:30:00.11+00   | null       |

HTTP POST request to /identify with body:
```json
{
	"email": "mcfly@hillvalley.edu",
	"phoneNumber": "123456"
}
```
In this case, the email and phone number match with the existing contact with id 23, which is a secondary contact linked to the primary contact with id 1. The response should include the primary contact details along with the secondary contacts.
```json

	{
		"contact":{
			"primaryContatctId": 1,
			"emails": ["lorraine@hillvalley.edu","mcfly@hillvalley.edu"]
			"phoneNumbers": ["123456"]
			"secondaryContactIds": [23]
		}
	}
```

If there is no existing contacts against an incoming request, we simply create a new record in the database with the provided email and phone number, and set it as primary contact.

Request to /identify with body:
```json
{
    "email": "newunkonown@hillvalley.edu",
    "phoneNumber": "789012"
}

```
```json
{
    "contact": {
        "primaryContactId": 24,
        "emails": ["newunkonown@hillvalley.edu"],
        "phoneNumbers": ["789012"],
        "secondaryContactIds": []
    }
}
```
So far so good.

If there is a request that matches email and phone across records, then we update the existing record to make it primary and link all other records with same email or phone as secondary.
intitial state of database:
| id | phoneNumber | email          | linkedId | linkPrecedence | createdAt           | updatedAt           | deletedAt |
|----|-------------|----------------|----------|----------------|---------------------|---------------------|------------|
| 11 | 919191      | george@hillvalley.edu | null     | primary        | 2023-04-11 00:00:00.374+00 | 2023-04-11 00:00:00.374+00 | null       |
| 27 | 717171      | biffsucks@hillvalley.edu | null     | primary        | 2023-04-21 05:30:00.11+00   | 2023-04-21 05:30:00.11+00   | null       |

Request to /identify with body:
```json
{
"email":"george@hillvalley.edu",
"phoneNumber": "717171"
}
```
then in the response we should have the primary contact with id 11 and secondary contact with id 27, and the email and phone numbers should be updated accordingly.
```json
	{
		"contact":{
			"primaryContatctId": 11,
			"emails": ["george@hillvalley.edu","biffsucks@hillvalley.edu"]
			"phoneNumbers": ["919191","717171"]
			"secondaryContactIds": [27]
		}
	}
```

New state of database:
| id | phoneNumber | email          | linkedId | linkPrecedence | createdAt           | updatedAt           | deletedAt |
|----|-------------|----------------|----------|----------------|---------------------|---------------------|------------|
| 11 | 919191      | george@hillvalley.edu | null     | primary        | 2023-04-11 00:00:00.374+00 | 2023-04-21 05:30:00.11+00 | null       |
| 27 | 717171      | biffsucks@hillvalley.edu | 11       | secondary      | 2023-04-21 05:30:00.11+00   | 2023-04-21 05:30:00.11+00   | null       |

this should be sufficient to get started with the implementation of the /identify endpoint.
I would proceed with Django Rest Framework to implement this endpoint as Python is easy to work with and the framework also provides an SQLite database for quick prototyping as they've asked for a SQL database to work with.

Installation:
First lets activate the virtual environment and install the required packages.
```bash
python -m venv venv
# source venv/bin/activate  # for macOS/Linux
`venv\Scripts\activate` # for windows
pip install -r requirements.txt
```
