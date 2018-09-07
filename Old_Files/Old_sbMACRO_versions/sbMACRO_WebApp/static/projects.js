

function gatherProjects () {
    // alert('button clicked');
    let URLarray = [];
    let input = document.querySelector('#url').value; // item is gotten from the for input with id 'item'
    console.log("input1: " + input);
    $('#url').val(''); //clear the input 

    //clear any spaces
    while (input.indexOf(' ') > -1)
    {
        input = input.replace(' ', '');
    }
    console.log("input w/0 spaces: " + input);
    let blank = false;
    
    
    let anySkipped = false;
    let amountSkipped = 0;
    let reasons = [];

    if (input == '')
    {
        blank = true;
        amountSkipped++;
        console.log("Blank Entry");
        problemAlert(amountSkipped, reasons, blank);
    }
    //extract each url
    while (input != '')
    {
        let comma = input.indexOf(',');
        if (comma > -1)
        {
            //grab from the beginning to just before the comma as a url
            var url = input.substring(0,comma)
            console.log("url: " + url);
            //change to correct url format (folder->item) if necessary
            if (url.includes("https://www.sciencebase.gov/catalog/folder")) {
                url = url.replace("https://www.sciencebase.gov/catalog/folder", "https://www.sciencebase.gov/catalog/item")
            }
            if (url.includes("https://www.sciencebase.gov/catalog/item")) {
                URLarray.push(url)
            } else {
                anySkipped = true;
                console.log("Skipped 1");
                amountSkipped++;
                //if "format" is not in the reasons array, add it.
                let typeIndex = reasons.indexOf("format");
                if (typeIndex == -1) { reasons.push("format"); }
            }
            input = input.substring(comma+1, input.length)
            console.log("new input: " + input)
        }
        if (comma === -1 && input != '')
        {
            //change to correct url format (folder->item) if necessary
            if (input.includes("https://www.sciencebase.gov/catalog/folder"))

            {

                input = input.replace("https://www.sciencebase.gov/catalog/folder", "https://www.sciencebase.gov/catalog/item")
            }
            //check that it has the right format
            if (input.includes("https://www.sciencebase.gov/catalog/item"))
            {
                //take the whole thing as another url
                // console.log("check here:");
                // console.log("https://www.sciencebase.gov/catalog/item/4f4e476ae4b07f02db47e13b".length);
                URLarray.push(input);
            } else {
                anySkipped = true;
                console.log("Skipped 2");
                console.log(input);
                amountSkipped++;
                //if "format" is not in the reasons array, add it.
                let typeIndex = reasons.indexOf("format");
                if (typeIndex == -1) { reasons.push("format"); }
            }            
            input = '';
        }
    }
    
    if(anySkipped===true)
    {
        problemAlert(amountSkipped, reasons, blank);
    }
    console.log("URLarray");
    console.log(URLarray);
    if(URLarray.length > 0){
        createCollection(URLarray);
    }
    
}

function problemAlert (amountSkipped, reasons, blank){
    if(blank)
    {
        alert("Please add a Science Base Project URL");
        return;
    }
    let wasORwere;
    if (amountSkipped == 1) { wasORwere = 'was'; }
    else { wasORwere = 'were'; }

    if (reasons.indexOf("length") > -1 && reasons.indexOf("format") > -1) {
        alert(amountSkipped + " of the URL(s) provided did not appear to be either formated correctly or of the correct length and " + wasORwere + " discarded.");
    } else if (reasons.indexOf("format") > -1) {
        alert(amountSkipped + " of the URL(s) provided did not appear to be the correct format and " + wasORwere + " discarded.");
    } else if (reasons.indexOf("length") > -1) {
        alert(amountSkipped + " of the URL(s) provided did not appear to be of the correct length and " + wasORwere + " discarded.");
    }
};

function createCollection (array) {
    if (array.length === 0) {
        return;
    }
    const ul = document.querySelector('ul');
    ul.className = 'collection';//adds the collectin class to the ul's so they look good as a Materialize list
    for (var i = 0; i < array.length; i++)
    {
        const li = document.createElement('li'); //create a list item element
        li.className = 'collection-item SBurls';
        const inputEl = document.createElement('input');
        inputEl.setAttribute("type", "hidden")
        inputEl.setAttribute("name", "SBurls");
        inputEl.setAttribute("value", array[i]);
        li.appendChild(inputEl);
        const itemText = document.createTextNode(array[i]); //take the text from where we are in the array of urls as variable 'itemText'
        li.appendChild(itemText);   //add itemText within li
        ul.appendChild(li); //add li within ul.
        
    }
    
}
const ul = document.querySelector('ul');
//remove item
ul.addEventListener('dblclick', removeItem);//listen for a double ckick, and call removeItem if you hear it
function removeItem(e) {
    e.target.remove();
    if (ul.children.length == 0) {
        ul.className = '';
    }
}
//to set what enter does when in the input box
$(document).ready(function () {
    $('#url').keypress(function (e) {
        
        if (e.keyCode == 13)
        {
            $('#addProj').click();
        }
    });
});

function processForm(e) {

    const urls = document.getElementsByClassName("SBurls");
    console.log(urls);

    if (urls.length > 0) {
        // You must return true to allow the default form behavior
        return true;
    }
    else {
        if (e.preventDefault) e.preventDefault();
        DontShowLoading();
        alert("Please add a Science Base Project URL");
        // You must return false to prevent the default form behavior
        return false;
    }
    /* do what you want with the form */

}


const form = document.getElementById('Project-Select-Form');
if (form.attachEvent) {
    form.attachEvent("submit", processForm);
} else {
    form.addEventListener("submit", processForm);
}