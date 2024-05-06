
//import { ExtractorEmail } from "./extractorEmail";

//website waits for message to send mail data
const isEmailOpened = (document) => document.getElementsByClassName("hP").length > 0 ? true:false

if (!window.firstTimeExecuted) {
    console.log("executed content.js");
    window.firstTimeExecuted = true;
    chrome.runtime.onMessage.addListener((data, sender, sendResponse) => {
        console.log("received message : " + data.msg);
        //wait for message from "popup.js"
        if (data.msg == "giveme") {
            var list= document.getElementsByClassName("gs");
            var subj= document.getElementsByClassName("hP"); 
            for (var i = 0; i < list.length; i++) {
                console.log(list[i].innerText);  
                extract_info_from_mail(list[i],subj) 
            }  
        }

        if(data.msg == "urlchange"){
            console.log("url changed" + data.status)
            //console.log("url changed" + data.status)
            //check if email is open
            isEmailOpened = document.getElementsByClassName("hP").length > 0 ? true:false

            if(isEmailOpened){console.log("email opened !")}
            else {console.log("email NOT opened !")}
            
            //TODO
        }
        //wait for button 3 clicked
        if(data.msg == "button3"){
            console.log("button 3 clicked")
            let extractor = new ExtractorEmail(document)
            txt_to_send = extractor.sender.innerText //.substring(1,ret.length-1)  //remove <>

            sendResponse({response :  txt_to_send})

            
        }


        //Real Extract button
        if(data.msg == "extract"){
            if(!isEmailOpened(document)) 
                console.log("not email")
            else{
                console.log("extracting")
                let extractor = new ExtractorEmail(document)
                console.log(extractor)
                
                a = extractor.sender
                b = extractor.subject.innerText
                c = extractor.body.innerHTML

                console.log("body is :")
                console.log(c)
                sendResponse({
                    'sender' : a,
                    'subject' : b,
                    'body' : c
                })
            }

        }
    });
}


function extract_info_from_mail(data,subj) {  // data = list[0]
    senderAndDate = data.childNodes[0].innerText
    email = data.childNodes[0].getElementsByClassName("go")[0].innerText
    date = data.childNodes[0].getElementsByClassName("g3")[0].innerText
    body_text = data.childNodes[2].innerText
    body_html = data.childNodes[2].innerHTML
    subject = data.innerText

} 



function getCurrentTabUrl(callback) {
    // Query for the active tab in the current window
    chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
      // Chrome returns an array of tab objects
      var tab = tabs[0];
      // Extract the URL from the tab object
      var url = tab.url;
      // Pass the URL to the callback function
      callback(url);
    });
  }











/*
  //subject
 var list= document.getElementsByClassName("hP");
    for (var i = 0; i < list.length; i++) {
        console.log(list[i].innerText);

//sender/reciver :
Division du Système d'Information - UCA <dsi@uca.ac.ma>
13 févr. 2024 18:52 (il y a 3 jours)
À cci : alluca

 var list= document.getElementsByClassName("gE");
    for (var i = 0; i < list.length; i++) {
        console.log(list[i].innerText);}

// sender+receiver + body

 var list= document.getElementsByClassName("gs");

// date 

var list= document.getElementsByClassName("g3");

*/