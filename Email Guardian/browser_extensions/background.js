

//






function extractURLsFromHtml(rawHTML){

  var anchors = /<a\s[^>]*?href=(["']?)([^\s]+?)\1[^>]*?>/ig;
  var links = [];
  rawHTML.replace(anchors, function (_anchor, _quote, url) {
    links.push(url);
  });
  
  console.log(links);
  return links
  }

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    console.log("mesage recived to background.js  = "+ message);
    //
    if(message.msg === 'test'){
      const getData = async ()  =>{
      const query = await fetch("https://www.boredapi.com/api/activity")   // exemeple https://jsonplaceholder.typicode.com/users

      const response =  await query.json(); console.log("response = " + response)
      const json = await response; console.log("json = " + JSON.stringify(json))}

      try {
        console.log("getting data")
        getData();
      } catch (error) {
        console.log("errorr "+error)
      }
    }

    if(message.msg === "check"){
      
      mail = message.mail
      url = extractURLsFromHtml(mail)
      console.log("got : "+url)
      const res = checkPhishing(url[0])
      sendResponse({'result': res})
      
    }
      
});

async function checkPhishing(url){
  const myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/json");

  const reqOption = {
    method: "POST",
    headers: myHeaders,
    body: JSON.stringify({'url': url}),
  };


  const query = await fetch("http://localhost:5002/phishing_detection",reqOption)




  const response = await query.json()
  console.log("response = "+ response.result)
  return response.result
}





chrome.tabs.onUpdated.addListener(function
  (tabId, changeInfo, tab) {
    // read changeInfo data and do something with it (like read the url)
    if (changeInfo.status) {
      console.log("The URL has changed");
      console.log("status = "+changeInfo.status)
    }
    if(changeInfo.status == 'complete'){
      console.log('true')
      //extractButton(null)

      setTimeout( ()=>
        chrome.tabs.sendMessage( tabId, {
          msg: 'urlchange',
          status: changeInfo.status
        })
      ,1000);

    }
  }
);


chrome.tabs.query({ active: true, currentWindow: true }, function(tabs){
  console.log(tabs)
  tabs.forEach(element => { console.log(element)})
});







