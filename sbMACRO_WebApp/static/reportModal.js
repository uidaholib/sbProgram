function findModalBtns () {
    $(document).ready(function () {
        var modal_btns = document.getElementsByClassName('modalbtn');
        // console.log("modal_btns");
        // console.log(modal_btns);
        // console.log("modal_btns[0].id");
        // console.log(modal_btns[0]['id']);

        // modal_btns.forEach(function (element, i) {
        //     console.log(element.id);//do your stuffs
        // });
        for (let i = 0; i < modal_btns.length; i++)
        {
            let m_id = modal_btns[i].id;
            // console.log("modal_btns[i].id");
            // console.log(m_id);
            createModal(m_id)
            // modal_btns[i].onclick = displayModal(m_id);
            // if (modal_btns[i].attachEvent) {
            //     modal_btns[i].attachEvent("click", displayModal(m_id));
            // } else {
            //     modal_btns[i].addEventListener("click", displayModal(m_id));
            // }
            // $("#"+m_id).click( displayModal(m_id))
            
        }
        
    });
}
// $(document).ready(function () {
//     $("#btnExport2").click(function (e) {
//         e.preventDefault();
var displayModal = function (elem) {
    // alert("clicked!");
    // console.log("clicked");
    // console.log(elem.id);
    let modal = document.getElementById(elem.id+"_div");
    // console.log(modal);
    modal.style.display = "block";
}
function createModal(id) {
    let project_id = id.replace("modal_", '');

    let projectDict = reportDict['projects'][project_id];
    let modal_id = id + "_div";
    let BaseModal = document.getElementById("BaseModal");
    let newModal = $("<div></div>").attr("id", modal_id).addClass("projModal");
    // let newModal = $("<div></div>");
    let basicModalContent = $('#BaseModal').html();
    // console.log(basicModalContent);
    newModal.html(basicModalContent);
    // newModal.attr("id", id);
    $("#BaseModal").after(newModal);
    // console.log(newModal);
    // console.log(BaseModal);
    // console.log(id);
    // When the user clicks on <span> (x), close the modal
    // Get the <span> element that closes the modal
    // var span = document.getElementsByClassName("close");
    var span = $('#' + modal_id).find('.close');
    // console.log(span);
    span.on("click", function () {
        // closeModal(id + "_div");
        console.log("close");
        let modal = document.getElementById(modal_id);
        modal.style.display = "none";
    });

    // add project title
    var title = $('#' + modal_id).find('.title');
    title.text(projectDict['title']).wrap('<a href="' + projectDict['URL']+'" target="_blank"></a>');

    //add PI
    for (let i = 0; i < projectDict['contacts'].length; i++){
        if (projectDict['contacts'][i]['type'] === "Principal Investigator")
        {
            var PI = $('#' + modal_id).find('.PI');
            PI.text(projectDict['contacts'][i]['name'])
                .wrap('<a href="mailto:' + projectDict['contacts'][i]['email'] + '"></a>');
        }
    }

    // add summary
    var summary = $('#' + modal_id).find('.summary');
    summary.text(projectDict['summary']);

    // add history
    var history = $('#' + modal_id).find('.history');
    let histText = projectDict['history'];
    histText = histText.replace(/(?:\r\n|\r|\n)/g, '<br />'); //replaces newline character (\n) with html equivalent (<br />)
    history.html(histText);


    // add potential products
    var PotentialProd = $('#' + modal_id).find('.potential_products');
    let potProdText = projectDict['Potential_Products']
    potProdText = potProdText.replace(/(?:\r\n|\r|\n)/g, '<br />'); //replaces newline character (\n) with html equivalent (<br />)
    PotentialProd.html(potProdText);

    // add products recieved
    var ProdRecieved = $('#' + modal_id).find('.products_recieved');
    ProdRecieved.text(projectDict['Received_Products']);
    
    // Display DMP status
    if(projectDict['DMP'] === "Approved")
    {
        $("#"+modal_id).find(".DMPstatus_good").css("display", "inline-block");
    } else if (projectDict['DMP'] === "None" || projectDict['DMP'] === "none" || projectDict['DMP'] === "n/a") {
        $("#" + modal_id).find(".DMPstatus_neutral").css("display", "inline-block");
    } else if (projectDict['DMP'] === "Project not currently tracked by Data Steward") {
        $("#" + modal_id).find(".DMPstatus_neutral").css("display", "inline-block");
    } else {
        $("#" + modal_id).find(".DMPstatus_bad").css("display", "inline-block");
    }
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function (event) {
    if ( $(event.target).hasClass("projModal")) {
        let modal = document.getElementById(event.target.id);
        modal.style.display = "none";
    }
}



function closeModal(id) {
    
}

