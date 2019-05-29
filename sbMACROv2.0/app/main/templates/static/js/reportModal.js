function findModalBtns(projectArray) {
  $(document).ready(function () {
    var modalBtns = document.getElementsByClassName('modalbtn')
    for (var i = 0; i < modalBtns.length; i++) {
      let m_id = modalBtns[i].id

      createModal(m_id, projectArray)
    }
  })
}

var displayModal = function (elem) {
  let modal = document.getElementById(elem.id + '_div')
  modal.style.display = 'block'
  let thead = document.getElementById('table_head')
  thead.style.display = 'none'
}

function createModal(sbId, projectArray) {
  let projectSbId = sbId.replace('modal_', '')
  let project = null
  for (var i = 0; i < projectArray.length; i++) {
    if (projectArray[i].sb_id === projectSbId) {
      project = projectArray[i]
      break
    }
  }
  if (project === null) {
    console.error('Could could not find project ' + projectSbId)
  }
  let modal_id = sbId + '_div'
  let BaseModal = document.getElementById('BaseModal')
  let newModal = $('<div></div>')
    .attr('id', modal_id)
    .addClass('projModal')
  let basicModalContent = $('#BaseModal').html()
  newModal.html(basicModalContent)
  $('#BaseModal').after(newModal)

  var span = $('#' + modal_id).find('.close')
  span.on('click', function () {
    let modal = document.getElementById(modal_id)
    modal.style.display = 'none'
    let thead = document.getElementById('table_head')
    thead.style.display = 'table-header-group'
  })

  //Create Pie Chart
  createPieChart(d3, project, modal_id)

  // add project title
  var title = $('#' + modal_id).find('.title')
  title
    .text(project.name)
    .wrap('<a href="' + project.url + '" target="_blank"></a>')

  //add PI
  let PI = $('#' + modal_id).find('.PI')
  for (let i = 0; i < project.pi_list.length; i++) {
    let currPiHtml = project.pi_list[i].name
    if (project.pi_list[i].email) {
      currPiHtml =
        '<a href="mailto:' +
        project.pi_list[i].email +
        '">' +
        currPiHtml +
        '</a>'
    }
    if (i === 0) {
      PI.append(currPiHtml)
    } else {
      PI.append('</br>' + currPiHtml)
    }
  }
  PI.append('</br></br>')

  // add summary
  var summary = $('#' + modal_id).find('.summary')
  summary.text(project.summary)

  // add history
  var history = $('#' + modal_id).find('.history')
  let histText = project.history
  histText = histText.replace(/(?:\r\n|\r|\n)/g, '<br />') //replaces newline character (\n) with html equivalent (<br />)
  history.html(histText)

  // add potential products
  var PotentialProd = $('#' + modal_id).find('.potential_products')
  let potProdText = project.potential_products
  potProdText = potProdText.replace(/(?:\r\n|\r|\n)/g, '<br />') //replaces newline character (\n) with html equivalent (<br />)
  PotentialProd.html(potProdText)

  // add products received
  var ProdReceived = $('#' + modal_id).find('.products_received')
  let prodRecArray = project.products_received
  let html = ''
  for (let i = 0; i < prodRecArray.length; i++) {
    if (prodRecArray[i].name) {
      let item_name = prodRecArray[i].name

      html +=
        '<a href="' +
        prodRecArray[i].url +
        '" target="_blank">' +
        (i + 1) +
        '. ' +
        prodRecArray[i].name +
        '</a><br>'
    }
  }
  if (html != '') {
    ProdReceived.html(html)
  } else {
    ProdReceived.html('No Science Base Items found.')
  }

  // Display DMP status
  if (project.dmp_status === 'Approved') {
    $('#' + modal_id)
      .find('.DMPstatus_good')
      .css('display', 'inline-block')
  } else if (
    project.dmp_status === 'None' ||
    project.dmp_status === 'none' ||
    project.dmp_status === 'n/a'
  ) {
    $('#' + modal_id)
      .find('.DMPstatus_neutral')
      .css('display', 'inline-block')
  } else if (
    project.dmp_status === 'Project not currently tracked by Data Steward'
  ) {
    $('#' + modal_id)
      .find('.DMPstatus_neutral')
      .css('display', 'inline-block')
  } else {
    $('#' + modal_id)
      .find('.DMPstatus_bad')
      .css('display', 'inline-block')
  }
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function (event) {
  if ($(event.target).hasClass('projModal')) {
    let modal = document.getElementById(event.target.id)
    modal.style.display = 'none'
    let thead = document.getElementById('table_head')
    thead.style.display = 'table-header-group'
  }
}

// function closeModal(id) {

// }