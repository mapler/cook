$(document).ready(function() {
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    var riElements = $('.ri-element');
    var riElementNum = riElements.length;
    var currentIdx = 0
    var lastIdx = -1
    var weightStableCount = 0
    socket.on('weight', function(weight) {
      $('#weight').text(weight);
      var targetWeight = $('#target-weight').text();
      console.log(targetWeight);
      if (!isNaN(parseInt(targetWeight))) {
        if (Math.abs(weight - targetWeight) <= 10) {
            weightStableCount ++;
            if (weightStableCount > 5) {
               enableNextBtn();
            }
          } else {
               disableNextBtn();
          };
      };
    });
    socket.on('next-btn', function() {
      console.log('next-btn is pushed ' + currentIdx);
      // stop unfinished speech
      stopSpeech();
      // reset weight stable counter
      weightStableCount = 0;
      if (riElements[currentIdx] != null) {
        // remove last element highlight
        if (riElements[lastIdx] != null) {
          $("#" + riElements[lastIdx].id).removeClass("bg-primary");
        }
        // speech ingredient
        var element = $("#" + riElements[currentIdx].id);
        if (element.data("weight") != "") {
          speech(element.data("name") + element.data("weight") + "グラムを用意してください");
          $('#weight-slash').text("/");
          $('#target-weight').text(element.data("weight"));
          disableNextBtn();
        } else {
          speech(element.data("name") + "を用意してください");
          $('#weight-slash').text("");
          $('#target-weight').text("");
        }
        // hide description image if first
        $("#ingredient-desc").hide();
        // show current element hightlight and weight
        $("#" + riElements[currentIdx].id).addClass("bg-primary");
        $("#ingredient-weight").removeClass("d-none");
        // update cursor index
        lastIdx = currentIdx;
        currentIdx ++;
      } else if (currentIdx == riElementNum) {
        window.location.href = "/recipe/1/procedures/1";
      }
    });
    socket.on('reset-btn', function() {
      console.log('reset-btn is pushed ' + currentIdx);
    });
    speech("材料の用意");
    enableNextBtn();
    $('#next-btn').click(function (event){
      $.post("/next");
    });
    $('#reset-btn').click(function (event){
      $.post("/reset");
    });
});

