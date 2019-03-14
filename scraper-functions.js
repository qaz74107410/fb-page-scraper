window.Scraper = {
  "ping" : function () {

    return "HELLO WORLD!"
    
  },
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
  "findTxt" : function (elem, text) {

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


  }
}