window.Scraper = {
  "ping" : function () {

    return "HELLO WORLD!"
      
  },
  // find where post block start and end
  "findPostBlocks" : function (pagename, liketxt) {

    max_find = 14
    post_blocks = []

    $("a").each(function(i ,v) {
      if ($(this).text() == pagename) {

        var result = {
          "elem" : [],
          "found" : false
        }
        
        function findTxtChild(elem) {
          var children = $(elem).children()
          if (children.length != 0) {
    
            for (var i = 0; i < children.length; i++) {
              var child = children[i]
              if (findTxtChild(child)) {
                // console.log(child)
                // arr.push(child)
                result.elem.push(child)
                return true
              }
            }
    
          } else {
    
            if ($(elem).text() == liketxt) {
              result.found = true
              return true
            } else {
              return false
            }
    
          }
    
        }

        var parent = $(this).parent()[0]
        var retry = 0
        while (!result.found && retry <= max_find) {
          retry++
          parent = $(parent).parent()[0]
          findTxtChild(parent)
        }

        var post_block = $(result.elem.slice(-1).pop()).parent();
        post_blocks.push(post_block[0]);
      }

    })

    // cyclic object value selenium exception
    return post_blocks
    // return String(post_blocks)

  },
  // find where the text is located in elem
  "findTxt" : function (elem, text) {

    var result = {
      "elem" : [],
      "found" : false
    }

    var maxretry = 10
    var retry = 0

    var etext = $(elem).find("p")
    if (etext.get(0) != undefined) {
      while (!etext.is(elem) && maxretry >= retry) {
        result.elem.push(etext.prop("tagName"))
        etext = $(etext.parent())
        retry++
      }
    
      result.found = true
    }

    return result

    // return $(elem).find("p").text()

  },
  // find where the text is located in elem
  "findTxtOld" : function (elem, text) {

    var result = {
      "elem" : [],
      "found" : false
    }

    function findTxtChild(elem) {
      var children = $(elem).children()
      if (children.length != 0) {

        for (var i = 0; i < children.length; i++) {
          var child = children[i]
          if (findTxtChild(child)) {
            // console.log(child)
            // arr.push(child)
            result.elem.push(child)
            return true
          }
        }

      }

      if ($(elem).text() == text) {
        return true
      } else {
        return false
      }

    }

    result.found = findTxtChild(elem, 0);

    return result


  },
  // find where img tags are located 
  "findImgTags" : function (elem) {
    var result = {
      "elems" : [],
      "found" : false
    }
    
    // we have to exclude dupicate image suck as profile pic, like, etc
    var exclude = { w: 35, h: 35 }
    var imgs = $(elem).find("img")
    for (var i = 0; i < imgs.length; i++) {
      var img = $(imgs[i]);
      if (img.width() > exclude.w || img.height() > exclude.h) {
        var ielem = []
        while (!img.is(elem)) {
          ielem.push(img.prop("tagName"))
          img = $(img.parent())
        }
        result.elems.push(ielem)
      }
    }
    
    if (result.elems.length != 0) {
      result.found = true
    }

    return result

  },
  // clear everyting inside body tag
  "clearbody" : function() {
    $("body").empty()
    $(document.body).trigger('load');
    return true
  },

  // inject html to body
  "html" : function(html) {
    $("body").html(html);
    return true
  },

  // find number of like by expending like button
  "findLikeCount" : function(elem, liketxt) {
    
    var result = {
      "elem" : [],
      "found" : false
    }

    var maxretry = 20
    var retry = 0

    // .replace(/\D+/g, '');

    var etext = $(elem).find("span:contains("+ liketxt + ")" )
    if (etext.get(0) != undefined) {
      while (!etext.is(elem) && maxretry >= retry) {
        if (result.found) { 
          
          result.elem.push(etext.prop("tagName"))
          etext = $(etext.parent())

        } else if (/\d/.test(etext.text())) {

          likecount = etext.text().replace(/\D+/g, '')

          etext = $(etext).find(":contains("+likecount+")")
          
          result.found = true

        } else {
          etext = $(etext.parent())
        }
        
        retry++
      }
    }

    if (result.elem[0] == undefined) {
      result.elem = []
      result.found = false
    }

    return result

  },

  // find number of comments by expending comment button
  "findCommentCount" : function(elem, commenttxt) {
    
    var result = {
      "elem" : [],
      "found" : false
    }

    var maxretry = 20
    var retry = 0

    // .replace(/\D+/g, '');

    var etext = $(elem).find("a:contains("+ commenttxt + ")" )
    if (etext.get(0) != undefined) {
      while (!etext.is(elem) && maxretry >= retry) {
        if (result.found) { 
          
          result.elem.push(etext.prop("tagName"))
          etext = $(etext.parent())

        } else if (/\d/.test(etext.text())) {
          
          result.found = true

        } else {
          etext = $(etext.parent())
        }
        
        retry++
      }
    }

    if (result.elem[0] == undefined) {
      result.elem = []
      result.found = false
    }

    return result

  }
  

}