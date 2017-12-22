

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

    //extract each url
    while (input != '')
    {
        let comma = input.indexOf(',');
        if (comma > -1)
        {
            //grab from the beginning to just before the comma as a url
            var url = input.substring(0,comma)
            console.log("url: " + url);
            URLarray.push(url)
            input = input.substring(comma+1, input.length)
            console.log("new input: " + input)
        }
        if (comma === -1 && input != '')
        {
            //take the whole thing as another url
            URLarray.push(input);
            input = '';
        }
    }
    console.log("URLarray");
    console.log(URLarray);
    createCollection(URLarray);
}


function createCollection (array) {
    const ul = document.querySelector('ul');
    ul.className = 'collection';//adds the collectin class to the ul's so they look good as a Materialize list
    for (var i = 0; i < array.length; i++)
    {
        const li = document.createElement('li'); //create a list item element
        li.className = 'collection-item';
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