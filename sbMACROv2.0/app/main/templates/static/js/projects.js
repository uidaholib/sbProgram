function gatherProjects() {
  let input = document.querySelector('#url').value // item is gotten from the for input with id 'item'
  // console.log('input1: ' + input)
  input = input.replace(/,/g, ' ')
  // console.log('input: comma->space')
  // console.log(input)
  $('#url').val('') //clear the input
  let anySkipped = false
  let amountSkipped = 0
  let reasons = []
  let blank = false
  if (input.trim().length < 65) {
    //String must at least be length of the url
    if (input.trim().length === 0) {
      blank = true
      // console.log('skipped1')
      amountSkipped++
      anySkipped = true
      // console.log('Blank Entry')
    } else {
      //if "length" is not in the reasons array, add it.
      let typeIndex = reasons.indexOf('length')
      if (typeIndex == -1) {
        reasons.push('length')
      }
      // console.log('skipped2')
      amountSkipped++
      anySkipped = true
    }
    problemAlert(amountSkipped, reasons, blank)
  }

  let urlArray = input.split(/(\s+)/).filter(function(e) {
    // Must include part of science base url
    if (
      e.indexOf('https://www.sciencebase.gov/catalog/folder') > -1 ||
      e.indexOf('https://www.sciencebase.gov/catalog/item') > -1
    ) {
      //Must insure that the url is the correct length after including
      //sb ID
      if (e.trim().length > 64 || e.trim().length < 69) {
        return true
      } else {
        if (e.trim().length > 0) {
          //If 0, it is filtered whitespace
          // console.log('skipped3')
          amountSkipped++
          anySkipped = true
          //if "length" is not in the reasons array, add it.
          let typeIndex = reasons.indexOf('length')
          if (typeIndex == -1) {
            reasons.push('length')
          }
        }
        return false
      }
    } else {
      if (e.trim().length > 0) {
        //If 0, it is filtered whitespace
        // console.log('skipped4')
        amountSkipped++
        anySkipped = true
        //if "format" is not in the reasons array, add it.
        let typeIndex = reasons.indexOf('format')
        if (typeIndex == -1) {
          reasons.push('format')
        }
      }
      return false
    }
  })
  urlArray = urlArray.map(entry => {
    //change to correct url format (folder->item) if necessary
    if (entry.includes('https://www.sciencebase.gov/catalog/folder')) {
      entry = entry.replace(
        'https://www.sciencebase.gov/catalog/folder',
        'https://www.sciencebase.gov/catalog/item'
      )
    }
    return entry
  })
  // console.log('urlArray:')
  // console.log(urlArray)

  // if (anySkipped === true) {
  //   problemAlert(amountSkipped, reasons, blank)
  // }
  // console.log('urlArray')
  // console.log(urlArray)
  if (urlArray.length > 0) {
    createCollection(urlArray)
  }
}

function problemAlert(amountSkipped, reasons, blank) {
  if (blank) {
    alert('Please add a Science Base Project URL')
    return
  }
  let wasORwere
  if (amountSkipped == 1) {
    wasORwere = 'was'
  } else {
    wasORwere = 'were'
  }

  if (reasons.indexOf('length') > -1 && reasons.indexOf('format') > -1) {
    alert(
      amountSkipped +
        ' of the URL(s) provided did not appear to be either formated correctly or of the correct length and ' +
        wasORwere +
        ' discarded.'
    )
  } else if (reasons.indexOf('format') > -1) {
    alert(
      amountSkipped +
        ' of the URL(s) provided did not appear to be the correct format and ' +
        wasORwere +
        ' discarded.'
    )
  } else if (reasons.indexOf('length') > -1) {
    alert(
      amountSkipped +
        ' of the URL(s) provided did not appear to be of the correct length and ' +
        wasORwere +
        ' discarded.'
    )
  }
}

function createCollection(array) {
  if (array.length === 0) {
    return
  }
  let ul = document.querySelector('.SbCollection')
  // console.log(ul)
  if (!ul.className.includes(' collection')) {
    ul.className += ' collection' //adds the collection class to the ul's so they look good as a Materialize list
  }
  for (var i = 0; i < array.length; i++) {
    let li = document.createElement('li') //create a list item element
    li.className = 'collection-item SBurls'
    let inputEl = document.createElement('input')
    inputEl.setAttribute('type', 'hidden')
    inputEl.setAttribute('name', 'SBurls')
    inputEl.setAttribute('value', array[i])
    li.appendChild(inputEl)
    let itemText = document.createTextNode(array[i]) //take the text from where we are in the array of urls as variable 'itemText'
    li.appendChild(itemText) //add itemText within li
    ul.appendChild(li) //add li within ul.
  }
}
let ul = document.querySelector('.SbCollection')
//remove item
ul.addEventListener('dblclick', removeItem) //listen for a double click, and call removeItem if you hear it
function removeItem(e) {
  e.target.remove()
  if (ul.children.length == 0) {
    ul.className = ''
  }
}
//to set what enter does when in the input box
$(document).ready(function() {
  $('#url').keypress(function(e) {
    if (e.keyCode == 13) {
      $('#addProj').click()
    }
  })
})

function processForm(e) {
  const urls = document.getElementsByClassName('SBurls')
  // console.log(urls)

  if (urls.length > 0) {
    // You must return true to allow the default form behavior
    return true
  } else {
    if (e.preventDefault) e.preventDefault()
    DontShowLoading()
    alert('Please add a Science Base Project URL')
    // You must return false to prevent the default form behavior
    return false
  }
  /* do what you want with the form */
}

const form = document.getElementById('Project-Select-Form')
if (form.attachEvent) {
  form.attachEvent('submit', processForm)
} else {
  form.addEventListener('submit', processForm)
}
