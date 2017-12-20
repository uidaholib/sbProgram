
var createGraphfunc;
var NWCSC_projectObjArray;
var SWCSC_projectObjArray;
function projectBarGraph (reportDict) {
  // console.log("GRAPH-BUILDING SCRIPT");   //DeBug
  $(document).ready(function () {
    console.log("reportDict in second script:");   //DeBug
    
    console.log(reportDict);   //DeBug
    
  NWCSC_projectObjArray = [];
  SWCSC_projectObjArray = [];

  var createAndAddObject = function (name, size, number, FY, CSC) {
    var project = {};
    project.name = name;
    if (size === "None") {
      // console.log("It's NONE")   //DeBug
      project.size = 0;
    } else {
      project.size = size;
    }
    project.number = number.toString();
    project.FY = FY.substring(3,7);
    project.CSC = CSC;
    // console.log("project:");   //DeBug
    // console.log(project);   //DeBug
    if (CSC === "NWCSC")
    {
      console.log("NWCSC!");
      NWCSC_projectObjArray.push(project);
    }
    if (CSC === "SWCSC")
    {
      console.log("SWCSC!");
      SWCSC_projectObjArray.push(project);
    }
    
    // console.log("!!!!!!!!!!!!array:");   //DeBug
    // console.log(projectObjArray);   //DeBug
  }
  function iterate(reportDict) {
    var report = reportDict.report;
    var identity = reportDict.identity;
    var projectNumber = 0
    // console.log("report");   //DeBug
    // console.log(report);   //DeBug
    for (var i = 0; i < report.length; i++) {
      var fiscalYear = report[i];
      var FY = identity[i].name;
      var csc = identity[i].CSC;
      console.log("FY:")   //DeBug
      console.log(FY);   //DeBug
      for (var z = 0; z < fiscalYear.length; z++) {
        projectNumber++;
        var projectObj = fiscalYear[z];
        var name = projectObj.name;
        // console.log("name");   //DeBug
        // console.log(name);   //DeBug
        var size = projectObj.DataInProject;
        // console.log("data");   //DeBug
        // console.log(data);   //DeBug
        createAndAddObject(name, size, projectNumber, FY, csc);
      }
    }
  }
  iterate(reportDict);
  NWCSC_Max = getMaxSize(NWCSC_projectObjArray);
  SWCSC_Max = getMaxSize(SWCSC_projectObjArray);
  //Check which size is the max size of all data.
  if( NWCSC_Max >= SWCSC_Max)
  {
    var Max = NWCSC_Max;
  }
  else {
    var Max = SWCSC_Max;
  }
  createGraph(NWCSC_projectObjArray, "NWCSC", Max);
  createGraph(SWCSC_projectObjArray, "SWCSC", Max);
});
};
  
var getMaxSize = function (objArray) {
  var maxSize = 0;
  for (var i = 0; i < objArray.length; i++)
  {
    // console.log("current size: " + objArray[i].size);    //Debug
    // console.log("MaxSize: " + maxSize);    //Debug
    maxSize = objArray[i].size > maxSize ? objArray[i].size : maxSize;
  }
  return maxSize;
}

function createGraph (data, currCSC, DATA_max){
  console.log("In createGraph");
  // var data = projectObjArray;
  // set the dimensions and margins of the graph
  var margin = {top: 40, right: 20, bottom: 30, left: 40},
      width = 960 - margin.left - margin.right,
      height = 500 - margin.top - margin.bottom;
      //Should set width and height dynamically
  updateDimensions(data, window.innerWidth, window.innerHeight);

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
  var svg = d3.select("#wrapper").append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .attr("id", "projectGraph_svg")
      .append("g")
      .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

  // format the data
  data.forEach(function(d) {
    d.size = +d.size;
  });
  

  // Scale the range of the data in the domains
  // x.domain([0, d3.max(data, function(d){ return d.size; })])
  //Instead of normal ^, we must use max of both datasets for both graphs.
  x.domain([0, DATA_max]) 
  y.domain(data.map(function(d) { return d.number; }));
  //y.domain([0, d3.max(data, function(d) { return d.sales; })]);

  //Adding labels for amount of each bar

  //d3-tip: http://bl.ocks.org/davegotz/bd54b56723c154d25eedde6504d30ad7
  // Setup the tool tip.
  // See original documentation for more details on styling: http://labratrevenge.com/d3-tip/
  var tool_tip = d3.tip()
    .attr("class", "d3-tip")
    .offset([0, 0])
    .html(function (d) {
      var rStr = d.size.toString().substring(0, 4);
      var rFY = d.FY;
      var rCSC = d.CSC
      if (parseFloat(rStr) < 0.01) {
        rStr = "Less than 0.01";
      } else {
        rStr = "~"+rStr;
      }
      return "Science Center: " + rCSC + "<br>" + 
      "Fiscal Year: " + rFY + "<br>" +
      "Project Number: " + d.number + "<br>" +
      rStr + "gb";
    });
  svg.call(tool_tip);


  
  // append the rectangles for the bar svg
  svg.selectAll(".bar")
      .data(data)
    .enter().append("rect")
      .attr("class", function (d) { console.log(d.CSC); return "bar "+d.CSC; })
      // .attr("class", function (d) { console.log(d.CSC); return d.CSC; })
      .attr("id", function (d) { return "FY"+d.FY; })
      //.attr("x", function(d) { return x(d.sales); })
      .attr("width", function(d) {return x(d.size); } )
      .attr("y", function(d) { return y(d.number); })
      .attr("data-legend", function (d) {return d.CSC + " FY: " + d.FY})
      .attr("height", y.bandwidth())
      .on('mouseover', tool_tip.show)
      .on('mouseout', tool_tip.hide);

  // add the x Axis
  svg.append("g")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x));

  // add the y Axis
  svg.append("g")
      .call(d3.axisLeft(y));

  //Adding x axis label
  svg.append("text")
    .attr("y", (height + margin.bottom / 2))
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
      .text("ScienceBase Project Size Comparison-- " + currCSC);

  //Adding Legend
  var legendRectSize = 18;
  var legendSpacing = 4;
  
  var existing_FYs = [];

  for (var i = 0; i < data.length; i++)
  {
    if ($.inArray(data[i].FY, existing_FYs) === -1) {
      // the value is not in the array
      existing_FYs.push(data[i].FY);
    }
  }
  console.log("existing_FYs");
  console.log(existing_FYs);
  var legend = svg.selectAll('.legend')
    .data(data.filter(function (d) {
      var index = $.inArray(d.FY, existing_FYs);
      if (index > -1) {
        // the value is in the array
        //remove element from array
        existing_FYs.splice(index, 1);
        //use this d:
        return d;
      }
      else {
        //do nothing (skip this d)
      }
    }))
    .enter()
    .append('g')
    .attr('class', 'legend')
      .attr('id', function (d) {return 'FY' + d.FY})
    .attr('transform', function (d, i) {
      // var height = legendRectSize + legendSpacing;
      // var offset = height * data.length / 2;
      // var horz = -2 * legendRectSize;
      // var vert = i * height - offset;
      var horz = width * 0.9;
      var vert = i * 18;
      return 'translate(' + horz + ',' + vert + ')';
    });

  legend.append('rect')
    .attr('class', function (d) { return 'legend ' + currCSC; })
    .attr('id', function (d) { return 'FY' + d.FY; })
    .attr('width', legendRectSize)
    .attr('height', legendRectSize)


  legend.append('text')
    .attr('x', legendRectSize + legendSpacing)
    .attr('y', legendRectSize - legendSpacing)
    .text(function (d) { return "FY "+d.FY; });


  //Updating dimensions
  function updateDimensions(data, winWidth, winHeight) {
    console.log("In UPdateDimensions");
    console.log(data);
    margin.top = 40;
    margin.right = winWidth < breakPoint ? 0 : 20;
    margin.left = winWidth < breakPoint ? 0 : 40;
    margin.bottom = 30;

    width = (winWidth * .75) - margin.left - margin.right;
    var barRelativeSize = 70 + (10 * data.length)
    var widthRelativeSize = .5 * width;
    height = widthRelativeSize > barRelativeSize ? widthRelativeSize : barRelativeSize;
    widthRelativeSize > barRelativeSize ? console.log("widthRelativeSize") : console.log("barRelativeSize");
    if(barRelativeSize > window.innerHeight)
    {
      height = winHeight * 0.5;
      console.log("Height = window.innerHeight");
    }
    console.log("End updateDimensions");
  }
}

// var createGraphfunc = createGraph();

// console.log("projectObjArray...");
// console.log(projectObjArray);

// d3.select(window).on('resize', createGraph(projectObjArray));
function catchResize () {
  console.log("Resized1!");
  d3.select("#projectGraph_svg").remove();
  d3.select("#projectGraph_svg").remove(); //once for each CSC
  projectBarGraph(reportDict);

}
// d3.select(window).on('resize', go);
window.addEventListener('resize', catchResize);
// addEvent(window, "resize", function (event) {
//   console.log('resized');
// });
}
