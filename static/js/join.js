

function sign_up() {
  let username = $("#input-username").val();
  let nickname = $("#input-nickname").val();
  let password = $("#input-password").val();
  let password2 = $("#input-password2").val();
  let phone = $("#input-phone").val();
  let email = $("#input-email").val();
  let emailUrl = $("#input-email-url").val();

  console.log(username, password, password2);

  // {# help-id가 is-danger 클래스 갖고 있으면 중복검사 통과 못한거니까 아이디 다시 확인해라#}
  if ($("#help-id").hasClass("is-danger")) {
    alert("아이디를 다시 확인해주세요.");
    return;
    //   {# help-id가 is-success 클래스 갖고 있지 않으면 중복검사 해라#}
  } else if (!$("#help-id").hasClass("is-success")) {
    alert("아이디 중복확인을 해주세요.");
    return;
  } else if ($("#help-password").hasClass("is-danger")) {
    alert("비밀번호를 다시 확인해주세요.");
    return;
  } else if ($("#help-nickname").hasClass("is-danger")) {
    alert("닉네임을 다시 확인해주세요.");
    return;
  }
  if (nickname == "") {
    $("#help-nickname")
      .text("닉네임을 입력해주세요.")
      .removeClass("is-safe")
      .addClass("is-danger");
    $("#input-nickname").focus();
    return;
  } else if (!is_nickname(nickname)) {
    $("#help-nickname")
      .text(
        "닉네임의 형식을 확인해주세요. 한글, 영문, 숫자 사용 가능하며 2자 이상"
      )
      .removeClass("is-safe")
      .addClass("is-danger");
    $("#input-nickname").focus();
    return;
  } else {
    $("#help-nickname").removeClass("is-danger").addClass("is-success");
  }
  if (password == "") {
    $("#help-password")
      .text("비밀번호를 입력해주세요.")
      .removeClass("is-safe")
      .addClass("is-danger");
    $("#input-password").focus();
    return;
  } else if (!is_password(password)) {
    $("#help-password")
      .text(
        "비밀번호의 형식을 확인해주세요. 영문과 숫자 필수 포함, 특수문자(!@#$%^&*) 사용가능 8-20자"
      )
      .removeClass("is-safe")
      .addClass("is-danger");
    $("#input-password").focus();
    return;
  } else {
    $("#help-password")
      .text("사용할 수 있는 비밀번호입니다.")
      .removeClass("is-danger")
      .addClass("is-success");
  }
  if (password2 == "") {
    $("#help-password2")
      .text("비밀번호를 입력해주세요.")
      .removeClass("is-safe")
      .addClass("is-danger");
    $("#input-password2").focus();
    return;
  } else if (password2 != password) {
    $("#help-password2")
      .text("비밀번호가 일치하지 않습니다.")
      .removeClass("is-safe")
      .addClass("is-danger");
    $("#input-password2").focus();
    return;
  } else {
    $("#help-password2")
      .text("비밀번호가 일치합니다.")
      .removeClass("is-danger")
      .addClass("is-success");
  }
  if (!is_phone(phone)) {
    $("#help-phone")
      .text("숫자만 입력해주세요")
      .removeClass("is-safe")
      .addClass("is-danger");
    $("#input-phone").focus();
    return;
  } else {
    $("#help-phone").removeClass("is-danger").addClass("is-success");
  }

  $.ajax({
    type: "POST",
    url: "/join/request",
    data: {
      id: username,
      pw: password,
      nickname: nickname,
      phone: phone,
      email: email + "@" + emailUrl,
    },
    success: function (response) {
      alert("회원가입을 축하드립니다!");
      window.location.replace("/");
    },
  });
}

function sign_revise() {
  let nickname = $("#input-nickname").val();
  let password = $("#input-password").val();
  let password2 = $("#input-password2").val();
  let phone = $("#input-phone").val();

   if ($("#help-password").hasClass("is-danger")) {
    alert("비밀번호를 다시 확인해주세요.");
    return;
  } else if ($("#help-nickname").hasClass("is-danger")) {
    alert("닉네임을 다시 확인해주세요.");
    return;
  }

  if (password == "") {
    $("#help-password")
      .text("비밀번호를 입력해주세요.")
      .removeClass("is-safe")
      .addClass("is-danger");
    $("#input-password").focus();
    return;
  } else if (!is_password(password)) {
    $("#help-password")
      .text(
        "비밀번호의 형식을 확인해주세요. 영문과 숫자 필수 포함, 특수문자(!@#$%^&*) 사용가능 8-20자"
      )
      .removeClass("is-safe")
      .addClass("is-danger");
    $("#input-password").focus();
    return;
  } else {
    $("#help-password")
      .text("사용할 수 있는 비밀번호입니다.")
      .removeClass("is-danger")
      .addClass("is-success");
  }
  if (password2 == "") {
    $("#help-password2")
      .text("비밀번호를 입력해주세요.")
      .removeClass("is-safe")
      .addClass("is-danger");
    $("#input-password2").focus();
    return;
  } else if (password2 != password) {
    $("#help-password2")
      .text("비밀번호가 일치하지 않습니다.")
      .removeClass("is-safe")
      .addClass("is-danger");
    $("#input-password2").focus();
    return;
  } else {
    $("#help-password2")
      .text("비밀번호가 일치합니다.")
      .removeClass("is-danger")
      .addClass("is-success");
  }

  $.ajax({
    type: "POST",
    url: "/user/revise/request",
    data: {
      pw: password,
      nickname: nickname,
    },
    success: function (response) {
      alert("회원정보 수정 완료!");
      window.location.replace("/");
    },
  });
}

// 회원정보 수정시 ID 값 변경 X
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
        "아이디의 형식을 확인해주세요. 영문과 숫자, 일부 특수문자(._-) 사용 가능. 2-15자 길이"
      )
      .removeClass("is-safe")
      .addClass("is-danger");
    $("#input-username").focus();
    return;
  }
  $("#help-id").addClass("is-loading");
  $.ajax({
    type: "POST",
    url: "/join/checkDup",
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

// 정규식
function is_username(asValue) {
  //  {# 괄호 ( )안의 요소는 필수 포함 요소임. a-zA-Z 소문자 a-z, 대문자 A-Z 포함! 대괄호는 선택포함을 의미함. 숫자 0-9사용가능!. 2-20 한다!#}
  var regExp = /^(?=.*[a-zA-Z])[-a-zA-Z0-9_.]{2,20}$/;
  return regExp.test(asValue);
}

function is_nickname(asValue) {
  var regExp = /^[가-힣ㄱ-ㅎa-zA-Z0-9._-]{2,}$/;
  return regExp.test(asValue);
}
function is_password(asValue) {
  //  {# *\d = 숫자 무조건 포함해라#}
  var regExp = /^(?=.*\d)(?=.*[a-zA-Z])[0-9a-zA-Z!@#$%^&*]{8,20}$/;
  return regExp.test(asValue);
}
function is_phone(asValue) {
  //  {# *\d = 숫자 무조건 포함해라#}
  var regExp = /^[0-9]+$/;
  return regExp.test(asValue);
}

disableID();
