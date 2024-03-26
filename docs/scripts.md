We use some other scripts for CTFd

On <https://ctf.nkcyber.org/admin/config>

We use:

```html
<script>
if(window.location.pathname == "/scoreboard") 
{	var containers=document.querySelectorAll('div.jumbotron');  //<---- Define Tag to replace w/ clock
    containers.forEach(function(container)
    {  replaceContentWithTimestamp(container);
    });
    setTimeout(function(){location.reload();},30000);  //<---- Define refresh rate in milliseconds


    function formatTime()
    {  var date=new Date();
        var hours=addZero(date.getHours());
        var minutes=addZero(date.getMinutes());
        var seconds=addZero(date.getSeconds());
        return '<div class="container"><h1 style="font-size: 80pt;">'+hours+':'+minutes+':'+seconds+'</h1></div>';
    }
    function addZero(value)
    {  return value < 10 ? '0' + value : value;
    }

    function replaceContentWithTimestamp(element)
    {  element.innerHTML=formatTime();
    }
}
</script>


<script type="module">
   if (window.location.pathname == "/register") {
     // set real name and email descriptions
     document.querySelector('label.form-label[for="name"]').textContent = "Real First and Last Name";
     document.querySelector('label.form-label[for="email"]').textContent = "Real Email";
     document.querySelector('input[name="password"] + small.form-text.text-muted').textContent = "Used to sign in to your account. Don't forget it!";
     
     // set School input
      let div = document.createElement("div");
      div.setAttribute("class", "mb-3");

      let b = document.createElement("b");

      let label = document.createElement("label");
      label.setAttribute("for", "affiliation");
      label.textContent = "Real School Name";

      let input = document.createElement("input");
      const select_Attr = {
         class: "form-control custom-select",
         id: "affiliation",
         name: "affiliation",
         required: "required",
         type: "text",
         value: "",
      };

      (function () {
         Object.keys(select_Attr).forEach((attr) => {
            input.setAttribute(attr, select_Attr[attr]);
         });
      })();

      let small = document.createElement("small");
      small.setAttribute("class", "form-text text-muted");
      small.textContent = "What school do you go to? (Please use the full name)";

      b.appendChild(label);
      div.appendChild(b);
      div.appendChild(input);
      div.appendChild(small);

      document.querySelector("form").children[3].insertAdjacentElement("afterEnd", div);
   }
</script>
```
