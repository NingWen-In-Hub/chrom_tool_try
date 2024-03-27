chrome.action.onClicked.addListener((tab) => {
    alert("background worked");
    chrome.scripting.executeScript({
      target: { tabId: tab.id },
      function: modifyPage
    });
  });
  
  function modifyPage() {
    // 在這裡編寫修改網頁信息的程式碼
    alert("background modifyPage worked");

    var imageUrl = 'images/berries-8577873_640.jpg';//document.getElementById('imageURL').value;
    document.body.style.backgroundImage = 'url("' + imageUrl + '")';
  }
  