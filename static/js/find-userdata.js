function find_id() {
    let radioValue = $("[name=certification]:checked").val();
    let phone = $("#input-phone").val();
    let email = $("#input-email").val();
    let emailUrl = $("#input-email-url").val();
    let findBtn = $("#find-btn");
    let insertdata = $("#insert_userdata");
    let input_data = $("#data").innerHTML();
    let find_phone = $("#find-phone-box");
    let find_email = $("#find-email-box");
  
    if(radioValue == "phone"){
      find_phone.removeClass("invisible");
      find_email.addClass("invisible");
      result = phone;
    } else {
      find_phone.addClass("invisible");
      find_email.removeClass("invisible");
      result = email + "@" + emailUrl;
    }

    $.ajax({
      type: "POST",
      url: "/join-in/find/id/request",
      data: {
        value: radioValue,
        result: result
      },

      success: function (response) {
        findBtn.addClass("invisible");
        insertdata.removeClass("invisible");
        input_data = `찾은 아이디는 "${response}"입니다.`;
      },
    });
  }
  
  function check_id() {
    let findBtn = $("#find-btn");
    let insertid = $("#find-pw-form");
    let insertpw = $("find-userdata");
    let id = $("#id");
  

    $.ajax({
      type: "POST",
      url: "/join-in/find/pw/check",
      data: {
        result: result,
      },

      success: function (response) {
        insertid.addClass("invisible");
        insertpw.removeClass("invisible");
      },
    });
  }
  
  function find_pw(){
    let printurl = $("#insert_userdata");
    let password = $("#input-password").val();
    let password2 = $("#input-password2").val();
    
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
      url: "/join-in/find/pw/request",
      data: {
        result: result,
      },

      success: function (response) {
        insertid.addClass("invisible");
        insertpw.removeClass("invisible");
      },
    });
  }
  

  // 정규식
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
  