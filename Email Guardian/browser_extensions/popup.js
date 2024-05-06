// Copyright 2017 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.
'use strict';

//get current open tab URL
function getCurrentTabUrl(callback) {
  chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
    var tab = tabs[0];
    var url = tab.url;
    callback(url);
  });
}
//edit result text
function editResult(str){
  const resDiv = document.getElementById('res');
  resDiv.innerText =  str;
  

}

function editResult_with_url(){
  const resDiv = document.getElementById('res');
  getCurrentTabUrl(function(url) {
    resDiv.innerText = url;
    console.log("Current tab URL:", url);
  })
}

function sendMessageToExtension(msg){
  chrome.tabs.query({ active: true, currentWindow: true }, function(tabs){
    const tab = tabs[0];
    console.log(tab);
    chrome.tabs.sendMessage(tab.id, msg)} //{ msg: "giveme"}
)
}

//onclick function
function click_function(event) {
  const button = event.target;
  editResult();
}
function click2_function(event){
  console.log("click2")
    chrome.tabs.query({ active: true, currentWindow: true }, function(tabs){
        const tab = tabs[0];
        console.log(tab);
        chrome.tabs.sendMessage(tab.id, { msg: "giveme"})}
    )

}

function click3_function(){
  console.log("click3")
  chrome.tabs.query({ active: true, currentWindow: true }, function(tabs){
    const tab = tabs[0];
    //console.log(tab);
    chrome.tabs.sendMessage(tab.id, { msg: "button3"}, function(response) {
      console.log("Response from background script:", response.response);
      console.log("Got it");
      let ret = String(response.response)
      if (response) {
        console.log("response success")
        console.log(document.getElementById('res'))
        editResult(ret)
      } else {
        console.error("Failed to edit result:", response && response.response);
      }

      }
    )}
  )
}

function extractButton(event){
  console.log("click Extract")

  chrome.tabs.query({ active: true, currentWindow: true }, function(tabs){
    const tab = tabs[0];
    //console.log(tab);
    chrome.tabs.sendMessage(tab.id, { msg: "extract"}, function(response) {
      console.log("Response from content script:", response);
      console.log("Got it");
      //console.log(extractURLsFromHtml(response.body))


      if (response) {
        //edit popup.js
        document.getElementsByClassName("email-sender")[0].innerText = response.sender
        document.getElementsByClassName("email-subject")[0].innerText = response.subject
        document.getElementsByClassName("email-body")[0].innerHTML = response.body
        let emailbody =response.body
        let url = extractURLsFromHtml(emailbody)
        let emailsubject = response.subject
        if(event == null) return

        // Phishing check section
        let phshing_text = document.getElementsByClassName("server-result")[0].querySelector(".p") 

        phshing_text.innerText = ""
        phshing_text.classList.remove("danger_text","safe_text")
        phshing_text.classList.add("loader")
        let chk  = checkPhishing(url[0]).then((response)=>{
          phshing_text.classList.remove("loader")
          if(response==="phishing") phshing_text.classList.add("danger_text")
          else phshing_text.classList.add("safe_text")
          phshing_text.innerText = response + "probably" 
        }).catch((e)=>{phshing_text.innerText="error"})
               

        // Spam detection section
        let spam_text = document.getElementsByClassName("server-result")[0].querySelector(".s") 

        spam_text.innerText = ""
        spam_text.classList.remove("danger_text","safe_text")
        spam_text.classList.add("loader")
        let chk2  = checkSpam(emailsubject).then((response)=>{
          spam_text.classList.remove("loader")
          if(response.startsWith("s")) spam_text.classList.add("danger_text")
          else spam_text.classList.add("safe_text")
          spam_text.innerText = response 
        }).catch((e)=>{
          console.log("error in spam detection : " +e)
          spam_text.innerText="error"})

        // Malware detection
        let mw_text = document.getElementsByClassName("server-result")[0].querySelector(".m") 
        let selectedfile = document.getElementById("fileUpload").files[0]

        const formData = new FormData()
        formData.append('file', selectedfile)

        mw_text.innerText = ""
        mw_text.classList.remove("danger_text","safe_text")
        mw_text.classList.add("loader")

        let ch3 = fetch('http://localhost:5001/malware_detection', {
          method: 'POST',
          body: formData
      })
      .then(response => {
          if (!response.ok) {
            console.log("response not ok")
            mw_text.classList.remove("loader")
              throw new Error('Network Error');
          }
          return response.json();
      })
      .then(data => {
          let res = data.result
          console.log('File uploaded successfully:', res);
          
          if(res.startsWith("m")) mw_text.classList.add("danger_text")
          else mw_text.classList.add("safe_text")
          mw_text.classList.remove("loader")
          mw_text.innerText = res
      })
      .catch(error => {
          console.log('There was a problem with the upload:', error);
          mw_text.innerText = "unknown"
          mw_text.classList.remove("loader")
      });

      
  
      } else {
        console.error('Failed to edit result, No response from content script' );
      }

      }
    )}
  )

}

async function checkPhishing(url){
  const myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/json");

  const reqOption = {
    method: "POST",
    headers: myHeaders,
    body: JSON.stringify({'url': url}),
  };

try{
  const query = await fetch("http://localhost:5002/phishing_detection",reqOption)


  const response = await query.json()
  console.log("response = "+ response.result)
  return response.result
}
catch(e){
  return "error"
}
}

async function checkSpam(content){
  const myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/json");

  const reqOption = {
    method: "POST",
    headers: myHeaders,
    body: JSON.stringify({'content': content}),
  };

try{
  const query = await fetch("http://localhost:5000/email_spam",reqOption)


  const response = await query.json()
  console.log("response = "+ response.result)
  return response.result
}
catch(e){
  return "error"
}
}



function fetchIsPhishing(data){
  const myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/json");

  const reqOption = {
    method: "POST",
    headers: myHeaders,
    body: JSON.stringify({'data': data}),
  };


  document.getElementsByClassName("email-body")[0].innerHTML = "<div class=\"loader\"></div>"
  //fetching
  const rep = fetch("http://localhost:5000/api/data",reqOption).then((reponse)=>{
    let ret = reponse.json()

    document.getElementsByClassName("email-body")[0].innerHTML = "<h3>Result from server : "+ ret.message+"</h3>"
    return ret

  }).then((result)=>{
    console.log(JSON.stringify(result));
    console.log(result)
    if(result.error) document.getElementsByClassName("email-body")[0].innerHTML = "<h3>Result from server : "+ result.error+"</h3>"
    else document.getElementsByClassName("email-body")[0].innerHTML = "<h3>Result from server : "+ result.message+"</h3>"
    return result
  }).catch((e)=>{
    document.getElementsByClassName("email-body")[0].innerHTML = "<h3>Result from server : "+ result.error+"</h3>"
    console.log("error : " + e)
  })

}

function extractURLsFromHtml(rawHTML){

var anchors = /<a\s[^>]*?href=(["']?)([^\s]+?)\1[^>]*?>/ig;
var links = [];
rawHTML.replace(anchors, function (_anchor, _quote, url) {
  links.push(url);
});

console.log(links);
return links
}

function chromeOnTabUpdatedListener (tabId, changeInfo, tab) {
    // read changeInfo data and do something with it (like read the url)
    if (changeInfo.status) {
      console.log("The URL has changed");
      console.log("status = "+changeInfo.status)
    }
    if(changeInfo.status == 'complete'){
      console.log('true');
      setTimeout(function(){
          extractButton(null)
      },1000);

    }
  }

function chromeOnMessageListener (message, sender, sendResponse){
    console.log("received : "+ message)
  }

//-------------------------------------------------------------


//on load
function onLoadDOM(){
  document.getElementById('extract-btn').addEventListener('click', extractButton);
  chrome.tabs.onUpdated.addListener(chromeOnTabUpdatedListener);
  chrome.runtime.onMessage.addListener(chromeOnMessageListener);
  extractButton(null)

  chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
    chrome.runtime.sendMessage({ msg: "test"}) //to backgorund.js
  });
  

  
}
document.addEventListener('DOMContentLoaded', onLoadDOM); 



