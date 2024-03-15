# for ./challenges/web/jwt/
from get_flag import get_flag_from
import jwt
import time

SECRET = "super_duper_secret"  # assume secret doesn't matter, as we're not really using the JWT for authentication

def get_page(flag: str) -> str:
    data = {
        "iss": "ctf.nkcyber.org",
        "iat": round(time.time()),
        "sub": "your_id_here",
        "flag": flag
    }
    my_jwt = jwt.encode(data, SECRET, algorithm="HS256")

    return f"""\
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8" />
  <title>JWT Analysis</title>
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <meta name="description" content="It's JWT Time!" />
  <link rel="stylesheet" type="text/css" href="style.css" />
  <link rel="icon" href="barty.png">
</head>

<body>
  <div class="constrained container">
    <h1>Here's your JWT!</h1>
    <code>
       {my_jwt}
    </code>
  </div>
</body>

</html>
    """

def main():  # expects to be run by Dockerfile via docker compose
    jwt_flag = get_flag_from("jwt.yml")
    with open('page4.html', 'w') as f:
        f.write(get_page(jwt_flag))

if __name__ == "__main__":
    main()

