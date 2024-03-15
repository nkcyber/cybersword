# for ./challenges/web/hidden_js
import base64
from get_flag import get_flag_from

def get_page() -> str:
    return """\
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8" />
  <title>Hidden JavaScript</title>
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <meta name="description" content="There's more than meets the eye." />
  <link rel="stylesheet" type="text/css" href="style.css" />
  <link rel="icon" href="barty.png">
</head>

<body>
  <div class="container">
    <p>
        I've loaded the script in the page,
        but I don't know how to run the code.
    </p>
    <p>
        Can you figure out how to call the
        JavaScript function <code>getFlag</code> from your browser?
    </p>
  </div>
  <script src="script.js"></script>
</body>

</html>
    """

def get_js(flag: str) -> str:
    encoded_flag = base64.b64encode(flag.encode()).decode("utf-8")[::-1]
    return """
// This is the flag after being encoded.

const encodedFlag = "%s";

// Can you run this function from your browser to get the flag?

function getFlag() {
    const reversedFlag = encodedFlag.split("").reverse().join("");
    return atob(reversedFlag);
}

    """ % encoded_flag

def main():
    flag = get_flag_from('hidden_js.yml')
    with open('page2.html', 'w') as f:
        f.write(get_page())
    with open('script.js', 'w') as f:
        f.write(get_js(flag))

if __name__ == "__main__":
    main()

