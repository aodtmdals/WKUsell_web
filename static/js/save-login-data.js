function saveID() {
  const userID = document.querySelector(".user-id").value;
  const ischecked = document.querySelector("#chk_id").checked;

  if (ischecked == true) {
    window.localStorage.setItem("savedID", `${userID}`);
  } else {
    window.localStorage.removeItem("savedID");
  }
}

function getSavedId() {

  if (window.localStorage.key("savedID") != null) {
    $("input[name=join-id]").attr(
      "value",
      window.localStorage.getItem("savedID")
    );
    $("input[name=save_ids]").attr("checked", true);
  }
}

//카카오 API 사용 어려워서 우선 주석처리
/*
function kakaoLogin() {
  window.Kakao.Auth.login({
    scope: "profile_nickname, account_email", //동의항목 페이지에 있는 개인정보 보호 테이블의 활성화된 ID값을 넣습니다.
    success: function (response) {
      console.log(response); // 로그인 성공하면 받아오는 데이터
      window.Kakao.API.request({
        // 사용자 정보 가져오기
        url: "/v2/user/me",
        success: (res) => {
          kakao_account = res.kakao_account;
          $.ajax({
            type: "POST",
            url: "/join-in/kakao",
            data: {
              id: kakao_account.email,
              nickname: kakao_account.profile.nickname,
            },
            success: function (response) {
              window.location.replace("/");
            },
          });
        },
      });
      // window.location.href='/ex/kakao_login.html' //리다이렉트 되는 코드
    },
    fail: function (error) {
      console.log(error);
    },
  });
}
*/
getSavedId();
