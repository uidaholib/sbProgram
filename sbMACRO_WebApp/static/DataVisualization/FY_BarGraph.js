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
      // y.domain(d3.range(data.length));
      y.domain(data.map(function (d) { return d.name; }));
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
          return rStr+"gb"; 
        });
      svg.call(tool_tip);


      // append the rectangles for the bar chart
      
      var bars = svg.selectAll(".bar")
        .data(data)
        .enter().append("rect")
          .attr("class", "bar")
          .attr("id", function (d) {console.log(d.CSC); return d.CSC; })
          //.attr("x", function(d) { return x(d.sales); })
          .attr("width", function (d) { return x(d.size); })
          .attr("y", function (d,i) { return y(d.name); })
          .attr("height", y.bandwidth())
          .on('mouseover', tool_tip.show)
          .on('mouseout', tool_tip.hide);

      // add the x Axis
      svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x));

      // add the y Axis
      var FYList = data.map(function (obj) {return obj.name});

      var yAxis = d3.axisLeft(y)  //);
        .tickFormat(function (d) { return d.substring(5, 13); });

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

      


    } else {
      console.log("Only 1 FY chosen");
    }
})
}