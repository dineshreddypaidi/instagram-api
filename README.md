# Instagram-Like API Documentation

## Authentication

All endpoints require authentication except for the **Register** and **Login** endpoints. After logging in, the user will receive a token, which must be included in the header of subsequent requests as follows:

```
Authorization: Token {user_key}
```

## Base URL

```
https://instagram-api.up.railway.app
```

## Endpoints

### 1. User Endpoints

#### a. Get Logged-In User

- **URL:** `/user`
- **Method:** `GET`
- **Authentication:** Required
- **Description:** Retrieve the details of the logged-in user.

**Response:**

- **200 OK**
  ```json
  {
      "id": "user_id",
      "username": "user_name",
      "email": "user_email",
      ...
  }
  ```
- **401 Unauthorized**
  ```json
  {
      "error": "Authentication credentials were not provided."
  }
  ```

#### b. Register User

- **URL:** `/user/register`
- **Method:** `POST`
- **Authentication:** Not required
- **Description:** Register a new user.

**Request Body:**

```json
{
    "username": "new_user",
    "email": "user_email",
    "password": "user_password"
}
```

**Response:**

- **201 Created**
  ```json
  {
      "message": "User registered successfully."
  }
  ```
- **400 Bad Request**
  ```json
  {
      "error": "Username already exists."
  }
  ```

#### c. Login User

- **URL:** `/user/login`
- **Method:** `POST`
- **Authentication:** Not required
- **Description:** Log in a user and return an authentication token.

**Request Body:**

```json
{
    "username": "existing_user",
    "password": "user_password"
}
```

**Response:**

- **200 OK**
  ```json
  {
      "token": "user_token"
  }
  ```
- **401 Unauthorized**
  ```json
  {
      "error": "Invalid credentials."
  }
  ```

#### d. Logout User

- **URL:** `/user/logout`
- **Method:** `POST`
- **Authentication:** Required
- **Description:** Log out the logged-in user.

**Response:**

- **200 OK**
  ```json
  {
      "message": "User logged out successfully."
  }
  ```

### 2. Follower Endpoints

#### a. User Followers

- **URL:** `/user/follower`
- **Method:** `GET`, `POST`, `DELETE`
- **Authentication:** Required
- **Description:** Manage user followers.

**Response:**

- **200 OK** (GET)
  ```json
  {
      "followers": ["follower1", "follower2", ...]
  }
  ```
- **201 Created** (POST)
  ```json
  {
      "message": "Successfully followed."
  }
  ```
- **204 No Content** (DELETE)
  ```json
  {
      "message": "Successfully unfollowed."
  }
  ```

#### b. User Following

- **URL:** `/user/following`
- **Method:** `GET`, `DELETE`
- **Authentication:** Required
- **Description:** Retrieve and manage users being followed.

**Response:**

- **200 OK** (GET)
  ```json
  {
      "following": ["user1", "user2", ...]
  }
  ```
- **204 No Content** (DELETE)
  ```json
  {
      "message": "Successfully unfollowed."
  }
  ```

### 3. Post Endpoints

#### a. User Post

- **URL:** `/user/post`
- **Method:** `GET`, `POST`
- **Authentication:** Required
- **Description:** Retrieve or create user posts.

**Response:**

- **200 OK** (GET)
  ```json
  {
      "posts": [
          {
              "post_id": "1",
              "caption": "First post!",
              "likes": 10,
              ...
          },
          ...
      ]
  }
  ```
- **201 Created** (POST)
  ```json
  {
      "message": "Post created successfully."
  }
  ```

#### b. Post Like

- **URL:** `/post/like/<str:post_id>`
- **Method:** `GET`, `POST`, `DELETE`
- **Authentication:** Required
- **Description:** Manage likes on a post.

**Response:**

- **200 OK** (GET)
  ```json
  {
      "likes": 15
  }
  ```
- **201 Created** (POST)
  ```json
  {
      "message": "Post liked."
  }
  ```
- **204 No Content** (DELETE)
  ```json
  {
      "message": "Like removed."
  }
  ```

#### c. Post Comment

- **URL:** `/post/comment/<str:post_id>`
- **Method:** `GET`, `POST`, `PUT`, `DELETE`
- **Authentication:** Required
- **Description:** Manage comments on a post.

**Response:**

- **200 OK** (GET)
  ```json
  {
      "comments": [
          {
              "comment_id": "1",
              "content": "Nice post!",
              ...
          },
          ...
      ]
  }
  ```
- **201 Created** (POST)
  ```json
  {
      "message": "Comment added."
  }
  ```
- **204 No Content** (PUT)
  ```json
  {
      "message": "Comment updated."
  }
  ```
- **204 No Content** (DELETE)
  ```json
  {
      "message": "Comment deleted."
  }
  ```

### 4. User Profile Endpoints

#### a. User Following

- **URL:** `/user/<str:username>/following`
- **Method:** `GET`
- **Authentication:** Required
- **Description:** Get the list of users that the specified user is following.

**Response:**

- **200 OK**
  ```json
  {
      "following": ["user1", "user2", ...]
  }
  ```

#### b. User Followers

- **URL:** `/user/<str:username>/followers`
- **Method:** `GET`
- **Authentication:** Required
- **Description:** Get the list of followers for the specified user.

**Response:**

- **200 OK**
  ```json
  {
      "followers": ["follower1", "follower2", ...]
  }
  ```

#### c. User Profile

- **URL:** `/user/u/<str:username>`
- **Method:** `GET`
- **Authentication:** Required
- **Description:** Get the profile of the specified user.

**Response:**

- **200 OK**
  ```json
  {
      "id": "user_id",
      "username": "user_name",
      "email": "user_email",
      ...
  }
  ```

#### d. User Posts

- **URL:** `/user/u/<str:username>/post`
- **Method:** `GET`
- **Authentication:** Required
- **Description:** Get all posts made by the specified user.

**Response:**

- **200 OK**
  ```json
  {
      "posts": [
          {
              "post_id": "1",
              "caption": "User's first post!",
              ...
          },
          ...
      ]
  }
  ```

### Error Codes

- **400 Bad Request:** The request could not be understood or was missing required parameters.
- **401 Unauthorized:** Authentication failed or user does not have permissions for the desired action.
- **404 Not Found:** The requested resource could not be found.
- **500 Internal Server Error:** An error occurred on the server.

## Notes

- Responses are returned in JSON format.
- All response codes will be included as per standard HTTP status codes.
- Example requests and responses are based on common scenarios and may vary based on actual data.
