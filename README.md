# gripp-deep
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
refresh token lifetime: 1 day
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
  - title: string
  - degree: int
  - difficulty: degree
- Response
  - success: bool
  - startTime: str
  - endTime: str

</details>
