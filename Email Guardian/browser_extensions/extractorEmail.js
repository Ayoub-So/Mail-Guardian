class ExtractorEmail {




    constructor(htmlDocumentElement,type="gmail", ) {
      if (type === 'gmail') {
        this.mail = document.getElementsByClassName("gs"); //HTMLCollection []
        this.subject= document.getElementsByClassName("hP")[0]; //HTMLCollection [] 
        this.senderAndDate = this.mail[0].childNodes[0];
        this.date = this.mail[this.mail.length-1].childNodes[0].getElementsByClassName("g3")[0];
        this.body = this.mail[this.mail.length-1].childNodes[2];

        //
        //this.sender = this.mail[this.mail.length-1].childNodes[0].getElementsByClassName("go")[0];

        let mytxt= this.mail[this.mail.length-1].childNodes[0].getInnerHTML()
        this.sender =  mytxt.substring(mytxt.indexOf('email=')+7 , mytxt.indexOf('"',mytxt.indexOf('email=')+7))

      } else if (type === 'outlook') {
        this.mail = null
        
      } else this.mail = null;
    }
  }
  

