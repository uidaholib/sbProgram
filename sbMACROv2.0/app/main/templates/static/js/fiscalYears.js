//to set what enter does when in the input box
// $(document).ready(function () {
//     $('#submit').submit(function (e) {

//         var boxes = document.getElementsByClassName("FY-Checkbox");
//         console.log(boxes);
//         e.preventDefault();
//         if (3 === 4) {
//             e.preventDefault();
//             alert("Please Select a Fiscal Year");
//         }
//     });
// });


function processForm(e) {
    
    const boxes = document.getElementsByClassName("FY-Checkbox");
    // console.log(boxes);
    let anyChecks = false;
    for(var i = 0; i < boxes.length; i++)
    {   
        if(boxes[i].checked===true)
        {
            anyChecks = true;
            // console.log(boxes[i].checked);
        }
    }
    if(anyChecks===true)
    {// You must return true to allow the default form behavior
        return true;
    }
    else {
        if (e.preventDefault) e.preventDefault();
        DontShowLoading();
        alert("Please select a Fiscal Year");
        // You must return false to prevent the default form behavior
        return false;
    }
    /* do what you want with the form */
    
}


const form = document.getElementById('FY-Select-Form');
if (form.attachEvent) {
    form.attachEvent("submit", processForm);
} else {
    form.addEventListener("submit", processForm);
}