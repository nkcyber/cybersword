from get_flag import get_flag_from

def get_page(flag: str) -> str:
    return f"""
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8" />
  <title>Hidden HTML</title>
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <meta name="description" content="There's more than meets the eye." />
  <link rel="stylesheet" type="text/css" href="style.css" />
  <link rel="icon" href="barty.png">
</head>

<body>
  <div class="container">
    <h1>There's more than meets the eye…</h1>
  </div>
  <!--
      Here you go:
       {flag}
    -->
</body>

</html>
    """

def main():  # expects to be run by Dockerfile via docker compose
    html_flag = get_flag_from("hidden_html.yml")
    with open('page1.html', 'w') as f:
        f.write(get_page(html_flag))

if __name__ == "__main__":
    main()

