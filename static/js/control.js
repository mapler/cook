function enableNextBtn() {
  $('#next-btn').removeClass("btn-secondary");
  $('#next-btn').prop("disabled", false);
  $('#next-btn').addClass("btn-primary");
};

function disableNextBtn() {
  $('#next-btn').removeClass("btn-primary");
  $('#next-btn').prop("disabled", true);
  $('#next-btn').addClass("btn-secondary");
};
