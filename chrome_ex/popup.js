document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('modifyButton').addEventListener('click', () => {
        // alert("pupup worked");
    
        chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
            // alert("tabs, " + tabs[0].id + "!");
            chrome.scripting.executeScript({
                target: { tabId: tabs[0].id },
                function: modifyPage,
                args: [document.getElementById("modifyButton").value]   // 関数に渡すパラメータ
            });
        });
    });

    document.getElementById('modifyButton_1').addEventListener('click', () => {
        // alert("pupup worked");
    
        chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
            // alert("tabs, " + tabs[0].id + "!");
            chrome.scripting.executeScript({
                target: { tabId: tabs[0].id },
                function: modifyPage,
                args: [document.getElementById("modifyButton_1").value]   // 関数に渡すパラメータ
            });
        });
    });

    document.getElementById('modifyButton_color').addEventListener('click', () => {
        chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
            chrome.scripting.executeScript({
                target: { tabId: tabs[0].id },
                function: modifyBackColor
            });
        });
    });
});
  
  
  function modifyPage(i_url) {
    // 在這裡編寫修改網頁信息的程式碼
    //var imageUrl = 'images/berries-8577873_640.jpg';//document.getElementById('imageURL').value;
    document.body.style.backgroundImage = 'url("images/' + i_url + '")';
  }

  function modifyBackColor() {
    // Change background color to red
    document.body.style.backgroundColor = "red"; // 背景色を赤に変更する
  }
  