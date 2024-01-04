---
auth_required: false
draft: false
hidden: false
route: index
title: NKCyber Square Practice CTF
---

<div class="row">
    <div class="col-md-6 offset-md-3">
        <img class="w-100 mx-auto d-block" style="max-width: 50%;padding: 50px;padding-top: 14vh;"
            src="/files/698a2200546c2918499e1f99fb3b5446/nkcyber.png" />
        <h3 class="text-center">
            NKCyber Square Practice CTF
        </h3>
        <div style="text-align: center;">
            <small>
                From
                <time id="start-time">Start</time> to
                <time id="end-time">End</time>.
            </small>
        </div>
      	<div>
          <h2>Rules</h2>
          <ol>
            <li>You <strong>ARE</strong> allowed to use the internet to research topics.</li>
            <li>You <strong>MUST</strong> have fun. :]</li>
          </ol>
      	</div>
        <br>
        <div class="text-center">
          <b><a href="/socials">Follow us on Social Media!</a></b>
        </div>
        <br>
        <h4 class="text-center">
            <a href="register">Click here</a> to create your account.
        </h4>
    </div>
    <script>
        function isDateValid(dateStr) {
            return !isNaN(new Date(dateStr));
        }
        const start = document.getElementById('start-time');
        const end = document.getElementById('end-time');
        const startDate = new Date("{{ ctf_start }}");
        const endDate = new Date("{{ ctf_freeze }}");
        if (isDateValid(startDate)) {
            start.textContent = startDate.toLocaleTimeString()
        }
        if (isDateValid(endDate)) {
            end.textContent = endDate.toLocaleTimeString()
        }
    </script>
</div>