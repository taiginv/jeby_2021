$(document).ready(function () {
  // 네비게이션바에서 해당 메뉴를 활성화한다.
  $(".nav-link").eq(0).addClass("active");

  // 검색창에 키워드가 없으면 검색창 위치를 중간으로 변경한다.
  if ($("#input-keyword").val() == "") {
    $("#search-box").addClass("d-flex align-items-center h-50");
    $("#search-box").children().addClass("w-100");
  }

  // 화면 오픈 시 검색창에 커서를 이동시킨다.
  // 커서를 검색어 마지막에 위치시킨다.
  _keyword = $("#input-keyword").val();
  $("#input-keyword").focus();
  $("#input-keyword").val("").val(_keyword);

  // 검색버튼을 선택하면 검색을 수행한다.
  $("#search-img").click(function () {
    $("#frm-search").submit();
  });
});
