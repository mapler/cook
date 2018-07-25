$(document).ready(function() {
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    var currentIdx = 0;
    var rid = $('#procedure').data('rid');
    var step = $('#procedure').data('step');
    var actions = $('.actions');
    var actionNum = actions.length;
    enableNextBtn();
    socket.on('timer', function(timer) {
      $('#timer').text(timer);
      console.log(timer);
      if (timer == 0) {
         enableNextBtn();
      } else {
        if (currentIdx != actionNum) {
          enableNextBtn();
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
      console.log(actions[currentIdx]);
      if (actions[currentIdx] != null) {
        var action = actions[currentIdx];
        var timer = $("#" + action.id).data("timer");
        console.log(timer);
        if (timer != "") {
          if ($("#timer-block-" + action.id).hasClass("d-none")) {
            console.log("show timer #timer-block-" + action.id);
            $("#timer-block-" + action.id).removeClass("d-none");
            $("#timer").text($('#' + action.id).data('timer'));
            speech($("#" + action.id).find('.action-desc').text());
            enableNextBtn();
          } else {
            console.log("start timer #timer-block-" + action.id);
            $("#timer").text($('#' + action.id).data('timer'));
            $.post("/timer", {"timer": timer});
            currentIdx ++;
          }
        } else {
          speech($("#" + action.id).find('.action-desc').text());
          enableNextBtn();
          currentIdx ++;
        }
      } else if (currentIdx == actionNum) {
        window.location.href = "/recipe/" + rid + "/procedures/" + (step + 1);
      }
    });
    socket.on('reset-btn', function() {
      console.log('reset-btn is pushed ' + currentIdx);
    });
    $('#next-btn').click(function (event){
      $.post("/next");
    });
    $('#reset-btn').click(function (event){
      $.post("/reset");
    });
});

