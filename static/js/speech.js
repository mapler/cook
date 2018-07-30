function speech(text) {
    $.post("/speech", {"content": text});
    console.log("said: " + text);
};


function stopSpeech() {
    $.post("/speech", {"content": ':STOP:'});
    console.log("stop speech");
};
