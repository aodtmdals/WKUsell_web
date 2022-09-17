const pwText = document.querySelector(".pw-text");
const idText = document.querySelector(".id-text");
const nickText = document.querySelector(".nick-text");
const emailText = document.querySelector(".email-text");
const phoneText = document.querySelector(".phone-text");
const joinBtn = document.getElementById("join");

//회원가입 시 페스워드 중복검사 +
function passwordCheck() {
  const pw = document.getElementById("password").value;
  const pwCheck = document.getElementById("password-check").value;

  if (pw.length < 8 || pw.length > 20) {
    pwText.innerHTML =
      "비밀번호는 8~20글자, 특수문자가 하나 이상 들어가야합니다.";
    pwText.style.color = "red";
  } else if (pw != "" && pwCheck != "") {
    if (pw == pwCheck) {
      pwText.innerHTML = "비밀번호가 일치합니다.";
      pwText.style.color = "blue";
    } else {
      pwText.innerHTML = "비밀번호가 일치하지 않습니다.";
      pwText.style.color = "red";
    }
  } else {
    pwText.innerHTML = "";
  }
}

//아이디와 닉네임 값이 들어왔는지 체크
function innerTextCheck() {
  const id = document.getElementById("input-username").value;
  const nickname = document.getElementById("nickname").value;

  if (id == " ") {
    idText.innerHTML = "아이디를 입력하세요";
    idText.style.color = "red";
  } else if (id.length < 5) {
    pwText.innerHTML = "아이디는 5글자 이상만 가능합니다.";
    pwText.style.color = "red";
  } else {
    idText.innerHTML = "";
  }
  if (nickname == " ") {
    nickText.innerHTML = "닉네임을 입력하세요";
    nickText.style.color = "red";
  } else if (nickname.length < 3) {
    nickText.innerHTML = "닉네임은 3글자 이상만 가능합니다.";
    nickText.style.color = "red";
  } else {
    nickText.innerHTML = "";
  }
}

function disableID() {
  if (window.localStorage.key("savedID") != null) {
    $("input[name=revise-id]").attr(
      "value",
      window.localStorage.getItem("savedID")
    );
  }
}

// 아이디 중복 검사
function check_dup() {
  let username = $("#input-username").val();
  $(".id-text").addClass("is-loading");
  $.ajax({
    type: "POST",
    url: "/join/checkDup",
    data: {
      id: username,
    },
    success: function (response) {
      if (response["exists"]) {
        $(".id-text")
          .text("이미 존재하는 아이디입니다.")
          .removeClass("is-safe")
          .addClass("is-danger");
        $("#input-username").focus();
      } else {
        $(".id-text")
          .text("사용할 수 있는 아이디입니다.")
          .removeClass("is-danger")
          .addClass("is-success");
      }
      $(".id-text").removeClass("is-loading");
    },
  });
}

disableID();
