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
  let ischecked = document.querySelector("#chk_id").checked;

  if (window.localStorage.key("savedID") != null) {
    $("input[name=join-id]").attr(
      "value",
      window.localStorage.getItem("savedID")
    );
    $("input[name=save_ids]").attr("checked", true);
  } else {
    userID = "";
    ischecked = false;
  }
}

getSavedId();
