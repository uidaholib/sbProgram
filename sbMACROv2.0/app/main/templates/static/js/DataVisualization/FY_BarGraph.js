
// Doctored From http://bl.ocks.org/kiranml1/6872226 
function FY_BarGraph (reportDict) {

  $(document).ready(function () {

    //check that there are multiple FYs
    let FYs = [];
    for (let i = 0; i < reportDict.report.length; i++)
    {
      let identity = reportDict.identity[i].CSC + reportDict.identity[i].name;
      //if "identity" is not in the reasons array, add it.
      let fyIndex = FYs.indexOf(identity);
      if (fyIndex == -1) { FYs.push(identity); }
    }


    //if there is more than one FY, create the graph.
    if(FYs.length > 1){

      var fyObjArray = [];

      function createAndAddFYObject(FYname, FYsize, FYcsc){
        var FY = {};
        FY.name = FYcsc + " " + FYname;
        if (FYsize === "None") {
          // console.log("It's NONE")   //DeBug
          FY.size = 0;
        } else {
          FY.size = FYsize;
        }
        FY.CSC = FYcsc;
        fyObjArray.push(FY);
      // console.log("!!!!!!!!!!!!FYarray:");   //DeBug
      // console.log(fyObjArray);   //DeBug
      }
      function getFYsizes(report, identity){
        for (var i = 0; i < report.length; i++) {
          var fiscalYear = report[i];
          var FYcsc = identity[i].CSC;
          for (var z = 0; z < (fiscalYear.length - (fiscalYear.length-1)); z++) {
            var projectObj = fiscalYear[z];
            // console.log("projectObj");
            // console.log(projectObj);
            var FYname = projectObj.FY;
            // console.log("FYname");   //DeBug
            // console.log(FYname);   //DeBug
            var FYsize = projectObj.totalFYData;
            
            // console.log("data");   //DeBug
            // console.log(data);   //DeBug
            createAndAddFYObject(FYname, FYsize, FYcsc);
          }
        }
      }

      getFYsizes(reportDict.report, reportDict.identity);
      
      const fyMaxSize = getMaxSize(fyObjArray);
      if (fyMaxSize > 0){
        createFYGraph(fyObjArray)
      }
      else {
        createNoDataFyGraph();
      }
      
    }
    });
};

var getMaxSize = function (objArray) {
  var maxSize = 0;
  for (var i = 0; i < objArray.length; i++) {
    // console.log("current size: " + objArray[i].size);    //Debug
    // console.log("MaxSize: " + maxSize);    //Debug
    maxSize = objArray[i].size > maxSize ? objArray[i].size : maxSize;
  }
  return maxSize;
}

function createNoDataFyGraph() {
  // set the dimensions and margins of the graph
  var margin = { top: 40, right: 20, bottom: 30, left: 60 },
    width = 960 - margin.left - margin.right,
    height = 150 - margin.top - margin.bottom;
  //Should set width and height dynamically
  updateFYDimensions(window.innerWidth, window.innerHeight);
  //Come back to this to change graph layout for small screen sizes
  var breakPoint = 768;
  // set the ranges
  var y = d3.scaleLinear()
    .range([0, height])

  var x = d3.scaleLinear()
    .range([0, width]);

  // append the svg object to the body of the page
  // append a 'group' element to 'svg'
  // moves the 'group' element to the top left margin
  var svg = d3.select("#fyGraphWrapper").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .attr("id", "FYGraph_svg")
    .append("g")
    .attr("transform",
    "translate(" + margin.left + "," + margin.top + ")");



  // Scale the range of the data in the domains
  x.domain([0, 100])
  // y.domain(d3.range(data.length));
  y.domain([0,100]);
  //y.domain([0, d3.max(data, function(d) { return d.sales; })]);


  // append the rectangles for the bar chart

  //Adding x axis label
  svg.append("text")
    .attr("y", (.1 * height))
    .attr("x", (width/2))
    .attr("dy", "1em")
    .attr("font-size", "1.2em")
    .attr("font-style", "italic")
    .style("fill", "grey")
    .style("text-anchor", "middle")
    .text("Selected Fiscal Years");

  svg.append("text")
    .attr("y", (.3 * height))
    .attr("x", (width / 2))
    .attr("dy", "1em")
    .attr("font-size", "1.2em")
    .attr("font-style", "italic")
    .style("fill", "grey")
    .style("text-anchor", "middle")
    .text("contain no data");


  //Adding a title
  svg.append("text")
    .attr("x", (width / 2))
    .attr("y", 0 - (margin.top / 2))
    .attr("text-anchor", "middle")
    .style("font-size", "20px")
    .style("text-decoration", "underline")
    .text("ScienceBase Fiscal Year Data Comparison");

  //Updating dimensions
  function updateFYDimensions(winWidth, winHeight) {
    margin.top = 40;
    margin.right = winWidth < breakPoint ? 0 : 20;
    margin.left = winWidth < breakPoint ? 0 : 50;
    margin.bottom = 30;

    width = (winWidth * .50) - margin.left - margin.right;
    height = winHeight * 0.25;
  }
}


      //Now, building the graph:
function createFYGraph (data){
  // set the dimensions and margins of the graph
  var margin = { top: 40, right: 20, bottom: 30, left: 60 },
    width = 960 - margin.left - margin.right,
    height = 150 - margin.top - margin.bottom;
  //Should set width and height dynamically
  updateFYDimensions(data, window.innerWidth, window.innerHeight);
  //Come back to this to change graph layout for small screen sizes
  var breakPoint = 768;
  // set the ranges
  var y = d3.scaleBand()
    .range([0, height])
    .padding(0.1);

  var x = d3.scaleLinear()
    .range([0, width]);

  // append the svg object to the body of the page
  // append a 'group' element to 'svg'
  // moves the 'group' element to the top left margin
  var svg = d3.select("#fyGraphWrapper").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .attr("id", "FYGraph_svg")
    .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");

  // format the data
  data.forEach(function (d) {
    d.size = +d.size;
  });


  // Scale the range of the data in the domains
  x.domain([0, d3.max(data, function (d) { return d.size; })])
  // y.domain(d3.range(data.length));
  y.domain(data.map(function (d) { return d.name; }));
  //y.domain([0, d3.max(data, function(d) { return d.sales; })]);


  //Adding labels for amount of each bar

  //d3-tip: http://bl.ocks.org/davegotz/bd54b56723c154d25eedde6504d30ad7
  // Setup the tool tip.  Note that this is just one example, and that many styling options are available.
  // See original documentation for more details on styling: http://labratrevenge.com/d3-tip/
  var tool_tipFY = d3.tip()
    .attr("class", "d3-tip")
    .offset([0, 0])
    .html(function (d) { 
      var rStr = d.size.toString().substring(0, 4);
      if (parseFloat(rStr) < 0.01) {
        rStr = "Less than 0.01";
      } else {
        rStr = "~"+rStr;
      }
      return rStr+"gb"; 
    });
  svg.call(tool_tipFY);


  // append the rectangles for the bar chart
  
  var bars = svg.selectAll(".bar")
    .data(data)
    .enter().append("rect")
      .attr("class", "bar")
      .attr("id", function (d) {
        // console.log(d.CSC); 
        return d.CSC; 
      })
      //.attr("x", function(d) { return x(d.sales); })
      .attr("width", function (d) { return x(d.size); })
      .attr("y", function (d,i) { return y(d.name); })
      .attr("height", y.bandwidth())
      .on('mouseover', tool_tipFY.show)
      .on('mouseout', tool_tipFY.hide);

  // add the x Axis
  svg.append("g")
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(x));

  // add the y Axis
  var FYList = data.map(function (obj) {return obj.name});

  var yAxis = d3.axisLeft(y)  //);
    .tickFormat(function (d) { 

      var output = d.replace(' FY', '');

      // return d.substring(5, 13); 
      return output;
    });

  svg.append("g")
    .call(yAxis);

  //Adding x axis label
  svg.append("text")
    .attr("y", (height + margin.bottom/2))
    .attr("x", width)
    .attr("dy", "1em")
    .attr("font-size", ".8em")
    .style("text-anchor", "end")
    .text("Gigabytes (GB)");


  //Adding a title
  svg.append("text")
    .attr("x", (width / 2))
    .attr("y", 0 - (margin.top / 2))
    .attr("text-anchor", "middle")
    .style("font-size", "20px")
    .style("text-decoration", "underline")
    .text("ScienceBase Fiscal Year Data Comparison");


  //Adding Legend
  var legendRectSize = 18;
  var legendSpacing = 4;

  var existing_CSCs = [];

  for (var i = 0; i < data.length; i++) {
    if ($.inArray(data[i].CSC, existing_CSCs) === -1) {
      // the value is not in the array
      existing_CSCs.push(data[i].CSC);
    }
  }
  // console.log("existing_CSCs");
  // console.log(existing_CSCs);
  var legend = svg.selectAll('.legend')
    .data(data.filter(function (d) {
      var index = $.inArray(d.CSC, existing_CSCs);
      // console.log("index: "+index);
      if (index > -1) {
        // the value is in the array
        //remove element from array
        existing_CSCs.splice(index, 1);
        //use this d:
        return d;
      }
      else {
        //do nothing (skip this d)
      }
      // console.log("existing_CSCs2");
      // console.log(existing_CSCs);
    }))
    .enter()
    .append('g')
    .attr('class', 'legend')
    // .attr('id', function (d) { return d.CSC })
    .attr('transform', function (d, i) {
      // var height = legendRectSize + legendSpacing;
      // var offset = height * data.length / 2;
      // var horz = -2 * legendRectSize;
      // var vert = i * height - offset;
      var horz = width * 0.9;
      var vert = i * 19;
      return 'translate(' + horz + ',' + vert + ')';
    });

  legend.append('rect')
    .attr('class', function (d) { return 'legend'; })
    .attr('id', function (d) { return d.CSC; })
    .attr('width', legendRectSize)
    .attr('height', legendRectSize)


  legend.append('text')
    .attr('x', legendRectSize + legendSpacing)
    .attr('y', legendRectSize - legendSpacing)
    .text(function (d) { return d.CSC; });

  //Updating dimensions
  function updateFYDimensions(data, winWidth, winHeight) {
    // console.log("In UPdateDimensions");
    // console.log(data);
    margin.top = 40;
    margin.right = winWidth < breakPoint ? 0 : 20;
    margin.left = winWidth < breakPoint ? 0 : 75;
    margin.bottom = 30;

    width = (winWidth * .50) - margin.left - margin.right;
    var barRelativeSize = 70 + (10 * data.length)
    var widthRelativeSize = .5 * width;
    height = widthRelativeSize > barRelativeSize ? widthRelativeSize : barRelativeSize;
    // widthRelativeSize > barRelativeSize ? console.log("widthRelativeSize") : console.log("barRelativeSize");
    if (barRelativeSize > window.innerHeight) {
      height = winHeight * 0.5;
      // console.log("Height = window.innerHeight");
    }
    // console.log("End updateDimensions");
  }
}