  
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
  // // my version: format data
  // projectObjArray.forEach(function (d) {
  //   d.size = +d.size; //not sure what this means or how it formats the data.
  // });

  // Scale the range of the data in the domains
  x.domain([0, d3.max(data, function(d){ return d.size; })])
  y.domain(data.map(function(d) { return d.number; }));
  //y.domain([0, d3.max(data, function(d) { return d.sales; })]);

  // //My version: scale the range of the data in the domains
  // x.domain([0, d3.max(projectObjArray, function(d){ return d.size; })])
  // y.domain(projectObjArray.map(function(d) { return d.number; }));
  

  // append the rectangles for the bar chart
  svg.selectAll(".bar")
      .data(data)
    .enter().append("rect")
      .attr("class", "bar")
      //.attr("x", function(d) { return x(d.sales); })
      .attr("width", function(d) {return x(d.size); } )
      .attr("y", function(d) { return y(d.number); })
      .attr("height", y.bandwidth());

  // // My version: append the rectangles for the bar chart
  // svg.selectAll(".bar")
  //     .data(projectObjArray)
  //   .enter().append("rect")
  //     .attr("class", "bar")
  //     //.attr("x", function(d) { return x(d.sales); })
  //     .attr("width", function (d) { return x(d.size); })
  //     .attr("y", function (d, i) {
  //       return i * (width / projectObjArray.length);
  //     })
  //     .attr("height", y.bandwidth());

  // add the x Axis
  svg.append("g")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x));

  // add the y Axis
  svg.append("g")
      .call(d3.axisLeft(y));

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