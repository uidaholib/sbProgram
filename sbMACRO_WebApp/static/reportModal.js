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

    let BaseModal = document.getElementById("BaseModal");
    let newModal = $("<div></div>").attr("id", id+"_div").addClass("projModal");
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
    var span = $('#' + id + "_div").find('.close');
    // console.log(span);
    span.on("click", function () {
        // closeModal(id + "_div");
        console.log("close");
        let modal = document.getElementById(id + "_div");
        modal.style.display = "none";
    });
    // console.log(span);
    // for(var i = 0; i < span.length; i++)
    // {
    //     span[i].onclick = function callCloseModal(){
    //         closeModal(id+"_div");
    //     };
    // }
    

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

