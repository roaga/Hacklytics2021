mergeInto(LibraryManager.library, {

    ReadData: function () {
        const firebaseConfig = {
            apiKey: "AIzaSyAo4gZZE5tc9g-do0RAXIjTAvwv-54YoA0",
            authDomain: "hacklytics-2021-626b7.firebaseapp.com",
            projectId: "hacklytics-2021-626b7",
            storageBucket: "hacklytics-2021-626b7.appspot.com",
            messagingSenderId: "1024219270230",
            appId: "1:1024219270230:web:102279cff4ccdc45effff7"
        };
        
        var returnStr = "bla";
        var bufferSize = lengthBytesUTF8(returnStr) + 1;
        var buffer = _malloc(bufferSize);
        stringToUTF8(returnStr, buffer, bufferSize);
        return buffer;
    },

});