# gripp-deep
deep learning model and server of gripp

## API
<details>
<summary>Obtain Token</summary>

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
<summary>Refresh Token</summary>

- Request
  - refresh: string
- Response
  - access: string
  - 
access token lifetime: 5 min  

</details>