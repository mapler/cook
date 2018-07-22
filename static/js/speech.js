function speech(text) {
    var ssu = new SpeechSynthesisUtterance();
    ssu.text = text;
    ssu.lang = 'ja-JP';
    speechSynthesis.speak(ssu);
    console.log("Said: " + text);
};
