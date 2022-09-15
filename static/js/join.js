const pwText = document.querySelector(".pw-text");
const idText = document.querySelector(".id-text");
const nickText = document.querySelector(".nick-text");
const emailText = document.querySelector(".email-text");
const phoneText = document.querySelector(".phone-text");
const joinBtn = document.getElementById("join");

function passwordCheck() {
  const pw = document.getElementById("password").value;
  const pwCheck = document.getElementById("password-check").value;

  if (pw.length < 8 || pw.length > 16) {
    pwText.innerHTML = "비밀번호는 8글자 이상, 16글자 이하만 가능합니다.";
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

function innerTextCheck() {
  const id = document.getElementById("id").value;
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

function check_id() {
  let username = $("#input-username").val();
  if (username == "") {
    $("#help-id")
      .text("아이디를 입력해주세요.")
      .removeClass("is-safe")
      .addClass("is-danger");
    $("#input-username").focus();
    return;
  }
  if (!is_username(username)) {
    $("#help-id")
      .text(
        "아이디의 형식을 확인해주세요. 영문과 숫자, 일부 특수문자(._-) 사용 가능. 2-10자 길이"
      )
      .removeClass("is-safe")
      .addClass("is-danger");
    $("#input-username").focus();
    return;
  }
  $("#help-id").addClass("is-loading");
  $.ajax({
    type: "POST",
    url: "/join/id-overlap",
    data: {
      id: username,
    },
    success: function (response) {
      if (response["exists"]) {
        $("#help-id")
          .text("이미 존재하는 아이디입니다.")
          .removeClass("is-safe")
          .addClass("is-danger");
        $("#input-username").focus();
      } else {
        $("#help-id")
          .text("사용할 수 있는 아이디입니다.")
          .removeClass("is-danger")
          .addClass("is-success");
      }
      $("#help-id").removeClass("is-loading");
    },
  });
}
