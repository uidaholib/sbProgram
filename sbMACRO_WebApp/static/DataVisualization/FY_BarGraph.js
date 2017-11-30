// Doctored From http://bl.ocks.org/kiranml1/6872226 
function FY_BarGraph (reportDict) {
  // console.log("GRAPH-BUILDING SCRIPT");   //DeBug
  $(document).ready(function () {
    console.log(reportDict);
  if(reportDict.report.length > 1){
    // console.log("More than 1 fiscal year chosen!");
    $("<br><br>").insertAfter("#wrapper");

    var fyObjArray = [];

    function createAndAddFYObject(FYname, FYsize, FYcsc){
      var FY = {};
      FY.name = FYname;
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
    var data = fyObjArray;
    console.log("data:");
    console.log(data);


    //Now, building the graph:
    
    // set the dimensions and margins of the graph
    var margin = { top: 40, right: 20, bottom: 30, left: 60 },
      width = 960 - margin.left - margin.right,
      height = 150 - margin.top - margin.bottom;
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
    var svg = d3.select("#fyGraphWrapper").append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform",
      "translate(" + margin.left + "," + margin.top + ")");

    // format the data
    data.forEach(function (d) {
      d.size = +d.size;
    });
 

    // Scale the range of the data in the domains
    x.domain([0, d3.max(data, function (d) { return d.size; })])
    y.domain(d3.range(data.length));
    // y.domain(data.map(function (d) { return d.name; }));
    //y.domain([0, d3.max(data, function(d) { return d.sales; })]);

    // append the rectangles for the bar chart
    svg.selectAll(".bar")
      .data(data)
      .enter().append("rect")
        .attr("class", "bar")
        //.attr("x", function(d) { return x(d.sales); })
        .attr("width", function (d) { return x(d.size); })
        .attr("y", function (d,i) { return y(i); })
        .attr("height", y.bandwidth());

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
      .text("ScienceBase Fiscal Year Data Comparison");


  } else {
    console.log("Only 1 FY chosen");
  }
})
}