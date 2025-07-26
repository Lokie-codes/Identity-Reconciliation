# Identity Reconciliation

## Overview

FluxKart.com sells parts for building contraptions, and Bitespeed helps manage their customer experience. The challenge is to link different orders made with varying contact information to the same person. For example, if a user places orders with different emails or phone numbers, we need to identify and group these as belonging to the same user.

Contacts are linked if they share either an email or phone number. When a new request arrives:

- If both email and phone match an existing contact, no new contact is created.
- If either email or phone matches, the earliest contact becomes primary; others become secondary.
- If neither matches, a new primary contact is created.

## API Endpoint

Create an endpoint `/identify` that accepts HTTP POST requests with `email` and/or `phoneNumber`, and responds with the user’s emails, phone numbers, and related secondary contacts.

## Database Schema

**Contact Table**

| Column Name      | Data Type   | Description                                                      |
|------------------|------------|------------------------------------------------------------------|
| id               | INTEGER    | Unique identifier for the contact                                |
| phoneNumber      | String?    | Phone number of the contact                                      |
| email            | String?    | Email address of the contact                                     |
| linkedId         | INTEGER?   | ID of another contact linked to this one                         |
| linkPrecedence   | "primary"/"secondary" | Indicates if this contact is primary or secondary      |
| createdAt        | DateTime   | Timestamp when the contact was created                           |
| updatedAt        | DateTime   | Timestamp when the contact was last updated                      |
| deletedAt        | DateTime?  | Timestamp when the contact was deleted, if applicable            |

## Example Scenarios

### Initial State

| id | phoneNumber | email                    | linkedId | linkPrecedence | createdAt                | updatedAt                | deletedAt |
|----|-------------|--------------------------|----------|----------------|--------------------------|--------------------------|-----------|
| 1  | 123456      | lorraine@hillvalley.edu  | null     | primary        | 2023-04-01 00:00:00.374+00 | 2023-04-01 00:00:00.374+00 | null      |
| 23 | 123456      | mcfly@hillvalley.edu     | 1        | secondary      | 2023-04-20 05:30:00.11+00  | 2023-04-20 05:30:00.11+00  | null      |

#### Request

```json
{
	"email": "mcfly@hillvalley.edu",
	"phoneNumber": "123456"
}
```

#### Response

```json
{
	"contact": {
		"primaryContactId": 1,
		"emails": ["lorraine@hillvalley.edu", "mcfly@hillvalley.edu"],
		"phoneNumbers": ["123456"],
		"secondaryContactIds": [23]
	}
}
```

---

If no existing contact matches, create a new primary contact:

#### Request

```json
{
	"email": "newunkonown@hillvalley.edu",
	"phoneNumber": "789012"
}
```

#### Response

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

---

If a request matches email and phone across records, update the earliest record to primary and link others as secondary:

### Initial State

| id | phoneNumber | email                    | linkedId | linkPrecedence | createdAt                | updatedAt                | deletedAt |
|----|-------------|--------------------------|----------|----------------|--------------------------|--------------------------|-----------|
| 11 | 919191      | george@hillvalley.edu    | null     | primary        | 2023-04-11 00:00:00.374+00 | 2023-04-11 00:00:00.374+00 | null      |
| 27 | 717171      | biffsucks@hillvalley.edu | null     | primary        | 2023-04-21 05:30:00.11+00  | 2023-04-21 05:30:00.11+00  | null      |

#### Request

```json
{
	"email": "george@hillvalley.edu",
	"phoneNumber": "717171"
}
```

#### Response

```json
{
	"contact": {
		"primaryContactId": 11,
		"emails": ["george@hillvalley.edu", "biffsucks@hillvalley.edu"],
		"phoneNumbers": ["919191", "717171"],
		"secondaryContactIds": [27]
	}
}
```

### Updated State

| id | phoneNumber | email                    | linkedId | linkPrecedence | createdAt                | updatedAt                | deletedAt |
|----|-------------|--------------------------|----------|----------------|--------------------------|--------------------------|-----------|
| 11 | 919191      | george@hillvalley.edu    | null     | primary        | 2023-04-11 00:00:00.374+00 | 2023-04-21 05:30:00.11+00 | null      |
| 27 | 717171      | biffsucks@hillvalley.edu | 11       | secondary      | 2023-04-21 05:30:00.11+00  | 2023-04-21 05:30:00.11+00  | null      |

---

## Implementation with Django Rest Framework

### Setup

Activate your virtual environment and install dependencies:

```bash
python -m venv venv
# source venv/bin/activate  # macOS/Linux
venv\Scripts\activate       # Windows
pip install -r requirements.txt
```

Migrate the database:

```bash
python manage.py migrate
```

Run the server:

```bash
python manage.py runserver
```

### Testing the Endpoint

Use curl or Postman to test:

```bash
curl --location 'http://localhost:8000/identify/' \
--header 'Content-Type: application/json' \
--data-raw '{
	"email": "yousuck@hillvalley.edu",
	"phoneNumber": "123456"
}'
```
