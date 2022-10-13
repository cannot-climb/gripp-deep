# gripp-deep

[![Uptime Robot status](https://img.shields.io/uptimerobot/status/m792850623-58c0c6e3fcdf46f37875ea23)](https://stats.uptimerobot.com/YRoN9sDMOz)
[![Uptime Robot ratio (30 days)](https://img.shields.io/uptimerobot/ratio/m792850623-58c0c6e3fcdf46f37875ea23)](https://stats.uptimerobot.com/YRoN9sDMOz)

deep learning model and server of gripp

## API

### Accounts

Authorize: None
Fail: 401 Unauthorized

<details>
<summary>Obtain Token</summary>

url: accounts/token/obtain

- Request
  - username: string
  - password: string
- Response
  - access: string
  - token: string

access token lifetime: 5 min
refresh token lifetime: 30 day

</details>
<details>

url: accounts/token/refresh

<summary>Refresh Token</summary>

- Request
  - refresh: string
- Response
  - access: string

access token lifetime: 5 min

</details>

### KilterBoard

Authorize: Bearer Token
Fail: 401 Unauthorized

<details>
<summary>predict</summary>

- Request
  - videoUrl: string
- Response
  - videoUrl: string
  - success: bool
  - startTime: str
  - endTime: str

</details>
