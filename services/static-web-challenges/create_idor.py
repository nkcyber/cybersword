# for ./challenges/web/hidden_idor/
from get_flag import get_flag_from

def get_page(flag: str) -> str:
    return f"""\
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8" />
  <title>Hidden IDOR</title>
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <meta name="description" content="Don't give anyone this link!" />
  <link rel="stylesheet" type="text/css" href="style.css" />
  <link rel="icon" href="barty.png">
</head>

<body>
  <div class="container">
    <h1>This is a secret!</h1>
    <code>
       {flag}
    </code>
  </div>
</body>

</html>
    """

def main():  # expects to be run by Dockerfile via docker compose
    idor_flag = get_flag_from("hidden_idor.yml")
    with open('page3.html', 'w') as f:
        f.write(get_page(idor_flag))

if __name__ == "__main__":
    main()

