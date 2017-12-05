  
function projectBarGraph (reportDict) {
  // console.log("GRAPH-BUILDING SCRIPT");   //DeBug
  $(document).ready(function () {
    console.log("reportDict in second script:");   //DeBug
    
    console.log(reportDict);   //DeBug
    
  var projectObjArray = [];

  var createAndAddObject = function (name, size, number) {
    var project = {};
    project.name = name;
    if (size === "None") {
      // console.log("It's NONE")   //DeBug
      project.size = 0;
    } else {
      project.size = size;
    }
    project.number = number.toString();
    // console.log("project:");   //DeBug
    // console.log(project);   //DeBug
    projectObjArray.push(project);
    // console.log("!!!!!!!!!!!!array:");   //DeBug
    // console.log(projectObjArray);   //DeBug
  }
  function iterate(reportDict) {
    var report = reportDict.report;
    var projectNumber = 0
    // console.log("report");   //DeBug
    // console.log(report);   //DeBug
    for (var i = 0; i < report.length; i++) {
      var fiscalYear = report[i];
      // console.log("fiscalYear:")   //DeBug
      // console.log(fiscalYear);   //DeBug
      for (var z = 0; z < fiscalYear.length; z++) {
        projectNumber++;
        var projectObj = fiscalYear[z];
        var name = projectObj.name;
        // console.log("name");   //DeBug
        // console.log(name);   //DeBug
        var size = projectObj.DataInProject;
        // console.log("data");   //DeBug
        // console.log(data);   //DeBug
        createAndAddObject(name, size, projectNumber);
      }
    }
  }
  iterate(reportDict);
  console.log("projectObjArray");
  console.log(projectObjArray);
  

  var data = projectObjArray;
  // set the dimensions and margins of the graph
  var margin = {top: 40, right: 20, bottom: 30, left: 40},
      width = 960 - margin.left - margin.right,
      height = 500 - margin.top - margin.bottom;
      //Should set width and height dynamically

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
      .append("g")
      .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

  // format the data
  data.forEach(function(d) {
    d.size = +d.size;
  });

  // Scale the range of the data in the domains
  x.domain([0, d3.max(data, function(d){ return d.size; })])
  y.domain(data.map(function(d) { return d.number; }));
  //y.domain([0, d3.max(data, function(d) { return d.sales; })]);

  //Adding labels for amount of each bar

  //d3-tip: http://bl.ocks.org/davegotz/bd54b56723c154d25eedde6504d30ad7
  // Setup the tool tip.  Note that this is just one example, and that many styling options are available.
  // See original documentation for more details on styling: http://labratrevenge.com/d3-tip/
    var tool_tip = d3.tip()
      .attr("class", "d3-tip")
      .offset([0, 0])
      .html(function (d) {
        var rStr = d.size.toString().substring(0, 4);
        if (parseFloat(rStr) < 0.01) {
          rStr = "Less than 0.01";
        } else {
          rStr = "~"+rStr;
        }
        return rStr + "gb";
      });
  svg.call(tool_tip);



  // append the rectangles for the bar chart
  svg.selectAll(".bar")
      .data(data)
    .enter().append("rect")
      .attr("class", "bar")
      //.attr("x", function(d) { return x(d.sales); })
      .attr("width", function(d) {return x(d.size); } )
      .attr("y", function(d) { return y(d.number); })
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
      .text("ScienceBase Project Size Comparison");

  })
}