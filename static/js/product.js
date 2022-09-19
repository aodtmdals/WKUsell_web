function create_product() {
  let productname = $("#input-p-name").val();
  let price = $("#input-p-price").val();
  let category = $("#input-p-category").val();
  let club = $("#check-club").is(":checked");
  let tags = $("#p-tags").val();

  console.log(productname, price, category, club);

  // // {# help-id가 is-danger 클래스 갖고 있으면 중복검사 통과 못한거니까 아이디 다시 확인해라#}
  // if ($("#p-name").hasClass("is-danger")) {
  //   alert("제품 이름을 다시 확인해주세요.");
  //   return;
  //   //   {# help-id가 is-success 클래스 갖고 있지 않으면 중복검사 해라#}
  // } else if (!$("#p-price").hasClass("is-danger")) {
  //   alert("제품 가격은 숫자만 입력 가능합니다.");
  //   return;
  // }
  // if (!is_productname(productname) || productname == "") {
  //   $("#p-name").addClass("is-danger").focus();
  //   return;
  // } else {
  //   $("#p-name").removeClass("is-danger").addClass("is-success");
  // }
  // if (!is_price(price) || price == "") {
  //   $("#p-price").addClass("is-danger").focus();
  //   return;
  // } else {
  //   $("#p-price").removeClass("is-danger").addClass("is-success");
  // }

  const formData = new FormData();
  formData.append("productname", productname);
  formData.append("price", price);
  formData.append("category", category);
  formData.append("club", club);
  formData.append("tags", tags);
  formData.append("tImage", $("#t-image")[0].files[0]);
  formData.append("pImage", $("#p-image")[0].files[0]);

  $.ajax({
    type: "POST",
    url: "/create/request",
    contentType: false,
    processData: false,
    data: formData,
    success: function (response) {
      alert("상품 등록 완료");
      window.location.replace("/");
    },
  });
}

// 정규식
function is_productname(asValue) {
  var regExp = /^[가-힣ㄱ-ㅎa-zA-Z0-9._-]{2,}$/;
  return regExp.test(asValue);
}

function is_price(asValue) {
  var regExp = /^[0-9]{2,}$/;
  return regExp.test(asValue);
}
