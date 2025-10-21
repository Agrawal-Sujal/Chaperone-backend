# 🔐 1️⃣ REGISTER USER

**URL:**  
`POST http://localhost:8000/api/register/`

**Description:**  
Register a new user.

**Request Body (JSON):**

```json
{
  "email": "test@example.com",
  "password": "mypassword123"
}
```

**Response (201 Created):**

```json
{
  "token": "32c93a890df4b62db2d924ee245fdcb9b9f792f1",
  "id": 1
}
```

**Errors (409 Conflict):**

```json
{
  "error": ["This email is already registered."]
}
```

**Errors (500 Internal Error):**

```json
{
  "error": ["Something went wrong try again later"]
}
```

---

# 🔑 2️⃣ LOGIN USER

**URL:**  
`POST http://localhost:8000/api/login/`

**Description:**  
Login an existing user and get authentication token.

**Request Body (JSON):**

```json
{
  "email": "test@example.com",
  "password": "mypassword123"
}
```

**Response (200 OK):**

```json
{
  "token": "32c93a890df4b62db2d924ee245fdcb9b9f792f1",
  "id": 1
}
```

**Error (404 Not Found):**

```json
{
  "error": ["Email does not exist or invalid credentials"]
}
```

**Errors (500 Internal Error):**

```json
{
  "error": ["Something went wrong try again later"]
}
```

---

# 🟢 3️⃣ GOOGLE AUTH

**URL:**  
`POST http://localhost:8000/api/google-auth/`

**Description:**  
Authenticate using Google Sign-In.

**Request Body (JSON):**

```json
{
  "id_token": "YOUR_GOOGLE_ID_TOKEN"
}
```

**Response (200 OK):**

```json
{
  "token": "32c93a890df4b62db2d924ee245fdcb9b9f792f1",
  "id": 1
}
```

**Error (400 Bad Request):**

```json
{ "error": "Invalid Google token" }
```

**Errors (500 Internal Error):**

```json
{
  "error": ["Something went wrong try again later"]
}
```

---

# 👤 4️⃣ UPDATE USER DETAILS

**URL:**  
`PUT http://localhost:8000/api/users/update/`  
or  
`PATCH http://localhost:8000/api/users/update/`

**Headers:**

```
Authorization: Bearer <your_token>
```

**Description:**  
Update basic user information.

**Request Body (JSON):**

```json
{
  "name": "New Name",
  "date_of_birth": "2002-05-15",
  "phone_number": 9876543210
}
```

**Response (200 OK):**

```json
{
  "message": "User details updated successfully"
}
```

**Error (500 Server Error):**

```json
{ "error": ["Something went wrong. Please try again later"] }
```

---

# 🔄 5️⃣ UPDATE USER ROLE (Walker/Wanderer)

**URL:**  
`PUT http://localhost:8000/api/users/update-role/`  
or  
`PATCH http://localhost:8000/api/users/update-role/`

**Headers:**

```
Authorization: Bearer <your_token>
```

**Description:**  
Switch between Walker and Wanderer roles.

**Request Body (JSON):**

```json
{
  "is_walker": true
}
```

**Response (200 OK):**

```json
{
  "message": "User promoted to Walker."
}
```

**OR**

```json
{
  "message": "User promoted to Wanderer."
}
```

**Error (500 Server Error):**

```json
{ "error": ["Something went wrong. Please try again later"] }
```

**Error (401 Unauthorized0):**

```json
{ "detail": "Authentication credentials were not provided." }
```

---

# 🚶‍♂️ 6️⃣ UPDATE WALKER INFO

**URL:**  
`PUT http://localhost:8000/api/update-walker/`  
or  
`PATCH http://localhost:8000/api/update-walker/`

**Headers:**

```
Authorization: Token <walker_token>
```

**Description:**  
Update Walker profile details, languages, and walking paces.

**Request Body (JSON):**

```json
{
  "photo_url": "https://example.com/photo.jpg",
  "about_yourself": "I love walking with new people!",
  "language_ids": [1, 2],
  "walking_pace_ids": [1]
}
```

**Response (200 OK):**

```json
{
  "message": "Walker info updated successfully."
}
```

**Error (403 Forbidden):**

```json
{ "error": "You are not allowed to perform this action." }
```

**Error (500 Server Error):**

```json
{ "error": ["Something went wrong. Please try again later"] }
```

**Error (401 Unauthorized0):**

```json
{ "detail": "Authentication credentials were not provided." }
```

---

# 🧭 7️⃣ UPDATE WANDERER PREFERENCES

**URL:**  
`PUT http://localhost:8000/api/update-wanderer-preferences/`  
or  
`PATCH http://localhost:8000/api/update-wanderer-preferences/`

**Headers:**

```
Authorization: Token <wanderer_token>
```

**Description:**  
Update preferences for a Wanderer — mobility assistance, languages, charities, and walking pace.

**Request Body (JSON):**

```json
{
  "need_mobility_assistance": true,
  "walking_pace_ids": [1, 2],
  "language_ids": [3, 4],
  "charity_ids": [1]
}
```

**Response (200 OK):**

```json
{
  "message": "Preferences updated successfully."
}
```

**Error (403 Forbidden):**

```json
{ "error": "You are not allowed to perform this action." }
```

**Error (500 Server Error):**

```json
{ "error": ["Something went wrong. Please try again later"] }
```

**Error (401 Unauthorized0):**

```json
{ "detail": "Authentication credentials were not provided." }
```

---
