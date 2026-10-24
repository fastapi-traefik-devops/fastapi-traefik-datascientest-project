# Backend endpoint guide

[Import/run instructions](README.md) · [Live results](TEST_REPORT.md)

The request examples cover the deployed DEV OpenAPI contract. Response examples in the full collection are illustrative, not captured successes.

| Method | Path | Bearer required | Purpose |
|---|---|---|---|
| POST | `/api/v1/login/access-token` | No | Login Access Token |
| POST | `/api/v1/login/test-token` | Yes | Test Token |
| POST | `/api/v1/password-recovery/{email}` | No | Recover Password |
| POST | `/api/v1/reset-password/` | No | Reset Password |
| POST | `/api/v1/password-recovery-html-content/{email}` | Yes | Recover Password Html Content |
| GET | `/api/v1/users/` | Yes | Read Users |
| POST | `/api/v1/users/` | Yes | Create User |
| GET | `/api/v1/users/me` | Yes | Read User Me |
| DELETE | `/api/v1/users/me` | Yes | Delete User Me |
| PATCH | `/api/v1/users/me` | Yes | Update User Me |
| PATCH | `/api/v1/users/me/password` | Yes | Update Password Me |
| POST | `/api/v1/users/signup` | No | Register User |
| GET | `/api/v1/users/{user_id}` | Yes | Read User By Id |
| PATCH | `/api/v1/users/{user_id}` | Yes | Update User |
| DELETE | `/api/v1/users/{user_id}` | Yes | Delete User |
| POST | `/api/v1/utils/test-email/` | Yes | Test Email |
| GET | `/api/v1/utils/health-check/` | No | Health Check |
| GET | `/api/v1/items/` | Yes | Read Items |
| POST | `/api/v1/items/` | Yes | Create Item |
| GET | `/api/v1/items/{id}` | Yes | Read Item |
| PUT | `/api/v1/items/{id}` | Yes | Update Item |
| DELETE | `/api/v1/items/{id}` | Yes | Delete Item |

## Login and authenticated reads

`POST /api/v1/login/access-token` takes **form URL-encoded** `username` (email) and `password`, not a JSON body. A successful response returns `access_token` and `token_type`. Subsequent protected requests send `Authorization: Bearer <access_token>`. No valid login was executed here.

The examples collection uses placeholders. Populate local-only values only for a future approved test account; do not export populated tokens/passwords.

## Item examples — not executed live

Create item request body:

```json
{"title":"API documentation example","description":"Synthetic fixture only"}
```

Update an owned fixture: `PUT /api/v1/items/{{item_id}}` with a body such as `{"title":"Updated fixture"}`. Read it using GET and remove only that test fixture using DELETE. These describe a future isolated CRUD exercise; this report claims no mutation/persistence result.

## User/admin and side effects

User listing and arbitrary user creation/update/delete require the documented permissions. Ordinary users access their own profile and owned items. Successful access-control separation between two authenticated users was not tested.

Signup, profile changes, password updates, account deletion, password recovery and test-email examples can create data or send messages when pointed at a real environment. They remain on the non-routable example host and were not run.
