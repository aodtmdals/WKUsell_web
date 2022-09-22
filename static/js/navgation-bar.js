function is_select(self) {
  //클릭한 요소가 몇 번째 요소인지 알아내기
  let itemsID = $(".navbar-nav>li>a").index(self);
  const maxchild = document.querySelector(".navbar-nav").childElementCount;

  for(let i = 0; i <= maxchild; i++){
    if(i == itemsID){
      //만일 i가 선택된 id와 같을 때
      //active class를 추가하고
      $('.navbar-nav>li:nth-child('+ (i+1) +')>a').addClass("active");
      //아니면 삭제한다
    } else{
      $('.navbar-nav>li:nth-child('+ (i+1) +')>a').removeClass("active");
    }
  }
  console.log(itemsID)

  $.ajax({
    url: "/list",
    data: {categori: itemsID},
    method: "GET",
    success: function(response){
    }
  })
}
